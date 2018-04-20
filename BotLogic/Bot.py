from BotLogic.VKRequest import VKRequest


class Bot:
    def __init__(self):
        with open('..\Information\meme_force_id.txt', 'r') as group_id:
            self.group_id = group_id.read()
        self.public_links = self.get_public_links()
        self.top_posts = self.get_top_posts()
        self.main()

    def main(self):
        pass

    def get_public_links(self):
        method_name = 'groups.getById'
        parameters = {'group_id': self.group_id, 'fields': 'links'}

        response = VKRequest().get(method_name, parameters)
        links = []
        for info in response['response'][0]['links']:
            links.append(info['id'])
        return links

    def get_top_posts(self):
        top = []
        for link in self.public_links:
            posts = self.get_all_posts(link)
            top.append(self.choose_top_post(posts))
        return top

    def get_all_posts(self, link):
        pass

    def choose_top_post(self, posts):
        pass
