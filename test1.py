#!/usr/bin/env python3
import time
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext,  ConversationHandler, Filters, MessageHandler

TOKEN = '1566339524:AAFEe0n8V7V1NfrgF-djdiVlzk72dEKJ1rY'
URL = 'url'
USERS = []
GETURL = range(1)

class User:
    def __init__(self, name, rank, solve_c, time):
        self.name = name
        self.rank = rank
        self.solve_c = solve_c
        self.time = time

def url_to_html(url):
    req = requests.get(url)
    h = req.text
    html = BeautifulSoup(h, 'html.parser')
    return html

def html_to_tag_a(html):
    arr = []
    for line in html.find_all('a'):
        #print(line.string)
        arr.append(line.string)
    return arr

def html_to_tag_tr(html):
    tr = []
    for td in html.find_all('tr'):
        #print(td.get_text())
        tr.extend(td.get_text().split("\n"))
    #print(tr)
    return tr

def find_contest_name(html):
    return list(html.find_all('div'))[5].string

def find_remaining_time(html):
    return list(html.find_all('span'))[2].string

def count_questions(tag_a):
    counter = 1
    i = 6
    if tag_a[6].lower() == 'a':
        while len(tag_a[i+1]) == 1:
            if ord(tag_a[i+1]) == ord(tag_a[i])+1: 
                counter += 1
            else:
                break
            i += 1
    return counter

def find_users_name(tag_a, question_c):
    return tag_a[question_c + 6: -(2+question_c)]

def find_users_solve_time(tag_tr, users_name):
    solve_arr = []
    time_arr = []
    for u in users_name:
        #print(tag_tr.index(u))
        solve_arr.append(tag_tr[tag_tr.index(u) + 1])
        time_arr.append(tag_tr[tag_tr.index(u) + 2])
    return solve_arr, time_arr

def init_users():
    global URL
    html = url_to_html(URL)
    tag_a  = html_to_tag_a(html)

    question_c = count_questions(tag_a)

    users_name = find_users_name(tag_a, question_c)

    users_solve_time = find_users_solve_time(html_to_tag_tr(html), users_name)
    users_solve = users_solve_time[0]
    users_time = users_solve_time[1]

    # generating the object of users
    global USERS
    for i in range(len(users_name)):
        new_user = User(users_name[i], i+1, users_solve[i], users_time[i])
        USERS.append(new_user)

def update_standing():
    global USERS
    updated = []
    past_user = USERS
    print(past_user[1].name) # check if prev linen works

    init_users() # update

    for i in range(len(USERS)):
        if past_user[i].solve_c > USERS[i].solve_c:
            updated.append(USERS[i].name)
    return updated

# BOT FUNCTIONS
def add(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('enter the standing url')
    return GETURL

def get_url(update: Update, context: CallbackContext) -> int:
    global URL
    URL = update.message.text
    if not URL.startswith('https://open.kattis.com/contests/'):
        update.message.reply_text('only Kattis standings is supported.send a Kattis url again.')
        return GETURL
    else:
        update.message.reply_text('contest name is {}'.format(find_contest_name(url_to_html(URL))))
        init_users()
        return ConversationHandler.END

def done(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END

def report(update: Update, context: CallbackContext) -> None:
    global URL
    print(URL)
    r_time = find_remaining_time(url_to_html(URL))
    while r_time != '0:00:00':
        init_users()
        # sleep here
        time.sleep(60)
        updated = update_standing()
        print(updated)
        if len(updated) > 0:
            #update.message.reply_text('NEW SUBMISIONS!')
            for i in range(len(updated)):
                #update.message.reply_text('{} solved a problem!'.format(updated[i]))
                print('submision')
        r_time = find_remaining_time(url_to_html(URL))

def main() -> None:
    
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            GETURL:[MessageHandler(Filters.text & ~Filters.command, get_url)]
        },
        fallbacks=[CommandHandler('done', done)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('report', report))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()