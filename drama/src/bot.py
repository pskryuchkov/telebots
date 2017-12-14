# -*- coding: utf-8 -*-
from copa import *
import telebot
import random
import glob

problem_solution = ["Выеби ее",
                    "Не еби ее",
                    "Напиши ей",
                    "Позвони ей",
                    "Найди новую",
                    "Не ной",
                    "Купи ей цветы",
                    "Выеби другую",
                    "Выеби ее подругу",
                    "Пошли ее нахуй"]

be_a_man = ", будь мужиком, блеать!"

config = get_params("../config.json")
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    if message.text == "/cry":
        portraits = list(map(lambda x: x.strip(), open("../" + config.pretty_girl +
                                                        "/portraits.txt", "r").readlines()))
        songs = glob.glob("../music/*.mp3")

        cry_photo = open('../{}/{}.jpg'.format(config.pretty_girl, random.choice(portraits)), 'rb')
        cry_song = open(random.choice(songs), 'rb')

        bot.send_photo(message.chat.id, cry_photo)
        bot.send_audio(message.chat.id, cry_song)

    elif message.text == "/advice":
        advice = random.choice(problem_solution) + be_a_man
        bot.send_message(message.chat.id, advice)

if __name__ == '__main__':
    bot.polling(none_stop=True)






