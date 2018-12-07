from piazza_api import Piazza
import csv
import re
import string
import cmd

p = Piazza()
p.user_login()

def cleanhtml(raw_html):
  cleantext = re.sub(html_re, '', raw_html)
  return cleantext

def cleanpunc(text):
    return text.translate(punc_table)

def cleanpiazza(text):
    cleantext = re.sub(piazza_re, '', text)
    return cleantext

def clean(text):
    text = cleanpiazza(text)
    text = cleanhtml(text)
    text = cleanpunc(text)
    return text.lower()

## Initialize cleaners
piazza_re = re.compile('&.*?;')
punc_table = str.maketrans({key: None for key in string.punctuation})
html_re = re.compile('<.*?>')


eecs280 = p.network("jlco33n8mip65u")
filterfunction = lambda x : len(x['folders']) is not 0 and x['type'] == 'question'

try:
    LIMIT = int(input("How many posts do you want to process? (-1 to process all posts)\n"))
except Exception as e:
    LIMIT = -1

if (LIMIT > 0):
    posts = filter(filterfunction, eecs280.iter_all_posts(limit=LIMIT))
else:
    posts = filter(filterfunction, eecs280.iter_all_posts())

with open('f18_projects_exam_long.csv', mode='w') as train_file:
    writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['tag', 'content'])
    for post in posts:
        content = post['history'][-1]['content']
        cleaned = clean(content)
        tag = post['folders'][-1]
        writer.writerow([tag, cleaned])
