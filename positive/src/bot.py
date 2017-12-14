from copa import *
import telebot
import random


config = get_params("../config.json")
bot = telebot.TeleBot(config.bot_token)


def load_news():
    sep = "; "
    pos_val = 0.6

    with open("../data/sent.csv", "r") as f:
        next(f)
        lines = f.readlines()

    data = []

    for line in lines:
        source, title, val = line.split(sep)

        source, title, val = source.strip(), title.strip(), float(val)

        if val > pos_val:
            data.append([source, title, val])

    return data


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    if message.text == "/n":
        item = random.choice(news)
        msg = "{0}: {1}".format(item[0].upper(), item[1])
        bot.send_message(message.chat.id, msg)


if __name__ == '__main__':
    news = load_news()
    print("n_positive: {}".format(len(news)))
    bot.polling(none_stop=True)