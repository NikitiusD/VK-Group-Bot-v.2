from BotLogic.UsefullFunctions import extract_date


class Post:
    def __init__(self, group_id, group_name, members_count, timestamp, likes, reposts, views, text, attachments):
        self.group_id = group_id
        self.group_name = group_name
        self.members_count = members_count
        self.date = extract_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.views = views
        self.text = text
        self.like_conversion_pct = round((self.likes / self.views) * 100, 5)
        self.repost_conversion_pct = (self.reposts / self.views) * 100 if self.reposts != 0 else 0
        self.photos, self.videos, self.audios, self.polls, self.notes, self.docs = [], [], [], [], [], []
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
                self.photos.append((attachment['photo']['owner_id'], attachment['photo']['id']))
            if attachment['type'] == 'video':
                self.videos.append((attachment['video']['owner_id'], attachment['video']['id']))
            if attachment['type'] == 'audio':
                self.audios.append((attachment['audio']['owner_id'], attachment['audio']['id']))
            if attachment['type'] == 'poll':
                self.polls.append((attachment['poll']['owner_id'], attachment['poll']['id']))
            if attachment['type'] == 'doc':
                self.docs.append((attachment['doc']['owner_id'], attachment['doc']['id']))
            if attachment['type'] == 'note':
                self.notes.append((attachment['note']['owner_id'], attachment['note']['id']))
