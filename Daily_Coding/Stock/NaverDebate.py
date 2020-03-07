from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import pickle
import urllib.parse
import pandas as pd

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'}

DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

def download_stock_codes(market=None, delisted=False):
    params = {'method': 'download'}

    if market.lower() in MARKET_CODE_DICT:
        params['marketType'] = MARKET_CODE_DICT[market]

    if not delisted:
        params['searchType'] = 13

    params_string = urllib.parse.urlencode(params)
    request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

    df = pd.read_html(request_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)

    return df

kosdaq_stocks = download_stock_codes('kosdaq')
kospi_stocks = download_stock_codes('kospi')

# Project 1,코스피 종목의 네이버 종목방 토론 데이터.
## 한 종목의 단위시간(30T)에 따른 댓글 수 df를 반환하는 함수. 

def one_item_simple(code,day,max_page):
    dates = []
    for page in range(1,max_page):
        url = 'https://finance.naver.com/item/board.nhn?code={}&page={}'.format(code,page)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        a = soup.select('td:nth-child(1) > span', {'class':'class="tah p10 gray03"'})
        date = list(map(lambda x : x.text,a))[2:]
        dates.extend(date)

        last_date = date[-1]
        last_date = datetime.strptime(last_date , '%Y.%m.%d %H:%M')
    
        if day > last_date:
            break
        else:
            continue
    df = pd.DataFrame({'date':dates})
    
    df.index = pd.to_datetime(df['date'])
    df = df.resample('30T').count()
    
    return df


# 단위시간에 따른 집적데이터 장전, 장중, 장후, 장말 4가지 범주로 재집적하는 함수. 
def time2cat(array):
    idx1 = []
    for i in array:
        
        H = str(i.hour)
        M = str(i.minute)
        if M == '0':
            M = '00'
        tmp = H+M
        idx1.append(int(tmp))
    
    idx = []
    for tmp in idx1:
        if tmp >= 1800:
            idx.append('장말')
        elif tmp >= 1600:
            idx.append('장후')
        elif tmp >= 900:
            idx.append('장중')
        elif tmp >= 730:
            idx.append('장전')
        else:
            idx.append('장말')
    
    return idx



'''
1. 장전 (시간외 종가: 07:30 ~ ~ 09:00
2. 장중 (정규 & 시간외 종가)09:00 ~ 16:00
3. 장후 (시간외 단일가): 16:00 ~ 18:00
4. 장말 18:00 ~ 익일 07:30
'''

## 가설 1
# 전날대비 장말 수치가 높은 종목들의 다음 영업일 변동한다. (3개월 정도??)

# 1-1 데이터 끌어오기.


dfs = []
for code in tqdm(kosdaq_stocks.종목코드):
    df = one_item_simple(code,datetime(2019, 10, 1, 0, 00),100)
    dfs.append(df)
'''    
name = '3개월_100page_코스닥_댓글수_30M_only'
with open('C:\GitHub\생활코딩\토론방_데이터\{}.pickle'.format(name),'wb') as f:
    pickle.dump(dfs, f, pickle.HIGHEST_PROTOCOL) 
'''    
# 4시간대로 재집적
dfs_re = []
for df in tqdm(dfs):
    df['시간대'] = time2cat(df.index)
    df['day'] = [str(x)[0:10] for x in df.index]
    df = df.groupby(['day','시간대']).sum()
    dfs_re.append(df)



# 전날대비 장말지수가 높은 종목을 일자별로 찾기.

dfs_agg = []

for idx,df in tqdm(enumerate(dfs_re)):
    try:
        tmp = df.loc[(slice(None),'장말'),:] + 1
        tmp2 = tmp.shift() 
        tmp = tmp / tmp2
        tmp.columns = [kosdaq_stocks.종목코드[idx]]
        dfs_agg.append(tmp)
    except:
        continue
    
dfs_agg = pd.concat(dfs_agg, axis = 1)

import numpy as np
dfs_agg = dfs_agg[np.isnan(dfs_agg).T.sum() < 1300]

dfs_agg = dfs_agg.T

rank5 = dfs_agg.iloc[:,-6].sort_values(ascending = False)[0:5]
tmp = dfs_agg.loc['091970',:] 
# 다음영업일 전날 종가 < 당일 시가 여부 확인.

# 전날 종가 < 당일 종가 여부 확인.

# 변동 확인.

def one_item(code,day,max_page):
    texts = []
    dates = []
    views = []
    goods = []
    hates = []

    for page in range(1,max_page):
        url = 'https://finance.naver.com/item/board.nhn?code={}&page={}'.format(code,page)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
    
    
        a = soup.find_all('td',{'class':'title'})
        text = list(map(lambda x : x.find('a')['title'], a))
        texts.extend(text)

        a = soup.select('td:nth-child(1) > span', {'class':'class="tah p10 gray03"'})
        date = list(map(lambda x : x.text,a))[2:]
        dates.extend(date)
        
        a = soup.select('td:nth-child(4) > span')
        view = list(map(lambda x : x.text,a))
        views.extend(view)

        a = soup.select('td:nth-child(5) > strong')
        good = list(map(lambda x : x.text,a))
        goods.extend(good)
        
        a = soup.select('td:nth-child(6) > strong')
        hate = list(map(lambda x : x.text,a))
        hates.extend(hate)        

        last_date = date[-1]
        last_date = datetime.strptime(last_date , '%Y.%m.%d %H:%M')
    
        if day > last_date:
            break
        else:
            continue
    df = pd.DataFrame({'date':dates,'text':texts, 'view':views,'good':goods,'hate':hates})
    
    return df
#content > div.section.inner_sub > table.type2 > tbody > tr:nth-child(3) > td:nth-child(1) > span
#content > div.section.inner_sub > table.type2 > tbody > tr:nth-child(3) > td:nth-child(4)
#chart_area > div.rate_info > table > tbody > tr:nth-child(1) > td.first > span
    

day = datetime(2020, 1, 2, 0, 00) 
max_page = 100

item_list = []
for code in tqdm(code_df.code):
    try:
        tmp = one_item(code,day,max_page)
    except:
        print(code)
        tmp = []
    item_list.append(tmp)
name = str(day)[0:-9] + '_' + str(datetime.now())[0:10]

with open('C:\GitHub\생활코딩\토론방_데이터\{}.pickle'.format(name),'wb') as f:
    pickle.dump(item_list, f, pickle.HIGHEST_PROTOCOL) # 하루하루 name 이터를 저장하쟈. 

def hit_ratio(df):
    df.index = pd.to_datetime(df['date'])
    df['cnt'] = 1
    df = df.resample('D')['cnt'].sum() / (df.resample('D')['cnt'].sum().shift() + 1)
    return df

def hit(df):
    df.index = pd.to_datetime(df['date'])
    df['cnt'] = 1
    df = df.resample('D')['cnt'].sum() 
    return df


df_hit_list = []
df_ratio_list = []

for num , _ in enumerate(item_list):
    df = item_list[num]
    df_ratio = hit_ratio(df)
    df_ratio = df_ratio.rename(code_df.code[num])
    df_ratio_list.append(df_ratio)
    
    df_hit = hit(df)
    df_hit = df_hit.rename(code_df.code[num])
    df_hit_list.append(df_hit)


df_ratio = pd.concat(df_ratio_list,axis = 1).T
df_view = pd.concat(df_hit_list, axis = 1).T

list(df_ratio)

target_day = df_ratio['2020-01-12 00:00:00'].sort_values(ascending = False)
'''
tmp = pd.concat([df_view,df2_view], axis = 1)

for df in tqdm(item_list):
    
    df_view = hit(df)
    try:
        hit_9_list.append(df_view['2020-01-09'])
    except:
        hit_9_list.append(0)    
    try:
        hit_10_list.append(df_view['2020-01-10'])
    except:
        hit_10_list.append(0)
    try:
        hit_11_list.append(df_view['2020-01-11'])
    except:
        hit_11_list.append(0)
    
    df_ratio = hit_ratio(df)
    try:
        ratio_9_list.append(df_ratio['2020-01-09'])
    except:
        ratio_9_list.append(0)
        
    try:
        ratio_10_list.append(df_ratio['2020-01-10'])
    except:
        ratio_10_list.append(0)
        
    try:
        ratio_11_list.append(df_ratio['2020-01-11'])
    except:
        ratio_11_list.append(0)
        
# 9일 대비 10일에 댓글 많은 종목 = 10일 화제종목, 10일 댓글수 / 9일 댓글수 + 1
        
ratio_df = pd.DataFrame({'ratio_10' :ratio_10_list, 'ratio_11' :ratio_11_list, 'view_10': hit_10_list,'view_11':hit_11_list})
'''