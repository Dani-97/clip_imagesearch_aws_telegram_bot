import configparser
import requests
import telebot

config = configparser.ConfigParser()
config.read('config.cfg')

bot = telebot.TeleBot(config['BOT']['token'], parse_mode='HTML')

@bot.message_handler(commands=['start', 'help'])
def show_help(message):
    response = 'This bot implements an image search engine using text queries to find the images.\n\n'
    response += 'To that end, the open-source CLIP model is used, that extracts the embeddings from text and images.\n\n'
    response += 'That part of the pipeline is run in a HuggingFace Space.\n\n'
    response += 'To use this bot, type <code>/query text_prompt</code> and wait a few seconds for the images to appear.\n\n'
    response += 'For example <code>/query Cat</code> will return 5 images of cats.'

    bot.reply_to(message, response)

@bot.message_handler(commands=['query'])
def process_query(message):
    endpoint = f'{config['CLIENT']['api_endpoint']}?{config['CLIENT']['parameter_key']}='
    splitted_message = message.text.split()
    if (len(splitted_message)>1):
        api_url_to_ask = endpoint + message.text.split()[1]

        bot.reply_to(message, 'Wait a few seconds for the images to appear...')
        results = requests.get(api_url_to_ask).json()
        for current_item in results:
            bot.reply_to(message, current_item)
    else:
        bot.reply_to(message, 'The query cannot be empty!')

bot.infinity_polling()
