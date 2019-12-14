import pandas as pd

inflation = pd.read_csv(r'C:\GitHub\HomeWork\Time_series\Data_inflation.csv', engine = 'python')

xt_1 = inflation.iloc[:,1][0:286]
yt_1 = inflation.iloc[:,2][0:286]
yt = inflation.iloc[:,2][1:287]

import pymc3 as pm
import numpy as np
np.random.seed(1000)
import matplotlib as mpl
import matplotlib.pyplot as plt

with pm.Model() as model: 
        # PyMC3의 모형은 with 문 안에서 사용된다.
    # 사전 확률 정의
    beta0 = pm.Normal('beta0', mu=0.5, sd=0.25)
    beta1 = pm.Normal('beta1', mu=0.5, sd=0.25)
    beta2 = pm.Normal('beta2', mu=0, sd=0.25)
    sigma = pm.InverseGamma('sigma', 10, 2)
    
    # 선형 회귀선 정의
    y_est = beta0 + beta1 * yt_1 + beta2 * xt_1 
    
    # 우도 정의 
    likelihood = pm.Normal('y', mu=y_est, sd=sigma, observed=yt)
    
    # 추정 과정
    start = pm.find_MAP()
      # 최적화를 사용하여 시작값 추정
    step = pm.NUTS(scaling= start)
      # MCMC 샘플링 알고리즘 인스턴스 생성
    trace = pm.sample(100, step, start=start, progressbar=False)
      # NUTS 샘플링을 사용하여 100개의 사후 샘플 생성

