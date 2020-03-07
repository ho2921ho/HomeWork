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

# 데이터 가져오기.

def stock_info_crawl(code):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    df = pd.DataFrame()
    for page in range(1, 21):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    df = df.dropna()
    return df

dfs = []
for code in tqdm(kospi_stocks.종목코드):
    df = stock_info_crawl(code)
    dfs.append(df)

'''
name = '1p_20p_네이버_시종저고거_코스피'
with open('C:\GitHub\생활코딩\토론방_데이터\{}.pickle'.format(name),'wb') as f:
    pickle.dump(dfs, f, pickle.HIGHEST_PROTOCOL) 
'''    
stds = []
for df in dfs:
    std = df.종가.std()
    stds.append(std)

tmp = pd.DataFrame(stds)
tmp = tmp.reset_index()
tmp = tmp.sort_values(by = [0])

dfs[tmp.index[3]].종가.plot()
tmp.index[3]

kospi_stocks.loc[tmp.index[3],:]
