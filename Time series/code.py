
import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import OLS
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
from arch.unitroot import PhillipsPerron
import matplotlib.pyplot as plt
# 문제1
'''

	cann: Total employee hours of Canada
     canrgdp: GDP of Canada
	deun: Total employee hours of Germany
    espgdpvs: GDP of Spain
        espn: Total employee hours of Spain
    fdrrgdps: GDP of Germany
         fm2: M2 of USA
        fran: Total employee hours of France
     frargdp: GDP of France
       fygm3: 3-month T-bill rate
        gbrn: Total employee hours of United Kingdom
     gbrrgdp: GDP of United Kingdom
        gdpq: Quarterly GDP of United States
        itan: Total employee hours of Italy
     itargdp: GDP of Italy
    jpngnp85: GDP of Japan
        jpnn: Total employee hours of Japan
        lhem: Civil labor force total
       lpmhu: Employee hours in non agrigultural establishments in United States
       punew: CPI in United States
'''

df = pd.read_excel(r'C:\GitHub\HomeWork\Time series\galiaer1999.xls')
df = df.dropna()
plt.figure(figsize=(20,10))

plt.subplot(2, 4, 1)
np.log(df.cann).plot()
plt.title('Canada')

plt.subplot(2, 4, 2)
np.log(df.deun).plot()
plt.title('Germany')

plt.subplot(2, 4, 3)
np.log(df.espn).plot()
plt.title('Spain')

plt.subplot(2, 4, 4)
np.log(df.fran).plot()
plt.title('France')

plt.subplot(2, 4, 5)
np.log(df.gbrn).plot()
plt.title('U.K')

plt.subplot(2, 4, 6)
np.log(df.itan).plot()
plt.title('Italy')

plt.subplot(2, 4, 7)
np.log(df.jpnn).plot()
plt.title('Japan')

plt.subplot(2, 4, 8)
np.log(df.lpmhu).plot()
plt.title('U.S')

df.columns

for i in df.columns:
    if 'n' in i or 'lpmhu' in i:
        try:
            print(i)
            y2 = df.loc[:,i]
            y1 = np.diff(y2)
            y0 = np.diff(y1)
            
            print(adfuller(y2)[1])
            print(adfuller(y1)[1])
            print(adfuller(y0)[1])
        except:
            pass

c = np.log(df.canrgdp) - np.log(df.cann)
g = np.log(df.fdrrgdps) - np.log(df.deun)
s = np.log(df.espgdpvs) - np.log(df.espn)
f = np.log(df.frargdp) - np.log(df.fran)
uk = np.log(df.gbrrgdp) - np.log(df.gbrn) 
i = np.log(df.itargdp) - np.log(df.itan)
j = np.log(df.jpngnp85) - np.log(df.jpnn)
us = np.log(df.gdpq) - np.log(df.lpmhu)

plt.figure(figsize=(20,10))

plt.subplot(2, 4, 1)
c.plot()
plt.title('Canada')

plt.subplot(2, 4, 2)
g.plot()
plt.title('Germany')

plt.subplot(2, 4, 3)
s.plot()
plt.title('Spain')

plt.subplot(2, 4, 4)
f.plot()
plt.title('France')

plt.subplot(2, 4, 5)
uk.plot()
plt.title('U.K')

plt.subplot(2, 4, 6)
i.plot()
plt.title('Italy')

plt.subplot(2, 4, 7)
j.plot()
plt.title('Japan')

plt.subplot(2, 4, 8)
us.plot()
plt.title('U.S')

exp_list = [c,g,s,f,uk,i,j,us]

for i in exp_list:
    
        try:
          
            y2 = i
            y1 = np.diff(y2)
            y0 = np.diff(y1)
            
            print(adfuller(y2)[1])
            print(adfuller(y1)[1])
            print(adfuller(y0)[1])
            print('\n')
        except:
            pass
        
        
# 문제2
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

# 데이터 plotting
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

## 2-1 unit root test

### 미국의 물가 지수
y2 = us_cpi.iloc[:,0]
y1 = np.diff(y2)
y0 = np.diff(y1)

adfuller(y2)
adfuller(y1)
adfuller(y0)

PhillipsPerron(y2)
PhillipsPerron(y1)
PhillipsPerron(y0)

### 캐나다의 물가 지수
y2 = ca_cpi.iloc[:,0]
y1 = np.diff(y2)
y0 = np.diff(y1)

adfuller(y2)
adfuller(y1)
adfuller(y0)

PhillipsPerron(y2)
PhillipsPerron(y1)
PhillipsPerron(y0)

### 한국의 물가 지수
y2 = kr_cpi.iloc[:,0]
y1 = np.diff(y2)
y0 = np.diff(y1)

adfuller(y2)
adfuller(y1)
adfuller(y0)

PhillipsPerron(y2)
PhillipsPerron(y1)
PhillipsPerron(y0)

### usd_cad 환율
y2 = usd_cad.iloc[:,0]
y1 = np.diff(y2)
y0 = np.diff(y1)

adfuller(y2)
adfuller(y1)
adfuller(y0)

PhillipsPerron(y2)
PhillipsPerron(y1)
PhillipsPerron(y0)


### usd_krw 환율
y2 = usd_krw.iloc[:,0]
y1 = np.diff(y2)
y0 = np.diff(y1)

adfuller(y2)
adfuller(y1)
adfuller(y0)

PhillipsPerron(y2)
PhillipsPerron(y1)
PhillipsPerron(y0)


## 절대적 구매력 평가설
### 미국 캐나다
usd_cad.columns = ['usd cad exchange rate']
usd_cad.plot()

cpi_us_ca = ca_cpi / us_cpi
cpi_us_ca.columns = ['ca_cpi / us_cpi']
cpi_us_ca.plot()

resid1 = OLS(cpi_us_ca , usd_cad).fit().resid
print(adfuller(resid1)[1])
print(PhillipsPerron(resid1))

coint(cpi_us_ca , usd_cad)
### 미국 한국 
usd_krw.columns = ['usd krw exchange rate']
usd_krw.plot()

cpi_us_kr = kr_cpi / us_cpi
cpi_us_kr.columns = ['kr_cpi / us_cpi']
cpi_us_kr.plot()

resid1 = OLS(cpi_us_kr , usd_krw).fit().resid
print(adfuller(resid1)[1])
print(PhillipsPerron(resid1))

coint(cpi_us_kr , usd_krw)


## 상대적 구매력 평가.
## 두 국가의 인플레이션 차이와 환율의 변화율
### 데이터 변환

kr_dt = 100*(kr_cpi - kr_cpi.shift()) / kr_cpi
ca_dt = 100*(ca_cpi - ca_cpi.shift()) / ca_cpi
us_dt = 100*(us_cpi - us_cpi.shift()) / us_cpi

kr_dt = kr_dt.dropna()
ca_dt = ca_dt.dropna()
us_dt= us_dt.dropna()

us_ca_dt = 100*(usd_cad - usd_cad.shift()) / usd_cad
us_kr_dt = 100*(usd_krw - usd_krw.shift()) / usd_krw

us_ca_dt  = us_ca_dt .dropna()
us_kr_dt  = us_kr_dt .dropna()

### 미국 한국

us_kr = kr_dt - us_dt
us_kr.columns = ['kr_dt - us_dt']
us_kr.plot()

us_kr_dt.columns = ['usd krw exchange rate']
us_kr_dt.plot()

resid1 = OLS(us_kr, us_kr_dt).fit().resid
print(PhillipsPerron(resid1))
print(adfuller(resid1)[1])

coint(us_kr , us_kr_dt)

## 미국 캐나다

us_ca = ca_dt - us_dt
us_ca.columns = ['ca_dt - us_dt']
us_ca.plot()

us_ca_dt.columns = ['usd cad exchange rate']
us_ca_dt.plot()

resid1 = OLS(us_ca, us_ca_dt).fit().resid
print(PhillipsPerron(resid1))
print(adfuller(resid1)[1])


coint(us_ca , us_ca_dt)

## 문제3 
from johansen import coint_johansen

import pyeviews as evp
