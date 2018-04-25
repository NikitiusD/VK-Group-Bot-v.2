from BotLogic.VKRequest import VKRequest as req
from BotLogic.Group import Group
from BotLogic.Post import Post
from time import sleep


class Bot:
    def __init__(self):
        with open('..\Information\meme_force_id.txt') as group_id:
            self.group_id = group_id.read()
        self.public_ids = self.get_public_ids()
        self.members_counts = self.get_members_count()
        self.top_posts = self.get_top_posts()[:25]
        self.post_in_group()

    def get_public_ids(self):
        method_name = 'groups.getById'
        parameters = {'group_id': self.group_id, 'fields': 'links,members_count'}
        response = req().get(method_name, parameters)
        short_names = [info['url'].split('/')[3] for info in response['response'][0]['links']]
        ids = Group.get_ids_from_urls(short_names)
        return ids

    def get_members_count(self):
        method_name = 'groups.getById'
        parameters = {'group_ids': ','.join([str(id) for id in self.public_ids]), 'fields': 'members_count'}
        response = req().get(method_name, parameters)
        members_count = [group_info['members_count'] for group_info in response['response']]
        return members_count

    def get_top_posts(self):
        top_posts = []
        for id, members_count in zip(self.public_ids, self.members_counts):
            group = Group(id, members_count)
            top_posts.append(group.top_post)
        return top_posts

    def post_in_group(self):
        publish_timestamp = Post.get_tomorrow_timestamp()
        amount_of_posts = len([post for post in self.top_posts if post is not None and post.suitable])
        time_interval = round(24 * 60 * 60 / (amount_of_posts * 60)) - 1

        for i, post in enumerate(self.top_posts):
            if post is None or not post.suitable:
                continue
            attachments = [f'photo-{post.group_id}_{photo}' for photo in post.photos]
            method_name = 'wall.post'
            parameters = {'owner_id': f'-{self.group_id}', 'from_group': 1, 'message': post.text,
                          'attachments': ','.join(attachments), 'publish_date': publish_timestamp}
            response = req().post(method_name, parameters)
            print(response)
            publish_timestamp += time_interval * 60
            sleep(0.33)
