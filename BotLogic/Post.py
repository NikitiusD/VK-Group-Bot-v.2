from datetime import datetime


class Post:
    def __init__(self, timestamp, likes, reposts, text, attachments):
        self.date = self.eject_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.attachments = attachments
        self.photos = self.eject_photos()
        self.text = text
        self.suitable = self.check_the_suitability()

    def __str__(self):
        return f'Date: {self.date}, Likes: {self.likes}, Reposts: {self.reposts}, ' \
               f'Attachments: {len(self.attachments)}, Photos: {len(self.photos)}, Text: "{self.text}", ' \
               f'Suitable: {self.suitable}.'

    def __eq__(self, other):
        if isinstance(other, Post):
            return self.date == other.date and self.likes == other.likes and self.reposts == other.reposts \
               and self.attachments == other.attachments and self.photos == other.photos \
               and self.text == other.text and self.suitable == other.suitable
        return False

    def eject_photos(self):
        if self.attachments == []:
            return []
        return [attachment['photo']['id'] for attachment in self.attachments if attachment['type'] == 'photo']

    def check_the_suitability(self):
        return len(self.attachments) == len(self.photos)

    def eject_date(self, timestamp):
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
