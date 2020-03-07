#time.py

import datetime
import os

os.getcwd()
s= datetime.datetime.now()
isfile = os.path.isfile('log.txt')

if isfile:
    with open('log.txt', 'a') as f: #파일이 있으면 마지막 행에 추가
        f.write(str(s)+'\n')
else :
    with open('log.txt', 'w') as f: #파일이 없으면 log.txt 생성하고 입력
        f.write(str(s)+'\n')