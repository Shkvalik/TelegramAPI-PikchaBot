import os
import random
import time

from telebot import TeleBot, types

from config import BUTTON_NAMES
from token import TOKEN

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_DIR = os.    path.join(PROJECT_DIR, 'Files')


bot = TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    with open(os.path.join(IMAGES_DIR, 'Welcome.jpg'), 'rb') as sti:
        bot.send_photo(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for button_name in BUTTON_NAMES:
        buttons.append(types.KeyboardButton(button_name))
    buttons.append(types.KeyboardButton('Выйти 🚶'))
    markup.add(*buttons)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} ✌!\nЯ - {bot.get_me().first_name}, бот созданый для получения качественных пикч и поднятия твоего настроения🤪")
    bot.send_message(message.chat.id, "Выбери какую пикчу хочешь получить", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text in BUTTON_NAMES:
            button_config = BUTTON_NAMES[message.text]
            folder_name = button_config['image_dir']
            if button_config.get('send_photo'):
                with open(os.path.join(IMAGES_DIR, button_config['send_photo']), 'rb') as f:
                    bot.send_photo(message.chat.id, f)

            # bot.send_message(message.chat.id, f'Ищем в папке "{folder_name}"')
            send_waiting_message(message.chat.id)
            send_random_photo(message.chat.id, folder_name)
            bot.send_message(message.chat.id, 'Вот держи')

        elif message.text == 'Выйти 🚶':
            with open(os.path.join(IMAGES_DIR, 'Good_Bye.jfif'), 'rb') as f:
                bot.send_photo(message.chat.id, f)
            bot.send_message(message.from_user.id, 'Клавиатура убрана.', reply_markup=types.ReplyKeyboardRemove())

        else:
            bot.send_message(message.chat.id, 'Ты чё умный самый!? Используй команды')
            with open(os.path.join(IMAGES_DIR, 'animation.gif.mp4'), 'rb') as f:
                bot.send_video(message.chat.id, f)


def send_random_photo(chat_id, folder_name):
    all_files_in_directory = os.listdir(os.path.join(IMAGES_DIR, folder_name))
    file_name = random.choice(all_files_in_directory)
    with open(os.path.join(IMAGES_DIR, folder_name, file_name), 'rb') as f:
        bot.send_photo(chat_id, f)


def send_waiting_message(chat_id):
    bot.send_message(chat_id, 'Щас чёт поищем...')
    time.sleep(3)
    bot.send_message(chat_id, 'Чёт вот тут заволялось...')
    time.sleep(3)

if __name__ == '__main__':
    bot.polling(none_stop=True)
