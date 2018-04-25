from datetime import datetime, date


class Post:
    def __init__(self, group_id, group_name, timestamp, likes, reposts, views, text, members_count, attachments):
        self.group_id = group_id
        self.group_name = group_name
        self.date = self.extract_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.views = views
        self.text = text
        self.like_conversion = round(self.likes / self.views, 5)
        self.members_count = members_count
        self.photos = self.extract_photos(attachments)
        self.suitable = self.check_the_suitability(attachments)

    def __str__(self):
        return ', '.join([f'{attribute}: {self.__dict__[attribute]}'for attribute in list(self.__dict__.keys())])

    def __eq__(self, other):
        if isinstance(other, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def extract_photos(self, attachments):
        """
        Extract photo ids from attachments json
        :return: list of photo ids
        """
        return [attachment['photo']['id'] for attachment in attachments if attachment['type'] == 'photo']

    def check_the_suitability(self, attachments):
        """
        Checking that there are only photos in the post, that is, there are no videos, music, polls, etc.
        :return: True, if photos and attachments are the same size, False otherwise
        """
        return len(attachments) == len(self.photos)

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
