from BotLogic.VKRequest import VKRequest as req
from BotLogic.Group import Group


class Bot:
    def __init__(self):
        with open('..\Information\meme_force_id.txt', 'r') as group_id:
            self.group_id = group_id.read()
        self.public_ids = self.get_public_ids()
        self.top_posts = self.get_top_posts()

    def get_public_ids(self):
        method_name = 'groups.getById'
        parameters = {'group_id': self.group_id, 'fields': 'links'}
        response = req().get(method_name, parameters)
        short_names = [info['url'].split('/')[3] for info in response['response'][0]['links']]
        return Group.get_ids_from_urls(short_names)

    def get_top_posts(self):
        top_posts = []
        # group = Group('158155713')
        for id in self.public_ids:
            group = Group(id)
            top_posts.append(group.top_post)
        top_posts = [post for post in top_posts if post is not None]
        return top_posts
