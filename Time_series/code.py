import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def c(raw):
    tmp = []
    for t in raw :
        tmp.append(t.text) 
    return tmp

def c_raw(num,variables,soup):
    tmp = soup.find_all(variables[num].lower())
    return(tmp)

def c_s_f(variables,soup):
    c_s = []
    for i in tqdm(range(len(variables))):
        tmp = c_raw(i,variables,soup)
        tmp = c(tmp)
        c_s.append(tmp)    
    return c_s

def open_api_load(key,item,variables):
    start_t = 1
    end_t = 1
    sep = 1000
    
    url = 'http://openapi.seoul.go.kr:8088/{}/xml/{}/{}/{}/'.format(key,item,start_t,end_t)
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    end = int(soup.find('list_total_count').text)
    print(end)
    
    end_list = []
    for i in range(1000, end, sep):
        end_list.append(i)
    end_list.append(end)
    
    all_df = []
    for idx, i in tqdm(enumerate(end_list)):
        if idx != 0: 
            start = end_list[idx-1] + 1
            end = i
        else:
            start = 1
            end = i
        
        url = 'http://openapi.seoul.go.kr:8088/{}/xml/{}/{}/{}/'.format(key,item,start,end)
        print('{}% 완료'.format(round((end/end_list[-1])*100)))
       
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        df = c_s_f(variables,soup)
        df = pd.DataFrame(dict(zip(variables,df)))
        all_df.append(df)
    one_df = pd.concat(all_df)
    return one_df

# 점포수 데이터. 
store_df = open_api_load(key = '735a436859686f323132397045786574',
                         variables = ['STDR_QU_CD','TRDAR_SE_CD',
                                    'TRDAR_SE_CD_NM',
                                    'TRDAR_CD',
                                    'TRDAR_CD_NM',
                                    'SVC_INDUTY_CD',
                                    'SVC_INDUTY_CD_NM',
                                    'STOR_CO',
                                    'SIMILR_INDUTY_STOR_CO',
                                    'OPBIZ_RT',
                                    'OPBIZ_STOR_CO',
                                    'CLSBIZ_RT',
                                    'CLSBIZ_STOR_CO',
                                    'FRC_STOR_CO'],
                        item = 'VwsmTrdarStorQq')

# 매출 데이터
sales_df = open_api_load(key = '735a436859686f323132397045786574',
                         variables = ['STDR_QU_CD',
                                    'TRDAR_SE_CD',
                                    'TRDAR_SE_CD_NM',
                                    'TRDAR_CD',
                                    'TRDAR_CD_NM',
                                    'SVC_INDUTY_CD',
                                    'SVC_INDUTY_CD_NM',
                                    'THSMON_SELNG_AMT'],
                        item = 'VwsmTrdarSelngQq')

one_df = pd.concat(sales_df)
one_df.to_csv('sales_df.csv', encoding = 'ms949', index = False)

one_df = pd.concat(store_df)
one_df.to_csv('store_df.csv', encoding = 'ms949', index = False)

