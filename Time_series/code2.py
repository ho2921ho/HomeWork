
import warnings
warnings.simplefilter('ignore')

from arch import arch_model
from datetime import datetime
import pandas_datareader.data as wb


def compute_variance(df):
    am = arch_model(df['Close'], vol='Egarch', p=1, o=0, q=1, dist='Normal')
    res = am.fit(update_freq=5)
    forecasts = res.forecast()
    print(forecasts.variance.iloc[-3:])


start = datetime(1995,7,1)
end = datetime(2000,6,30)
 
ko = wb.DataReader('^KS11','yahoo',start,end)
ni = wb.DataReader('^N225','yahoo',start,end)
snp = wb.DataReader('^GSPC','yahoo',start,end)

compute_variance(ko)
compute_variance(ni)
compute_variance(snp)

start = datetime(2005,7,1)
end = datetime(2010,6,30)
 
ko = wb.DataReader('^KS11','yahoo',start,end)
ni = wb.DataReader('^N225','yahoo',start,end)
snp = wb.DataReader('^GSPC','yahoo',start,end)

compute_variance(ko)
compute_variance(ni)
compute_variance(snp)


