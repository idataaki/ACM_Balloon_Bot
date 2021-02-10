#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '1566339524:AAFEe0n8V7V1NfrgF-djdiVlzk72dEKJ1rY'
#url = "https://open.kattis.com/contests/wjx8a3" # WRITE METHOD
#req = requests.get(url)

# This function replies with 'Hello <user.first_name>'
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

# getting url
def add(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('enter the standing url')


# Insert your token here
updater = Updater(TOKEN)

# Make the hello command run the hello function
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('add', add))

# Connect to Telegram and wait for messages
updater.start_polling()

# Keep the program running until interrupted
updater.idle()