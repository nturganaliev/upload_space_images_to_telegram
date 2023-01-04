import argparse
import os
import random
import time
import telegram

from dotenv import load_dotenv


def post_image_to_channel(token, document):
    bot = telegram.Bot(token)
    updates = bot.get_updates()
    chat_id = updates[-1]['channel_post']['chat']['id']
    bot.send_document(chat_id, document)


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    images = list(os.walk(os.path.join(os.path.abspath("."), "images")))[0][2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "pause_time",
            help="Post to telegram pause time",
            type=str
    )
    args = parser.parse_args()
    pause_time = 4*60*60 if not args.pause_time else int(args.pause_time)
    try:
        while True:
            if not images:
                images = list(os.walk(os.path.join(os.path.abspath("."),
                                                   "images")))[0][2]
                random.shuffle(images)
            document = open(f"images/{images.pop()}", 'rb')
            post_image_to_channel(token, document)
            time.sleep(pause_time)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
