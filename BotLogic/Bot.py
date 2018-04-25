from BotLogic.VKRequest import VKRequest as req
from BotLogic.Group import Group
from BotLogic.Post import Post
from time import sleep


class Bot:
    def __init__(self):
        with open('..\Information\meme_force_id.txt') as group_id:
            self.my_group_id = group_id.read()
        self.group_ids = self.get_group_ids()
        self.members_count = self.get_members_count()
        self.top_posts = self.get_top_posts()
        self.selected_posts = self.select_top_posts()
        self.post_in_group()

    def get_group_ids(self):
        """
        Gets the group ids from your groups link list
        :return: list of ids
        """
        method_name = 'groups.getById'
        parameters = {'group_id': self.my_group_id, 'fields': 'links'}
        response = req().get(method_name, parameters)
        short_names = [info['url'].split('/')[3] for info in response['response'][0]['links']]
        ids = Group.get_ids_from_urls(short_names)
        return ids

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
        Gets the list of top posts, one post from each group
        :return: list of top suitable posts
        """
        top_posts = [Group(id, members_count).top_post for id, members_count in zip(self.group_ids, self.members_count)]
        top_posts = [post for post in top_posts if post is not None and post.suitable]
        return top_posts

    def select_top_posts(self):
        """
        Selects best posts by sorting all posts by its conversion
        :return: list of 25 top posts
        """
        sorted_posts = sorted(self.top_posts, key=lambda x: x.conversion, reverse=True)
        return sorted_posts[:25]

    def post_in_group(self):
        """
        Makes deferred posts in your group of 25 selected posts in such a way that they are published after a
        certain period, calculated on the basis of their number
        """
        publish_timestamp = Post.get_tomorrow_timestamp()
        amount_of_posts = len(self.selected_posts)
        time_interval = round(24 * 60 * 60 / (amount_of_posts * 60)) - 1

        for i, post in enumerate(self.selected_posts):
            attachments = [f'photo-{post.group_id}_{photo}' for photo in post.photos]
            method_name = 'wall.post'
            parameters = {'owner_id': f'-{self.my_group_id}', 'from_group': 1, 'message': post.text,
                          'attachments': ','.join(attachments), 'publish_date': publish_timestamp}
            response = req().post(method_name, parameters)
            print(response)
            publish_timestamp += time_interval * 60
            sleep(0.33)
