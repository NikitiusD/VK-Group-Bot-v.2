from vk_request import VKRequest as req
from post import Post
from useful_functions import get_yesterday


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
        :return: list of suitable group posts
        """
        def suitable(post):
            return post.get('views', 0) != 0 and \
                   post['marked_as_ads'] == 0 and \
                   'vk.com/' not in post['text'] and \
                   '[club' not in post['text']

        method_name = 'wall.get'
        parameters = {'owner_id': f'-{self.id}', 'count': '100', 'offset': '1', 'filter': 'owner'}
        response = req().get(method_name, parameters)
        posts = [Post(self.id, self.name, self.members_count, post['date'], post['likes']['count'],
                      post['reposts']['count'], post['views']['count'], post['text'], post.get('attachments', []))
                 for post in response['response']['items'] if suitable(post)]
        return posts

    def choose_yesterday_posts(self):
        """
        Selects yesterday's posts from all posts
        :return: list of yesterday group posts
        """
        yesterday = get_yesterday()
        yesterday_posts = [post for post in self.all_posts if post.date == yesterday]
        return yesterday_posts

    def choose_top_post(self):
        """
        Choose the post with the highest number of likes
        :return: best post
        """
        if len(self.yesterday_posts) == 0:
            return None
        return sorted(self.yesterday_posts, key=lambda x: x.likes, reverse=True)[0]

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
