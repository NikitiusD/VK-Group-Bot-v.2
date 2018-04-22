from BotLogic.VKRequest import VKRequest as req
from BotLogic.Group import Group
from BotLogic.Post import Post
from time import sleep


class Bot:
    def __init__(self):
        with open('..\Information\meme_force_id.txt') as group_id:
            self.group_id = group_id.read()
        self.public_ids = self.get_public_ids()
        self.top_posts = self.get_top_posts()[:25]
        self.post_in_group()

    def get_public_ids(self):
        method_name = 'groups.getById'
        parameters = {'group_id': self.group_id, 'fields': 'links'}
        response = req().get(method_name, parameters)
        short_names = [info['url'].split('/')[3] for info in response['response'][0]['links']]
        return Group.get_ids_from_urls(short_names)

    def get_top_posts(self):
        top_posts = []
        for id in self.public_ids:
            group = Group(id)
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


