from pprint import pprint
from copa import *
import telebot
import os.path
import random
import glob

from os.path import realpath, dirname
from os import chdir, path
import os
import sys

config = get_params("config.json")
relative_path = '/../../ilovemusic/src'
bot = telebot.TeleBot(config.bot_token)
n_songs = 1


def get_songs(fn):
    file = open(fn, "r")
    return [line.strip() for line in file.readlines() if os.path.isfile(line.strip())]


def warn():
    return "Ooops, I'm not understand you"

@bot.message_handler(func=lambda message: True, content_types=['text'])
def bot_reply(message):
    chdir(dirname(realpath(__file__)))
    available_tags = [os.path.basename(x).split(".")[0]
                      for x in glob.glob("playlists/*.m3u")]
    
    available_classes = ["sad", "dance", "trash", "happy", "melancholia", "rock", "classical", "electronic"]
    
    assert("and" not in available_classes)
    assert("not" not in available_classes)
    
    msg = message.text.lower()
    args = msg.split()

    if len(args) == 1 and msg in available_tags:
        
        songs_list = get_songs("playlists/{}.m3u".format(msg))
        random.shuffle(songs_list)

        post = songs_list[0:n_songs]

        for song in post:
            try:
                audio_file = open(song, 'rb')
                bot.send_audio(message.chat.id, audio_file)
            except:
                bot.send_message(message.chat.id, "Ooops, I can't send track. Please wait.")

    elif len(args) == 3 and (args[1] == "and" or args[1] == "not"):
        
        class1, _, class2 = args
        if class1 in available_classes and class2 in available_classes:

            love_music_path = dirname(realpath(__file__)) + relative_path

            sys.path.append(love_music_path)
            chdir(love_music_path)

            from classifier import two_classes_relevant

            if args[1] == "and":
                relevant_songs = two_classes_relevant(class1, class2, 1)
            elif args[1] == "not":
                relevant_songs = two_classes_relevant(class1, class2, -1)
            
            song = random.choice(relevant_songs)
            
            artist, name = song[0].split(";")

            artist, name = artist.replace("_", " ").strip(), name.replace("_", " ").strip()

            bot.send_message(message.chat.id, "{} — {}".format(artist, name))
        else:
            bot.send_message(message.chat.id, warn())
    else:
        bot.send_message(message.chat.id, warn())


if __name__ == '__main__':
    bot.polling(none_stop=True)