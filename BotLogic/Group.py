from BotLogic.VKRequest import VKRequest as req
from BotLogic.Post import Post
from datetime import date


class Group:
    def __init__(self, id, name, members_count):
        self.id = id
        self.name = name
        self.members_count = members_count
        self.all_posts = self.get_all_posts()
        self.yesterday_posts = self.choose_yesterday_posts()
        self.top_post = self.choose_top_post()

    def get_all_posts(self):
        """
        Gets information about the last 100 posts of a group and converts them to a list of instances of the Post class
        :return: list of group posts
        """
        method_name = 'wall.get'
        parameters = {'owner_id': f'-{self.id}', 'count': '100', 'offset': '1', 'filter': 'owner'}
        response = req().get(method_name, parameters)
        posts = [Post(self.id, self.name, post['date'], post['likes']['count'], post['reposts']['count'],
                      post['views']['count'], post['text'], self.members_count, post.get('attachments', []))
                 for post in response['response']['items'] if post.get('views', 0) != 0]
        return posts

    def choose_yesterday_posts(self):
        """
        Selects yesterday's posts from all posts
        :return: list of yesterday group posts
        """
        today = date.today().strftime('%Y-%m-%d')
        yesterday = date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) - 1)\
            .strftime('%Y-%m-%d')
        yesterday_posts = [post for post in self.all_posts if post.date == yesterday]
        return yesterday_posts

    def choose_top_post(self):
        """
        Choose the post with the highest number of likes
        :return: best post
        """
        likes_max = 0
        top_post = Post(0, '', 1234567890, 0, 0, 1, '', 0, [])
        for post in self.yesterday_posts:
            if post.likes > likes_max:
                likes_max = post.likes
                top_post = post
        if top_post == Post(0, '', 1234567890, 0, 0, 1, '', 0, []):
            return None
        return top_post

    @staticmethod
    def get_ids_from_urls(urls):
        """
        Gets ids of groups from it's short names
        :param urls: list of (screen_name)s from VK API aka short names
        :return: list of ids
        """
        method_name = 'groups.getById'
        for i, url in enumerate(urls):
            if len(url) > 5 and url[:6] == 'public':
                urls[i] = urls[i][6:]
        parameters = {'group_ids': ','.join(urls)}
        response = req().get(method_name, parameters)
        ids = [group_info['id'] for group_info in response['response']]
        return ids
