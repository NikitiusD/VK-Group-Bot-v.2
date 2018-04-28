from datetime import datetime, date
import numpy as np
import matplotlib.pyplot as plt


def like_repost_plot(posts):
    border = len(posts) + 1
    x = np.arange(1, border)
    likes = [post.likes for post in posts]
    reposts = [post.reposts for post in posts]
    likes_per_repost = [post.likes_per_repost for post in posts]
    likes_pct = [post.like_conversion_pct for post in posts]
    reposts_pct = [post.repost_conversion_pct * 10 for post in posts]

    plt.rcParams['axes.grid'] = True

    plt.subplot(221)
    plt.plot(x, likes, color='b')
    plt.plot(x, likes, 'bo')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)
    plt.title('Amount of likes')

    plt.subplot(222)
    plt.plot(x, reposts, color='g')
    plt.plot(x, reposts, 'go')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)
    plt.title('Amount of reposts')

    plt.subplot(223)
    plt.plot(x, likes_pct, color='b', label='Like conv., %')
    plt.plot(x, likes_pct, 'bo')
    plt.plot(x, reposts_pct, color='g', label='Repost conv. * 10, %')
    plt.plot(x, reposts_pct, 'go')
    plt.title('Like and Repost Converison')
    plt.legend()
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)

    plt.subplot(224)
    plt.plot(x, likes_per_repost, 'ro', x, likes_per_repost)
    plt.title('Likes per repost')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)

    plt.show()


def extract_date(timestamp):
    """
    Converts timestamp to date
    :param timestamp: string timestamp from VK API response
    :return: date
    """
    return date.fromtimestamp(int(timestamp))


def get_tomorrow_timestamp():
    """
    Gets timestamp of tomorrow day at 00:00:00
    :return: integer timestamp
    """
    today = date.today()
    return datetime(today.year, today.month, today.day + 1).timestamp()


def get_yesterday():
    """
    Gets yesterday date
    :return: date
    """
    today = date.today()
    return date(today.year, today.month, today.day - 1)
