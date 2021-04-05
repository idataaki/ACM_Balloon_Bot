from bs4 import BeautifulSoup, NavigableString
import requests
import difflib
import json
import time as t

users = []

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

def find_contest_name(html):
    return list(html.find_all('div'))[5].string

def find_remaining_time(html):
    return list(html.find_all('span'))[2].string

'''def find_users_solve_arr(): # PROBLEM: if is always false
    arr_2d = []
    arr_1d = []
    tr = str(html.find_all('tr'))
    tr_arr = tr[tr.find(users_name[0]):tr.find('<td colspan="{}"></td>'.format(len(users_name)))].split('\n')
    for t in users_solve:
        arr_1d.clear()
        counter = 0
        index = tr_arr.index('<td class="total table-min-wrap table-td-align-right">{}</td>'.format(t)) + 2
        for i in range(question_c):
            counter += 1
            if tr_arr[index + i] != '<td></td>':
                arr_1d.append(counter)
        arr_2d.append(arr_1d)
    print(arr_2d)
    return arr_2d'''

def init_users():
    html = url_to_html("https://open.kattis.com/contests/rh8cuo")
    tag_a  = html_to_tag_a(html)

    question_c = count_questions(tag_a)

    users_name = find_users_name(tag_a, question_c)

    users_solve_time = find_users_solve_time(html_to_tag_tr(html), users_name)
    users_solve = users_solve_time[0]
    users_time = users_solve_time[1]

    # generating the object of users
    global users
    for i in range(len(users_name)):
        new_user = User(users_name[i], i+1, users_solve[i], users_time[i])
        users.append(new_user)

def update_standing():
    global users
    updated = []
    past_user = users
    print(past_user[0].name) # check if prev linen works

    init_users() # update

    for i in range(len(users)):
        if past_user[i].solve_c > users[i].solve_c:
            updated.append(users[i].name)
    return updated

def chenges():
    #now = url_to_html("https://codeforces.com/api/contest.ratingChanges?contestId=566")

    #first with contest.raitingChanges find all handle and rank and then with the bottom address find all their
    #submissions and update it

    # use this https://codeforces.com/api/contest.status?contestId=1433
    # &handle=idataaki with all members handle to 
    # get all their submissions
    req = requests.get("https://codeforces.com/api/contest.status?contestId=1433&handle=idataaki")
    r = req.json()
    if r['status'] == 'OK':
        rr = r['result']
        for e in rr:
            print(e['author'], "\n")    
    

time = find_remaining_time(url_to_html("https://open.kattis.com/contests/rh8cuo"))
chenges()
'''while time != '0:00:00':
    init_users()
    # sleep here
    updated = update_standing()
    print(updated)
    if len(updated) > 0:
        #update.message.reply_text('NEW SUBMISIONS!')
        for i in range(len(updated)):
            #update.message.reply_text('{} solved a problem!'.format(updated[i]))
            print('submision')
    time = find_remaining_time(url_to_html("https://open.kattis.com/contests/rh8cuo"))'''