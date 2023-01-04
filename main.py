import os
import telegram

from dotenv import load_dotenv


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    updates = bot.get_updates()
    chat_id = updates[-1].message.chat_id

    bot.send_message(text="Hi Nurlan", chat_id=chat_id)
    bot.send_message(text="This is another test message", chat_id=chat_id)
    bot.send_message(text="I'm sorry Nurlan I'm afraid I can't do that.", chat_id=chat_id)


if __name__ == '__main__':
    main()
