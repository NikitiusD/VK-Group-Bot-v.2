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
        self.photos = []
        self.videos = []
        self.audios = []
        self.polls = []
        self.notes = []
        self.docs = []
        self.members_count = members_count
        self.extract_media(attachments)

    def __str__(self):
        return ', '.join([f'{attribute}: {self.__dict__[attribute]}'for attribute in list(self.__dict__.keys())])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def extract_media(self, attachments):
        """
        Extract media from attachments
        :param attachments: attachments json from VK API's response
        """
        for attachment in attachments:
            if attachment['type'] == 'photo':
                self.photos.append(attachment['photo']['id'])
            if attachment['type'] == 'video':
                self.videos.append(attachment['video']['id'])
            if attachment['type'] == 'audio':
                self.audios.append(attachment['audio']['id'])
            if attachment['type'] == 'poll':
                self.polls.append(attachment['poll']['id'])
            if attachment['type'] == 'doc':
                self.docs.append(attachment['doc']['id'])
            if attachment['type'] == 'note':
                self.notes.append(attachment['note']['id'])

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
