from BotLogic.VKRequest import VKRequest as req
from BotLogic.Post import Post
from datetime import date


class Group:
    def __init__(self, id):
        self.id = id
        self.all_posts = self.get_all_posts()
        self.yesterday_posts = self.get_yesterday_posts()
        self.top_post = self.choose_top_post()

    def get_all_posts(self):
        method_name = 'wall.get'
        parameters = {'owner_id': f'-{self.id}', 'count': '100', 'filter': 'owner'}
        response = req().get(method_name, parameters)
        posts = [Post(self.id, post['date'], post['likes']['count'], post['reposts']['count'],
                      post['text'], post.get('attachments', [])) for post in response['response']['items']]
        return posts

    def get_yesterday_posts(self):
        today = date.today().strftime('%Y-%m-%d')
        yesterday = date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) - 1)\
            .strftime('%Y-%m-%d')
        yesterday_posts = [post for post in self.all_posts if post.date == yesterday]
        return yesterday_posts

    def choose_top_post(self):
        likes_max = 0
        top_post = 0
        for post in self.yesterday_posts:
            if post.likes > likes_max:
                likes_max = post.likes
                top_post = post
        if top_post == 0:
            return None
        return top_post

    @staticmethod
    def get_ids_from_urls(urls):
        method_name = 'groups.getById'
        for i, url in enumerate(urls):
            if len(url) > 5 and url[:6] == 'public':
                urls[i] = urls[i][6:]
        parameters = {'group_ids': ','.join(urls)}
        response = req().get(method_name, parameters)
        return [info['id'] for info in response['response']]