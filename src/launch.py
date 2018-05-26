from bot import Bot
import json


def main():
    """
    Reads the config, checks for errors and launches bots for all specified groups
    """
    config = json.load(open('..\config.json'))
    groups = config['groups']

    for i, group in enumerate(groups):
        if not (len(group) == 4
                and isinstance(group['group_id'], str)
                and isinstance(group['number_of_posts'], int)
                and isinstance(group['repost_border'], int)
                and (isinstance(group['scatter'], int) or isinstance(group['scatter'], float))
                and group['scatter'] >= 1
                and group['repost_border'] >= 0
                and group['number_of_posts'] <= config['vk_limit']):
            print(f'Wrong data in group {i+1} in config. There must be 4 parameters:'
                  f'\n\'group_id\' must be string'
                  f'\n\'number_of_posts\' must be integer and less or equal than "vk_limit"'
                  f'\n\'repost_border\' must be integer and not less than 0'
                  f'\n\'scatter\' must be integer or float and not less than 1')
            exit(1)

    for i, group in enumerate(groups):
        Bot(i, group['group_id'], group['number_of_posts'], group['repost_border'], group['scatter'])


if __name__ == '__main__':
    main()
