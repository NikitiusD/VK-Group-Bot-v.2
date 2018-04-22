from datetime import datetime, date


class Post:
    def __init__(self, group_id, timestamp, likes, reposts, text, attachments):
        self.group_id = group_id
        self.date = self.eject_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.attachments = attachments
        self.photos = self.eject_photos()
        self.text = text
        self.suitable = self.check_the_suitability()

    def __str__(self):
        return f'Id: {self.group_id}, Date: {self.date}, Likes: {self.likes}, Reposts: {self.reposts}, ' \
               f'Attachments: {len(self.attachments)}, Photos: {len(self.photos)}, Text: "{self.text}", ' \
               f'Suitable: {self.suitable}.'

    def __eq__(self, other):
        if isinstance(other, Post):
            return self.group_id == other.group_id and self.date == other.date and self.likes == other.likes and \
                   self.reposts == other.reposts and self.attachments == other.attachments and \
                   self.photos == other.photos and self.text == other.text and self.suitable == other.suitable
        return False

    def eject_photos(self):
        if self.attachments == []:
            return []
        return [attachment['photo']['id'] for attachment in self.attachments if attachment['type'] == 'photo']

    def check_the_suitability(self):
        return len(self.attachments) == len(self.photos)

    @staticmethod
    def eject_date(timestamp):
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

    @classmethod
    def get_tomorrow_timestamp(cls):
        today = date.today().strftime('%Y-%m-%d')
        return datetime(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) + 1).timestamp()
