from selenium import webdriver
from qparser import ProgHub


def call_parse_n_time(n, driver_, lang):
    parse = ProgHub(driver_, lang)
    parse.parse()
    q = []
    for _ in range(n-1):
        q.append(parse.parse_question_page())
    return q


driver = webdriver.Chrome()
arr = call_parse_n_time(50, driver, 'python')
for x in arr:
   print(x, '\n')