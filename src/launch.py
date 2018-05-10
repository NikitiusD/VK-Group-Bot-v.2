from bot import Bot
import json


def main():
    config = json.load(open('..\config.json'))
    group_ids = config['group_id']
    size = len(group_ids)
    numbers_of_posts = config['number_of_posts']
    repost_borders = config['repost_border']
    scatters = config['scatter']

    if size != len(numbers_of_posts) or size != len(repost_borders) or size != len(scatters):
        print('ERROR\nFix "config.json": there are different sizes of arrays')
        exit(1)

    for i in range(len(group_ids)):
        Bot(i, group_ids[i], numbers_of_posts[i], repost_borders[i], scatters[i])


if __name__ == '__main__':
    main()
