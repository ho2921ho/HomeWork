#%% 방법 1

import random 
from selenium import webdriver
import time
import pandas as pd

# 강의 목차 데이터 전처리
idx = pd.read_csv(r'C:\Users\dongkeon\Desktop\목차.csv', engine = 'python')
weeks = ['차시 ' in x for x in idx.학습목차]

flag = 0
mark = []
for x in weeks:
    if x == True:
        flag += 1
        mark.append(flag)
    else:
        mark.append(flag)
        
idx['mark'] = mark
idx['weeks'] = weeks  
idx = idx[idx.weeks == False]

idx = idx['mark'].value_counts().sort_index()

# NH 로그인. -> 드라이버로 로그인해야함.


driver = webdriver.Chrome('C:/Users/dongkeon/Documents/chromedriver')
driver.get('http://www.edu-nhbank.com/')


'''
p_id = '19313068'
password = 'ha5216568**'

driver.find_element_by_xpath('//*[@id="p_id"]').send_keys(p_id)
driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
driver.find_element_by_xpath('//*[@id="flogin"]/div[2]/fieldset/ul/li[4]/a').click()
driver.find_element_by_xpath('//*[@id="flogin"]/div[2]/fieldset/ul/li[4]/a').click()
'''


for week, max_page in enumerate(idx):
    for page in range(1,max_page+1):
        page3 = '{0:03}'.format(page)
        page2 = '{0:02}'.format(page)
        url = 'http://class14.campus21.co.kr/cpclassroom/onlinestudy/246827/week{}/{}.asp?part=01{}01&page={}'.format(week+1,page3,page2,page3)
        driver.get(url)
        term = random.randrange(90,180)
        print(time)
        time.sleep(term)
    break

#%% 방법2
    
import win32api
import win32con
import time
import random 

pos = win32api.GetCursorPos() # 현재 마우스의 좌표

win32api.SetCursorPos(pos) # 좌표로 이동


def mouse_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


while True:
    term = random.randrange(1,30)
    print(term)
    time.sleep(term)
    mouse_click(1570, 621)

