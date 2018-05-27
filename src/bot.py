from vk_request import VKRequest as req
from group import Group
from useful_functions import get_tomorrow_timestamp, create_metrics_plot
from time import sleep
from datetime import date
from random import shuffle
import json
import os


class Bot:
    vk_limit = json.load(open('..\config.json'))['vk_limit']
    bad_groups = []

    def __init__(self, index, id, number_of_posts, repost_border, scatter):
        self.index = index + 1
        self.my_group_id = id
        self.number_of_posts = number_of_posts
        self.repost_border = repost_border
        self.scatter = scatter
        self.group_ids = self.get_group_ids()
        self.group_names = self.get_group_names()
        self.members_count = self.get_members_count()
        self.top_posts = self.get_top_posts()
        self.selected_posts = self.select_top_posts()
        self.post_in_group()
        self.log_posts()
        self.print_main_info()

    def get_group_ids(self):
        """
        Gets the Group ids from your Groups link list
        :return: list of ids
        """
        method_name = 'groups.getById'
        parameters = {'group_id': self.my_group_id, 'fields': 'links'}
        response = req().get(method_name, parameters)
        short_names = [group_info['url'].split('/')[3] for group_info in response['response'][0]['links']]
        return Group.get_ids_from_urls(short_names)

    def get_group_names(self):
        """
        Gets names of all Groups
        :return: list of names
        """
        method_name = 'groups.getById'
        parameters = {'group_ids': ','.join([str(id) for id in self.group_ids])}
        response = req().get(method_name, parameters)
        return [group_info['name'] for group_info in response['response']]

    def get_members_count(self):
        """
        Gets the number of subscribers of Groups by their ids
        :return: list with the number of subscribers of Groups
        """
        method_name = 'groups.getById'
        parameters = {'group_ids': ','.join([str(id) for id in self.group_ids]), 'fields': 'members_count'}
        response = req().get(method_name, parameters)
        return [group_info['members_count'] for group_info in response['response']]

    def get_top_posts(self):
        """
        Gets the list of top Posts, one post from each Group and then sort them by its conversion
        :return: list of top Posts
        """
        top_posts = [Group(id, name, members_count).top_post
                     for id, name, members_count in zip(self.group_ids, self.group_names, self.members_count)]

        bad_group_indexes = [index for index, post in enumerate(top_posts) if post is None]
        self.bad_groups = [(self.group_ids[index], self.group_names[index]) for index, post in enumerate(top_posts)
                           if index in bad_group_indexes]
        top_posts = [post for post in top_posts if post is not None and post.reposts > self.repost_border]

        top_repost_posts = sorted(top_posts, key=lambda x: x.repost_conversion_pct)
        top_like_posts = sorted(top_posts, key=lambda x: x.like_conversion_pct)
        for post in top_posts:
            post.overall_rating = top_repost_posts.index(post) + top_like_posts.index(post)

        return sorted(top_posts, key=lambda x: x.overall_rating, reverse=True)

    def select_top_posts(self):
        """
        Selects best Posts with some randomization by shuffling them
        :return: list of Posts
        """
        if len(self.top_posts) >= self.number_of_posts * self.scatter:
            selected_posts = self.top_posts[:int((self.number_of_posts * self.scatter))]
        elif len(self.top_posts) >= self.number_of_posts:
            selected_posts = self.top_posts[:self.number_of_posts]
        else:
            selected_posts = self.top_posts
        shuffle(selected_posts)
        if len(selected_posts) > self.vk_limit:
            selected_posts = selected_posts[:self.vk_limit]
        return selected_posts

    def post_in_group(self):
        """
        Makes deferred Posts in your Group of selected Posts in such a way that they are published after a
        certain period, calculated on the basis of their number
        """
        publish_timestamp = get_tomorrow_timestamp()
        time_interval = round(24 * 60 * 60 / (len(self.selected_posts) * 60)) - 1

        for post in self.selected_posts:
            attachments = ([f'photo{photo[0]}_{photo[1]}' for photo in post.photos] +
                           [f'video{video[0]}_{video[1]}' for video in post.videos] +
                           [f'audio{audio[0]}_{audio[1]}' for audio in post.audios] +
                           [f'poll{poll[0]}_{poll[1]}' for poll in post.polls] +
                           [f'note{note[0]}_{note[1]}' for note in post.notes] +
                           [f'doc{doc[0]}_{doc[1]}' for doc in post.docs])
            method_name = 'wall.post'
            parameters = {'owner_id': f'-{self.my_group_id}', 'from_group': 1, 'message': post.text,
                          'attachments': ','.join(attachments), 'publish_date': publish_timestamp}
            response = req().post(method_name, parameters)
            print(response)
            publish_timestamp += time_interval * 60
            sleep(0.33)

    def log_posts(self):
        """
        Logs all posted Posts and groups without Posts
        """
        try:
            os.mkdir('..\logs', 777)
        except OSError:
            pass
        json_log = json.dumps([post.__dict__ for post in self.selected_posts],
                              indent=4, ensure_ascii=False, default=str)
        today = date.today().strftime('%Y-%m-%d')

        with open(f'..\logs\log_{self.my_group_id}_{today}.txt', 'w+', encoding='utf-8') as file:
            file.write(json_log)

        bad_groups = '\n'.join([f'{group[0]}_{group[1]}' for group in self.bad_groups])
        with open(f'..\logs\log_{self.my_group_id}_{today}_bad_groups.txt', 'w+', encoding='utf-8') as file:
            file.write(bad_groups)

    def print_main_info(self):
        """
        Prints main attributes of each selected Post, names of bad Groups and saves plots
        """
        selected_posts = sorted(self.selected_posts, key=lambda x: x.overall_rating, reverse=True)
        create_metrics_plot(selected_posts, self.my_group_id)
        print(f'Group {self.index}:')
        print(f'Amount of posts: {len(self.top_posts)}, from {len(self.group_ids)} groups.')
        print('Overall rating - Like conv. - Repost conv.')
        for post in selected_posts:
            print(f'{post.overall_rating} - {post.like_conversion_pct} - {post.repost_conversion_pct}')
        print(f'Bad Groups: {[group[1] for group in self.bad_groups]}.')
