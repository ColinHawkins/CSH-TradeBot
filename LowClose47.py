#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import numpy as np
from matplotlib import pyplot as plt
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')
import yfinance as yf


# In[ ]:





# In[ ]:






# In[2]:


#load data into a pandas dataframe

START = datetime.datetime(2005, 1, 1)
END = datetime.datetime(2023, 1, 1)
YEARS = (END - START).days/ 365.25
investment_amount = 10000
PCT_THRESH = 20

data = yf.download('^GSPC', '2005-01-01', '2023-01-01')

data.head()


# In[3]:


#calculate benchmark return and balance
data['Return'] = data.Close / data.Close.shift(1)
data.Return.iat[0] = 1
data['Bench_Bal'] = investment_amount * data.Return.cumprod()

data.tail()


# In[4]:


#calculate benchmark drawdown
data['Bench_Peak'] = data.Bench_Bal.cummax()
data['Bench_DD'] = data.Bench_Bal - data.Bench_Peak

bench_dd = round(((data.Bench_DD / data.Bench_Peak).min() * 100), 2)

bench_dd


# In[5]:


#calculate additional columns for strategy

#daily range
data['Range'] = data.High - data.Low
#distance between close and daily low
data['Dist'] = abs(data.Close - data.Low)
#distance as % of range
data['Pct'] = (data.Dist / data.Range) * 100

data.tail()


# In[6]:


#identify entries and allocate trading fees
data['Long'] = data.Pct < PCT_THRESH


# In[7]:


#calculate system return and balance
data['Sys_Ret'] = np.where(data.Long.shift(1) == True, data.Return, 1)
data['Sys_Bal'] = (investment_amount * data.Sys_Ret.cumprod())

data.tail()


# In[8]:


#calculate system drawdown
data['Sys_Peak'] = data.Sys_Bal.cummax()
data['Sys_DD'] = data.Sys_Bal - data.Sys_Peak

sys_dd = round(((data.Sys_DD / data.Sys_Peak).min()) * 100, 2)

sys_dd


# In[ ]:





# In[9]:


#plot balance and calculate metrics

plt.plot(data.Bench_Bal)
plt.plot(data.Sys_Bal)

plt.show()

bench_return = round(((data.Bench_Bal[-1]/data.Bench_Bal[0]) - 1) * 100, 2)
bench_cagr = round(((((data.Bench_Bal[-1]/data.Bench_Bal[0])**(1/YEARS))-1)*100), 2)
sys_return = round(((data.Sys_Bal[-1]/data.Sys_Bal[0]) - 1) * 100, 2)
sys_cagr = round(((((data.Sys_Bal[-1]/data.Sys_Bal[0])**(1/YEARS))-1)*100), 2)

print(f'Buy/Hold Total return: {bench_return}%')
print(f'Buy/Hold CAGR: {bench_cagr}')
print(f'Buy/Hold DD: {bench_dd}%')
print(f'System Total return: {sys_return}%')
print(f'System CAGR: {sys_cagr}')
print(f'System DD: {sys_dd}%')


# In[ ]:





# In[ ]:





# In[ ]:




