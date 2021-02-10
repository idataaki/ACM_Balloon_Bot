from bs4 import BeautifulSoup
import requests

ar1 = ['a', 'b']
ar2 = "c\nd".split("\n")
ar1.extend(ar2)
print(ar1)


class users:
    def __init__(self, name, rank, solve_c, time, solve_arr):
        self.name = name
        self.rank = rank
        self.solve_c = solve_c
        self.time = time
        self.solve_arr = solve_arr

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
    print(tr)
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

def find_users_solve(tag_tr, users_name):
    solve_arr = []
    for u in users_name:
        #print(tag_tr.index(u))
        solve_arr.append(tag_tr[tag_tr.index(u) + 1])
    return solve_arr, "b"



html = url_to_html("https://open.kattis.com/contests/k4ornu")
tag_a  = html_to_tag_a(html)
question_c = count_questions(tag_a)
users_name = find_users_name(tag_a, question_c)
users_solve = find_users_solve(html_to_tag_tr(html), users_name)
print(users_solve[0])