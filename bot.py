# -*- coding: utf-8 -*-

from config import *
import telebot
import random
import os


bot = telebot.TeleBot(token)

solution = ["Выеби ее",
            "Не еби ее",
            "Напиши ей",
            "Позвони ей",
            "Найди новую",
            "Не ной",
            "Купи ей цветы",
            "Выеби другую",
            "Пошли ее нахуй"]

be_a_man = ", будь мужиком, блеать!"


@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker'])
def echo_msg(message):
    if message.text == "/cry":
        portraits = map(lambda x: x.strip(), open(pretty_girl + "/portraits.txt", "r").readlines())
        songs = os.listdir("music")

        cry_photo = open('{}/{}.jpg'.format(pretty_girl, random.choice(portraits)), 'rb')
        cry_song = open("music/" + random.choice(songs), 'rb')

        bot.send_photo(message.chat.id, cry_photo)
        bot.send_audio(message.chat.id, cry_song)
    elif message.text == "/advice":
        advice = random.choice(solution) + be_a_man
        bot.send_message(message.chat.id, advice)

if __name__ == '__main__':
    bot.polling(none_stop=True)






