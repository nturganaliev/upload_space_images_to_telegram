import argparse
import os
import random
import time
import telegram

from dotenv import load_dotenv


def upload_image_to_channel(token, image):
    bot = telegram.Bot(token)
    updates = bot.get_updates()
    chat_id = updates[-1]['channel_post']['chat']['id']
    bot.send_document(chat_id, image)


def main():
    load_dotenv()

    if not os.path.exists(os.path.join(os.path.abspath("."), "images")):
        print("Directory 'images' does not exist on a given path.")
        return

    path = os.path.join(os.path.abspath("."), "images")

    if not os.listdir(path):
        print("Folder is empty. First, download images.")
        return

    images = os.listdir(path)
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument(
            "pause_time",
            nargs='?',
            help="Post to telegram pause time",
            default=4*60*60,
            type=int
    )
    args = parser.parse_args()

    try:
        while True:
            if not images:
                images = os.listdir(path)
            random.shuffle(images)
            with open(os.path.join(path, f"{images.pop()}"), 'rb') as image:
                if os.path.getsize(image.name)/(1024**2) < 20:
                    upload_image_to_channel(token, image)
            time.sleep(args.pause_time)
    except telegram.error.BadRequest as bad_request:
        print(bad_request)
    except telegram.error.Unauthorized as unauthorized:
        print(f"{unauthorized}, check your TELEGRAM_BOT_TOKEN")
    print("Завершение программы")


if __name__ == '__main__':
    main()
