from datetime import datetime, date


class Post:
    def __init__(self, group_id, timestamp, likes, reposts, views, text, attachments):
        self.group_id = group_id
        self.date = self.extract_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.views = views
        self.text = text
        self.attachments = attachments
        self.photos = self.extract_photos()
        self.suitable = self.check_the_suitability()

    def __str__(self):
        return f'Id: {self.group_id}, Date: {self.date}, Likes: {self.likes}, Reposts: {self.reposts}, ' \
               f'Views: {self.views}Attachments: {len(self.attachments)}, Photos: {len(self.photos)}, ' \
               f'Text: "{self.text}", Suitable: {self.suitable}.'

    def __eq__(self, other):
        if isinstance(other, Post):
            return self.group_id == other.group_id and self.date == other.date and self.likes == other.likes and \
                   self.reposts == other.reposts and self.attachments == other.attachments and \
                   self.views == other.views and self.photos == other.photos and self.text == other.text and \
                   self.suitable == other.suitable
        return False

    def extract_photos(self):
        """
        Extract photo ids from attachments json
        :return: list of photo ids
        """
        if self.attachments == []:
            return []
        return [attachment['photo']['id'] for attachment in self.attachments if attachment['type'] == 'photo']

    def check_the_suitability(self):
        """
        Checking that there are only photos in the post, that is, there are no videos, music, polls, etc.
        :return: True, if photos and attachments are the same size, False otherwise
        """
        return len(self.attachments) == len(self.photos)

    @staticmethod
    def extract_date(timestamp):
        """
        Convert timestamp to date in YYYY-MM-DD format
        :param timestamp: string timestamp, maybe from VK API response
        :return: string in YYYY-MM-DD format
        """
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

    @classmethod
    def get_tomorrow_timestamp(cls):
        """
        Get timestamp of tomorrow day at 00:00:00
        :return: integer timestamp
        """
        today = date.today().strftime('%Y-%m-%d')
        return datetime(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) + 1).timestamp()
