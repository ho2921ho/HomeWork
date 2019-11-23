import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime
import numpy as np

# 데이터 전처리
## time_index 만들기 총 117개월
time_index = []

end = datetime.date(2019, 9, 1)
start = datetime.date(2010, 1, 1)    

while start <= end:
    time_index.append(start)
    start += relativedelta(months=1)
    
## 데이터 형식 통일
    
kr_cpi = pd.read_csv(r'C:\GitHub\HomeWork\Time series\KR_CPI.csv', engine = 'python')
us_cpi = pd.read_csv(r'C:\GitHub\HomeWork\Time series\US_CPI.csv', engine = 'python')    
ca_cpi = pd.read_csv(r'C:\GitHub\HomeWork\Time series\CAD_CPI.csv', engine = 'python')   

ca_cpi.columns = time_index
ca_cpi = ca_cpi.T
ca_cpi.columns = ['CPI']

kr_cpi.columns = time_index
kr_cpi = kr_cpi.T
kr_cpi.columns = ['CPI']

cpi = list(map(lambda x:x[0].split()[-1], us_cpi.values))
tmp = list(map(lambda x:x[0].split()[-2], us_cpi.values))

for idx, item in enumerate(tmp):
    if '13' in item:
        cpi.pop(idx)
        
us_cpi = pd.DataFrame(cpi)
us_cpi.index = time_index
us_cpi.columns = ['CPI']
us_cpi = us_cpi.astype('float')

usd_cad = pd.read_csv(r'C:\GitHub\HomeWork\Time series\USD_CAD.csv', engine = 'python')   
usd_krw = pd.read_csv(r'C:\GitHub\HomeWork\Time series\USD_KRW.csv', engine = 'python')   

usd_cad = usd_cad.iloc[::-1]
usd_krw = usd_krw.iloc[::-1]

usd_cad.index = time_index
usd_krw.index = time_index

usd_cad = usd_cad.iloc[:,1]
usd_cad = pd.DataFrame(usd_cad)

usd_krw = usd_krw.iloc[:,1]
usd_krw = pd.DataFrame(usd_krw)

usd_cad.plot()
usd_krw.plot()

cpi_us_ca = ca_cpi / us_cpi
cpi_us_kr = kr_cpi / us_cpi 

cpi_us_kr.plot()
cpi_us_ca.plot()

exp = usd_krw.iloc[:,0] * us_cpi.iloc[:,0] 
exp.plot()

kr_cpi.plot()
ca_cpi / us_cpi


## 상대적 구매력 평가.
## 두 국가의 인플레이션 차이와 환율의 변화률


## 문제1.

import pyeviews as evp
