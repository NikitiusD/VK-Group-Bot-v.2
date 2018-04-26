from datetime import datetime, date


def extract_date(timestamp):
    """
    Converts timestamp to date in YYYY-MM-DD format
    :param timestamp: string timestamp, maybe from VK API response
    :return: string in YYYY-MM-DD format
    """
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')


def get_tomorrow_timestamp():
    """
    Gets timestamp of tomorrow day at 00:00:00
    :return: integer timestamp
    """
    today = date.today().strftime('%Y-%m-%d')
    return datetime(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) + 1).timestamp()


def get_yesterday():
    """
    Gets yesterday date in YYYY-MM-DD format
    :return: string in YYYY-MM-DD format
    """
    today = date.today().strftime('%Y-%m-%d')
    return date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]) - 1).strftime('%Y-%m-%d')
