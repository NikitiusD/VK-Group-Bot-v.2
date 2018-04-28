from BotLogic.VKRequest import VKRequest as req
from BotLogic.Group import Group
from BotLogic.UsefullFunctions import get_tomorrow_timestamp
from BotLogic.UsefullFunctions import like_repost_plot
from time import sleep
from datetime import date
from random import shuffle
import json
import os


class Bot:
    vk_limit = 25

    def __init__(self):
        with open('..\Information\\your_public_id.txt') as group_id:
            self.my_group_id = group_id.read()
        self.group_ids = self.get_group_ids()
        self.group_names = self.get_group_names()
        self.members_count = self.get_members_count()
        self.top_posts = self.get_top_posts()
        self.selected_posts = self.select_top_posts()
        # self.post_in_group()
        # self.log_posts()
        self.print_main_info()

    def get_group_ids(self):
        """
        Gets the group ids from your groups link list
        :return: list of ids
        """
        method_name = 'groups.getById'
        parameters = {'group_id': self.my_group_id, 'fields': 'links'}
        response = req().get(method_name, parameters)
        short_names = [group_info['url'].split('/')[3] for group_info in response['response'][0]['links']]
        ids = Group.get_ids_from_urls(short_names)
        return ids

    def get_group_names(self):
        """
        Gets names of all groups
        :return: list of names
        """
        method_name = 'groups.getById'
        parameters = {'group_ids': ','.join([str(id) for id in self.group_ids])}
        response = req().get(method_name, parameters)
        names = [group_info['name'] for group_info in response['response']]
        return names

    def get_members_count(self):
        """
        Gets the number of subscribers of groups by their ids
        :return: list with the number of subscribers of groups
        """
        method_name = 'groups.getById'
        parameters = {'group_ids': ','.join([str(id) for id in self.group_ids]), 'fields': 'members_count'}
        response = req().get(method_name, parameters)
        members_count = [group_info['members_count'] for group_info in response['response']]
        return members_count

    def get_top_posts(self):
        """
        Gets the list of top posts, one post from each group and then sort them by its conversion
        :return: list of top posts
        """
        top_posts = [Group(id, name, members_count).top_post
                     for id, name, members_count in zip(self.group_ids, self.group_names, self.members_count)]
        top_posts = [post for post in top_posts if post is not None]
        # top_posts = sorted(top_posts, key=lambda x: x.repost_conversion_pct, reverse=True)
        top_posts = sorted(top_posts, key=lambda x: x.likes_per_repost, reverse=False)
        return top_posts

    def select_top_posts(self):
        """
        Selects 25 or less best posts with some randomization and shuffle them
        :return: list of posts
        """
        if len(self.top_posts) >= int((self.vk_limit * 1.4)):
            selected_posts = self.top_posts[:int((self.vk_limit * 1.4))]
        elif len(self.top_posts) >= self.vk_limit:
            selected_posts = self.top_posts[:self.vk_limit]
        else:
            selected_posts = self.top_posts
        shuffle(selected_posts)

        return selected_posts[:self.vk_limit] if len(self.top_posts) >= self.vk_limit else selected_posts

    def post_in_group(self):
        """
        Makes deferred posts in your group of 25 selected posts in such a way that they are published after a
        certain period, calculated on the basis of their number
        """
        publish_timestamp = get_tomorrow_timestamp()
        amount_of_posts = len(self.selected_posts)
        time_interval = round(24 * 60 * 60 / (amount_of_posts * 60)) - 1

        for post in self.selected_posts:
            attachments = [f'photo{photo[0]}_{photo[1]}' for photo in post.photos] + \
                          [f'video{video[0]}_{video[1]}' for video in post.videos] + \
                          [f'audio{audio[0]}_{audio[1]}' for audio in post.audios] + \
                          [f'poll{poll[0]}_{poll[1]}' for poll in post.polls] + \
                          [f'note{note[0]}_{note[1]}' for note in post.notes] + \
                          [f'doc{doc[0]}_{doc[1]}' for doc in post.docs]
            method_name = 'wall.post'
            parameters = {'owner_id': f'-{self.my_group_id}', 'from_group': 1, 'message': post.text,
                          'attachments': ','.join(attachments), 'publish_date': publish_timestamp}
            response = req().post(method_name, parameters)
            print(response)
            publish_timestamp += time_interval * 60
            sleep(0.33)
        pass

    def log_posts(self):
        """
        Logs all posted posts
        """
        try:
            os.mkdir('..\logs', 777)
        except OSError:
            pass
        json_log = json.dumps([post.__dict__ for post in self.selected_posts], indent=4, ensure_ascii=False)
        today = date.today().strftime('%Y-%m-%d')
        with open(f'..\logs\log_{today}.txt', 'w+', encoding='utf-8') as file:
            file.write(json_log)
        pass

    def print_main_info(self):
        top_posts = self.selected_posts
        # top_posts = sorted(self.selected_posts, key=lambda x: x.repost_conversion_pct, reverse=True)
        top_posts = sorted(self.selected_posts, key=lambda x: x.likes_per_repost, reverse=False)
        like_repost_plot(top_posts)

        # print(len(self.top_posts))
        # for post in self.top_posts:
        #     print(f'{post.like_conversion_pct} - {post.repost_conversion_pct}')
        # pass
