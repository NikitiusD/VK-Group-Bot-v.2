from BotLogic.VKRequest import VKRequest as req
from BotLogic.Post import Post


class Group:
    def __init__(self, id):
        self.id = id
        self.all_posts = self.get_all_posts()
        self.top_post = self.choose_top_post()

    def get_all_posts(self):
        method_name = 'wall.get'
        parameters = {'owner_id': f'-{self.id}', 'count': '100', 'filter': 'owner'}
        response = req().get(method_name, parameters)
        return [Post(post['date'], post['likes']['count'], post['reposts']['count'],
                     post['text'], post.get('attachments', [])) for post in response['response']['items']]

    @staticmethod
    def get_ids_from_urls(urls):
        method_name = 'groups.getById'
        for i, url in enumerate(urls):
            if len(url) > 5 and url[:6] == 'public':
                urls[i] = urls[i][6:]
        parameters = {'group_ids': ','.join(urls)}
        response = req().get(method_name, parameters)
        return [info['id'] for info in response['response']]

    def choose_top_post(self):
        pass
