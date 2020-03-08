import datetime
import os
import urllib.parse
import pandas as pd
import pickle
from tqdm import tqdm 

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

kospi_stocks = download_stock_codes('kospi')

name = 'kospi_stocks'
with open('C:\DATA\Stock_data\{}.pickle'.format(name),'wb') as f:
    pickle.dump(kospi_stocks, f, pickle.HIGHEST_PROTOCOL) 
    
# 데이터 가져오기.

def stock_info_crawl(code):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    df = pd.DataFrame()
    for page in range(1, 25):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    df = df.dropna()
    return df

dfs = dict()
for code in tqdm(kospi_stocks.종목코드):
    df = stock_info_crawl(code)
    dfs[code] = df

now = datetime.datetime.now().date().strftime("%y%m%d_%H%M%S")
name = 'raw_data' + now
with open('C:\DATA\Stock_data\{}.pickle'.format(name),'wb') as f:
    pickle.dump(dfs, f, pickle.HIGHEST_PROTOCOL) 


##
s= str(datetime.datetime.now()) + 'Stock_Data_saved'
isfile = os.path.isfile('log.txt')

if isfile:
    with open('log.txt', 'a') as f: #파일이 있으면 마지막 행에 추가
        f.write(s+'\n')
else :
    with open('log.txt', 'w') as f: #파일이 없으면 log.txt 생성하고 입력
        f.write(s+'\n')

