#!/usr/bin/env python3
import requests
import json
import time as TIME
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext,  ConversationHandler, Filters, MessageHandler

from random import seed
from random import randint

class User:
    def __init__(self, team, handles, rank, submissions_arr, last_sub_id):
        self.team = team #string
        self.handles = handles #string
        self.rank = rank #integer
        self.submissions_arr = submissions_arr #array
        self.last_sub_id = last_sub_id

users = []
problems = []
token = "1606858867:AAEJo9apComw6E0trqee4tZ7JVDCGZelv_I"
super_user_id = 297193627
text_not_allowed = "سلام😇\n کاربر {} متاسفانه هنوز امکان استفاده از بات برای بقیه فراهم نیست و فقط @idataaki به اون دسترسی داره.\n ممنون میشیم اگه پیشنهاد یا انتقادی داری به ما و اعضای انجمن ACM پیام بدی."
text_submission = "تیم {} سوال {} رو حل کرد😎🎉\n{}"
motivation = ["KEEP IT UP!", "YAAAY!", "WAY TO GO!", "ّFAR OUT!", "WELL DONE!", "COOL, MAN!", "BIG UP!", "HATS OFF TO YOU!"]
gif_id = ["https://media.giphy.com/media/l46C5wVFdiXBHSwi4/giphy.gif",
"https://media.giphy.com/media/zD2SpVI4vBLeo/giphy.gif",
"https://media.giphy.com/media/3o7ZeltXSmmz7Q5LCo/giphy.gif",
"https://media.giphy.com/media/l41YbnQ2qRrBesVag/giphy.gif",
"https://download1477.mediafire.com/vb5epp8lrlsg/xautl5ec69ebqx9/baa.mp4",
"https://download1521.mediafire.com/he8nxypg76bg/yqolauf0ja4zqti/ball.mp4",
"https://download1646.mediafire.com/mypa5u9e1bsg/nx73utsa8udigw4/re.mp4",
"https://download1644.mediafire.com/svplm0s3b5dg/tkgs7r0i9a9xasq/mad.mp4"]

# TODO:
# later if you accessed others, write a def to find contets_id

def get_json(api_url):
    req = requests.get(api_url)
    j = req.json()
    if j['status'] == 'OK':
        return j['result']
    else:
        return "I DONT KNOW WHAT TO DO YET"

def find_last_sub_id(handle):
    user_status_json = get_json("https://codeforces.com/api/user.status?handle={}&from=1&count=1".format(handle))
    return user_status_json[0]['id']

def init_users():
    global users
    users_hadles_file = open("user.txt", "r")
    handle_team = users_hadles_file.read().split()
    for h_t in handle_team:
        handle, team = h_t.split('/')
        users.append(User(team, handle, 0, [], find_last_sub_id(handle)))

def init_problems():
    global problems
    problem_file = open("problems.txt", "r")
    for p in problem_file.read().split('\n'):
        problems.append(p)

def find_user_by_team(team):
    global users
    for p in users:
        if p.team == team:
            return p

def find_user_by_handle(handle):
    global users
    for p in users:
        if p.handle[0] == handle:
            return p

# it returns an array of some last subs of the user
# TODO:
# what if it does not find the id?
def find_user_last_subs(user, user_status_json):
    for i in range(len(user_status_json)):
        if user.last_sub_id == user_status_json[i]['id']:
            return user_status_json[0:i]

def find_user_last_accepts(user, last_subs):
    global users, problems
    accepted = []
    if len(last_subs) > 0:
        try:
            for sub in last_subs:
                if sub['verdict'] == 'OK':
                    p_name = sub['problem']['name']
                    for p in problems:
                        if p == p_name:
                            accepted.append(p_name)
                            break
            users[users.index(user)].last_sub_id = last_subs[0]['id']
        except:
            pass
    return accepted


# BOT FUNCTIONS

def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != super_user_id:
        update.message.reply_text(text_not_allowed.format(update.message.from_user.full_name))
        

def report(update: Update, context: CallbackContext) -> None:
    global users
    if update.message.from_user.id == super_user_id:
        seed(1)
        init_users()
        init_problems()
        while True:
            TIME.sleep(5)
            for user in users:
                TIME.sleep(2)
                user_status_json = get_json("https://codeforces.com/api/user.status?handle={}".format(user.handles))
                last_subs = find_user_last_subs(user, user_status_json)
                print(last_subs)
                accepted = find_user_last_accepts(user, last_subs)
                if len(accepted) > 0:
                    for acc in accepted: 
                        print(user.team, 'solved', acc, '\n')
                        context.bot.send_document(update.effective_chat.id, gif_id[randint(0, 7)])
                        update.message.reply_text(text_submission.format(user.team, acc, motivation[randint(0, 8)]))
    else:
        update.message.reply_text(text_not_allowed.format(update.message.from_user.full_name))

def stck(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == super_user_id:
        context.bot.send_document(update.effective_chat.id, gif_id[randint(0, 7)])
        update.message.reply_text(text_submission.format("team", "problem", motivation[randint(0, 8)]))
        #context.bot.send_document(update.effective_chat.id, "https://download1477.mediafire.com/vb5epp8lrlsg/xautl5ec69ebqx9/baa.mp4")
        #context.bot.send_sticker(update.effective_chat.id, "CAACAgQAAxkBAAEJ8GRgdtTb_-OCePkICYr3SdNOptR96wACHwEAAuIN3CWpuwM3RXBP0B8E")
    else:
        update.message.reply_text(text_not_allowed.format(update.message.from_user.full_name))
        update.message.reply_text(motivation[randint(0, 7)])

def main() -> None:
    
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('report', report))
    dispatcher.add_handler(CommandHandler('sticker', stck))
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
