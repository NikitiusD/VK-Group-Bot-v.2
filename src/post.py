from useful_functions import extract_date
from math import inf


class Post:
    def __init__(self, group_id, group_name, members_count, timestamp, likes, reposts, views, text, attachments):
        self.group_id = group_id
        self.group_name = group_name
        self.members_count = members_count
        self.date = extract_date(timestamp)
        self.likes = likes
        self.reposts = reposts
        self.likes_per_repost = round(self.likes / self.reposts) if self.reposts != 0 else inf
        self.views = views
        self.like_conversion_pct = round((self.likes / self.views) * 100, 5) if self.views != 0 else 0
        self.repost_conversion_pct = (self.reposts / self.views) * 100 if self.views != 0 else 0
        self.overall_rating = 0
        self.text = text
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
