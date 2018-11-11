from vk_request import VKRequest as req
from post import Post
from useful_functions import get_yesterday
from typing import List


class Group:
    def __init__(self, id, name, members_count, max_posts_per_group):
        self.id = id
        self.name = name
        self.members_count = members_count
        self.all_posts = self.get_all_posts()
        self.yesterday_posts = self.choose_yesterday_posts()
        self.top_posts = self.choose_top_posts(max_posts_per_group)

    def get_all_posts(self) -> List[Post]:
        """
        Gets information about the last 100 posts of a group and converts them to a list of instances of the Post class
        :return: list of suitable (not ads or reposts) group Posts
        """
        def suitable(post):
            return (post.get('views', 0) != 0 and post.get('copy_history', 0) == 0 and post['marked_as_ads'] == 0 and
                    'vk.com/' not in post['text'] and '[club' not in post['text'])

        method_name = 'wall.get'
        parameters = {'owner_id': f'-{self.id}', 'count': '100', 'offset': '1', 'filter': 'owner'}
        response = req().get(method_name, parameters)
        posts = [Post(self.id, self.name, self.members_count, post['date'], post['likes']['count'],
                      post['reposts']['count'], post['views']['count'], post['text'], post.get('attachments', []))
                 for post in response['response']['items'] if suitable(post)]
        return posts

    def choose_yesterday_posts(self) -> List[Post]:
        """
        Selects yesterday's posts from all posts
        :return: list of yesterday group Posts
        """
        return [post for post in self.all_posts if post.date == get_yesterday()]

    def choose_top_posts(self, max_posts_per_group) -> List[Post] or None:
        """
        Chooses the best posts
        :return: list of Posts
        """
        if len(self.yesterday_posts) == 0:
            return None
        top_posts = sorted(self.yesterday_posts, key=lambda x: x.likes, reverse=True)
        return top_posts[:max_posts_per_group]

    @staticmethod
    def get_ids_from_urls(urls: List[str]) -> List[str]:
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
        return [group_info['id'] for group_info in response['response']]
