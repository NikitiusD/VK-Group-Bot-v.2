class Post:
    def __init__(self, date, likes, reposts, text, attachments):
        self.date = date
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

    def eject_photos(self):
        if self.attachments == []:
            return []
        return [attachment['photo']['id'] for attachment in self.attachments if attachment['type'] == 'photo']

    def check_the_suitability(self):
        return len(self.attachments) == len(self.photos)
