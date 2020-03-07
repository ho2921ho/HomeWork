import datetime
import os
from bs4 import BeautifulSoup
import pandas as pd

s= str(datetime.datetime.now()) + 'TwoPoint_updated'
isfile = os.path.isfile('log.txt')

if isfile:
    with open('log.txt', 'a') as f: #파일이 있으면 마지막 행에 추가
        f.write(s+'\n')
else :
    with open('log.txt', 'w') as f: #파일이 없으면 log.txt 생성하고 입력
        f.write(s+'\n')

import pickle
from dateutil.parser import parse



import numpy as np

from tqdm import tqdm 
import warnings
warnings.filterwarnings("ignore")
## 코드를 입력하면 데이터 베이스에서 df를 반황하는 클라스

## 

# 종가가 m% 떨어졌을 때, d 영업일동안 한번이라도 n% 오르는 확률.
# m = 전일 종가 대비 종가 변화율
# n = 2% 상승 여부.
# d = 관측기간
now = datetime.datetime.now().date().strftime("%y%m%d_%H%M%S")

with open(r"C:\DATA\Stock_data\raw_data{}.pickle".format(now),"rb") as fr:
    dfs = pickle.load(fr)

with open(r"C:\DATA\Stock_data\kospi_stocks.pickle","rb") as fr:
    kospi_stocks = pickle.load(fr)

class TwoPoint:
    stock_cnt = 0
    event_cnt = 0
    
    def __init__(self,df,m,n,d,kind):
        self.df = df.copy()
        self.m = m
        self.n = n
        self.df['목표'] = self.df['종가']*((100+n)/100)
        for i in range(d):
            self.df['고가+'+str(i+1)] = self.df['고가'].shift(i+1)
        self.df['m'] =  (self.df['종가'] - self.df['종가'].shift(-1))*100/self.df['종가']
        self.df['n'] = self.df['목표'] < self.df.iloc[:,8:-1].max(axis = 1)
        self.df['날짜'] = [parse(x) for x in self.df['날짜']]
        self.df.set_index(['날짜'], inplace = True)
        self.kind = kind
        self.df['n2'] = self.df['목표'] < self.df['고가+1']
        
    def indx(self,mdf):
        if self.kind == 'DownUp':
            
            com_df = mdf[mdf['m'] < -self.m]
            
            if len(com_df.values) != 0:
                indx = round(sum(com_df['n'])/len(com_df.values),2)
            else:
                indx = np.nan
            
            cnt = len(mdf)
            event = sum(com_df['n'])
            return [indx, event, cnt]
        
        elif self.kind == 'AsolTwo':

            if len(mdf.values) != 0:
                indx = round(sum(mdf['n2'])/len(mdf.values),2)
            else:
                indx = np.nan
            
            cnt = len(mdf)
            event = sum(mdf['n2'])
            return [indx, event, cnt]
            
        
    def m1(self):
        mdf = self.df.loc[pd.date_range(end = self.df.index[0], periods=30)].dropna()
        return mdf

    def m3(self):
        mdf = self.df.loc[pd.date_range(end = self.df.index[0], periods=90)].dropna()
        return mdf

    def m6(self):
        mdf = self.df.loc[pd.date_range(end = self.df.index[0], periods=180)].dropna()
        return mdf
        
    def y1(self):
        mdf = self.df.loc[pd.date_range(end = self.df.index[0], periods=360)].dropna()
        return mdf
        self.indx_list.append((self.indx(mdf),len(mdf)))
    
    def to_indx_list(self, key = 'indx'):
        self.indx_list = []
        if key == 'indx':
            self.indx_list.append(self.indx(self.m1())[0])
            self.indx_list.append(self.indx(self.m3())[0])
            self.indx_list.append(self.indx(self.m6())[0])
            self.indx_list.append(self.indx(self.y1())[0])
            
        elif key == 'event':
            self.indx_list.append(self.indx(self.m1())[1])
            self.indx_list.append(self.indx(self.m3())[1])
            self.indx_list.append(self.indx(self.m6())[1])
            self.indx_list.append(self.indx(self.y1())[1])
            
        elif key == 'cnt':
            self.indx_list.append(self.indx(self.m1())[2])
            self.indx_list.append(self.indx(self.m3())[2])
            self.indx_list.append(self.indx(self.m6())[2])
            self.indx_list.append(self.indx(self.y1())[2])
            
        return self.indx_list
    
    def to_df(self):
        return self.df

# indx_df를 만들기 위한 과정.
kind = 'DownUp'
indx_df = dict()
for code in list(dfs.keys()):
    try:
        indx_df[code] = TwoPoint(dfs[code],3,2,5,kind).to_indx_list()
    except:
        print(code)

indx_df = pd.DataFrame(indx_df).T
indx_df.columns = ['1m','3m','6m','1y']

event_df = dict()
for code in list(dfs.keys()):
    try:
        event_df[code] = TwoPoint(dfs[code],3,2,5,kind).to_indx_list(key = 'event')
    except:
        print(code)

event_df= pd.DataFrame(event_df).T

indx_df = indx_df.merge(event_df,how = 'left',on = indx_df.index)

indx_df = indx_df.dropna()
indx_df = indx_df[indx_df.min(axis = 1) >= 0.8] 
indx_df = indx_df[indx_df[3] >= 10]
indx_df = indx_df.sort_values([0,1,2,3],ascending = False)

kospi_stocks['key_0'] = kospi_stocks['종목코드']
indx_df = indx_df.merge(kospi_stocks[['key_0','회사명']],how = 'left', on = 'key_0')


#
import requests
from bs4 import BeautifulSoup

m_s = []
for code in tqdm(indx_df['key_0']):
    url = 'https://finance.naver.com/item/sise.nhn?code='+code
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    m = soup.select('#_rate > span')[0].text.strip()
    m_s.append(m)

indx_df['m'] = m_s

name = 'TwoPoint_indx'
indx_df.to_csv('C:\DATA\Stock_data\TwoPoint\{}_{}.csv'.format(name,now))
    
# 모두 클래스화, m유연화, 데이터 갱신, 지표 저장.111770

