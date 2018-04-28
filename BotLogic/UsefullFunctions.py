from datetime import datetime, date
import numpy as np
import matplotlib.pyplot as plt


def like_repost_plot(posts):
    """
    
    :param posts:
    :return:
    """
    border = len(posts) + 1
    x = np.arange(1, border)
    likes = [post.likes for post in posts]
    reposts = [post.reposts for post in posts]
    likes_per_repost = [post.likes_per_repost for post in posts]
    overall_rating = [post.overall_rating for post in posts]
    likes_pct = [post.like_conversion_pct for post in posts]
    reposts_pct = [post.repost_conversion_pct * 10 for post in posts]

    plt.rcParams['axes.grid'] = True

    plt.subplot(321)
    plt.plot(x, likes, color='b')
    plt.plot(x, likes, 'bo')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)
    plt.title('Amount of likes')

    plt.subplot(322)
    plt.plot(x, reposts, color='g')
    plt.plot(x, reposts, 'go')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)
    plt.title('Amount of reposts')

    plt.subplot(323)
    plt.plot(x, likes_pct, color='b', label='Like conv., %')
    plt.plot(x, likes_pct, 'bo')
    plt.plot(x, reposts_pct, color='g', label='Repost conv. * 10, %')
    plt.plot(x, reposts_pct, 'go')
    plt.title('Like and Repost Conversion')
    plt.legend()
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)

    plt.subplot(324)
    plt.plot(x, likes_per_repost, 'ro', x, likes_per_repost)
    plt.title('Likes per repost')
    plt.xlim(0, border)
    plt.ylim(ymin=0)
    plt.xticks(x)

    plt.subplot(325)
    plt.plot(x, overall_rating, 'mo', x, overall_rating)
    plt.title('Overall Rating')
    plt.xlim(0, border)
    plt.ylim(ymin=(min(overall_rating) // 10) * 10)
    plt.xticks(x)

    plt.subplots_adjust(top=0.97, bottom=0.025, left=0.04, right=0.995, hspace=0.205, wspace=0.07)

    today = date.today().strftime('%Y-%m-%d')
    figure = plt.gcf()
    figure.set_size_inches(16, 9)
    plt.savefig(f'..\logs\log_{today}.png', dpi=120)

    plt.show()
    pass


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