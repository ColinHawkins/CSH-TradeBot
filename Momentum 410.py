#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import numpy as np
import datetime
import matplotlib.pyplot as plt
get_ipython().system('pip install yfinance')
import yfinance as yf
import talib


# In[ ]:





# In[2]:


START = datetime.datetime(2005, 1, 1)
END = datetime.datetime(2023, 1, 1)
YEARS = (END - START).days / 365.25
investment_amount = 10000


# In[3]:


data = yf.download('BTC-USD', '2005-01-01', '2023-01-01')
data = data.drop(['High', 'Low', 'Volume', 'Adj Close'], 1)

data.head()


# In[4]:


data.tail()


# In[ ]:





# In[ ]:





# In[5]:


data['Return'] = data.Close / data.Close.shift(1)
data.Return.iat[0] = 1
data['Bench_Bal'] = investment_amount * data.Return.cumprod()

data.tail()


# In[6]:


bench_return = round(((data.Bench_Bal[-1] / data.Bench_Bal[0]) - 1) * 100, 2)
bench_cagr = round((((data.Bench_Bal[-1] / data.Bench_Bal[0]) ** (1/YEARS))-1) * 100, 2)

print(bench_return)
print(bench_cagr)


# In[7]:


data['Bench_Peak'] = data.Bench_Bal.cummax()

data['Bench_DD'] = data.Bench_Bal - data.Bench_Peak

bench_dd = round((((data.Bench_DD / data.Bench_Peak).min()) * 100), 2)

bench_dd


# In[8]:


#calculate momentum indicators

EMA_F = talib.MA(data['Close'], 50)
EMA_S = talib.MA(data['Close'], 200)
data['Fast_MA'] = EMA_F
data['Slow_MA'] = EMA_S

data.tail()


# In[9]:


#MA/Pricegraph
plt.plot(data.Close)
plt.plot(data.Fast_MA)
plt.plot(data.Slow_MA)

plt.show()


# In[10]:


#entries
data['Long'] = data.Fast_MA > data.Slow_MA

data.tail()


# In[11]:


#calculate system balance
data['Sys_Ret'] = np.where(data.Long.shift(1) == True, data.Return, 1)

data.tail()


# In[12]:


#calculate system balance
data['Sys_Bal'] = investment_amount * data.Sys_Ret.cumprod()

data.tail()


# In[13]:


#calculate metrics
sys_return = round(((data.Sys_Bal[-1] / data.Sys_Bal[0]) - 1) * 100, 2)
sys_cagr = round((((data.Sys_Bal[-1] / data.Sys_Bal[0]) ** (1/YEARS))-1) * 100, 2)


print(sys_return)
print(sys_cagr)


# In[14]:


#calculate drawdown
data['Sys_Peak'] = data.Sys_Bal.cummax()

data['Sys_DD'] = data.Sys_Bal - data.Sys_Peak

sys_dd = round((((data.Sys_DD / data.Sys_Peak).min()) * 100), 2)

print(sys_dd)


# In[15]:


plt.plot(data.Bench_Bal)
plt.plot(data.Sys_Bal)
plt.show()

print(f'Buy/Hold Total return: {bench_return}%')
print(f'Buy/Hold CAGR: {bench_cagr}')
print(f'Buy/Hold DD: {bench_dd}%')
print(f'System Total return: {sys_return}%')
print(f'System CAGR: {sys_cagr}')
print(f'System DD: {sys_dd}%')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




