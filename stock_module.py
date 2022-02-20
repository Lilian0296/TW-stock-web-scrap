#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px 


# In[6]:


# Book value per share
def get_BVPS(year,season): # 110,1
    url='https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    payload_1={'encodeURIComponent': '1','step': '1','firstin':'1','off': '1','isQuery':'Y', 'TYPEK': 'sii','year': year,'season': season}
    payload_2={'encodeURIComponent': '1','step': '1','firstin':'1','off': '1','isQuery':'Y', 'TYPEK': 'otc','year': year,'season': season}
    res1 = requests.post(url, data = payload_1)
    res2 = requests.post(url, data = payload_2)
    data1=pd.read_html(res1.text)
    data2=pd.read_html(res2.text)
    ID=[]
    Name=[]
    Price_value=[]
    for i in range(1,len(data1)):
        ID.extend(list(data1[i]['公司代號']))
        Name.extend(list(data1[i]['公司名稱']))
        Price_value.extend(list(data1[i]['每股參考淨值']))
    for i in range(1,len(data2)):
        ID.extend(list(data2[i]['公司代號']))
        Name.extend(list(data2[i]['公司名稱']))
        Price_value.extend(list(data2[i]['每股參考淨值']))
    df1= pd.DataFrame(list(zip(ID,Name,Price_value)), columns = ['ID','Name','Price_value'])
    return df1


# In[7]:


# Earning per stock
def get_EPS(year,season): # 110,1
    url='https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    payload_1={'encodeURIComponent': '1','step': '1','firstin':'1','off': '1','isQuery':'Y','TYPEK': 'sii','year': year,'season': season}
    payload_2={'encodeURIComponent': '1','step': '1','firstin':'1','off': '1','isQuery':'Y','TYPEK': 'otc','year':year,'season': season}
    res1 = requests.post(url, data = payload_1)
    res2 = requests.post(url, data = payload_2)
    data1=pd.read_html(res1.text)
    data2=pd.read_html(res2.text)
    ID=[]
    Name=[]
    EPS=[]
    for i in range(1,len(data1)):
        ID.extend(list(data1[i]['公司代號']))
        Name.extend(list(data1[i]['公司名稱']))
        EPS.extend(list(data1[i]['基本每股盈餘（元）']))
    for i in range(1,len(data2)):
        ID.extend(list(data2[i]['公司代號']))
        Name.extend(list(data2[i]['公司名稱']))
        EPS.extend(list(data2[i]['基本每股盈餘（元）']))
    df= pd.DataFrame(list(zip(ID,Name,EPS)), columns = ['ID','Name','EPS'])
    df.set_index("ID" , inplace=True)
    return df


# In[9]:


def get_stockinf(year,season): 
    df=get_EPS(year,season)
    df1=get_BVPS(year,season)
    frame=df.merge(df1,how='left')
    frame['ID']= frame['ID'].astype(str)
    frame.to_csv('result_si.csv')
    return frame


# In[1]:


def get_stockprice(Date): #Date:20210410
    TWSE_URL = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date='
    search_date1=str(Date)
    resp_1=requests.get(TWSE_URL+ search_date1 + '&type=ALL')
    stock_price_1=resp_1.json()
    sp1=pd.DataFrame(stock_price_1['data9'],columns=['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價','收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比'])
    TPEX_URL='https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d='
    search_date2=str(int(search_date1[0:4])-1911)+'/'+str(search_date1[4:6])+'/'+str(search_date1[6:9])
    resp_2=requests.get(TPEX_URL+ search_date2 + '&s=0,asc,0')
    stock_price_2=resp_2.json()
    sp2=pd.DataFrame(stock_price_2['aaData'],columns=['證券代號','證券名稱','收盤價','漲跌(+/-)','開盤價','最高價','最低價','均價','成交股數','成交金額','成交筆數','最後揭示買價','最後揭示買量(千股）','最後揭示賣價','最後揭示賣量(千股）','發行股數','次日參考價','次日漲停價','次日跌停價'])
    sp1_data=sp1
    sp2_data=sp2
    frames=[sp1_data,sp2_data]
    result_sp = pd.concat(frames)
    result_sp=result_sp.rename(columns={'證券代號':'ID'})
    result_sp['ID']= result_sp['ID'].astype(str)
    result_sp['收盤價']=pd.to_numeric(result_sp['收盤價'],errors='coerce')
    result_sp.to_csv('result_SE.csv') #SE 證交所
    return result_sp


# In[2]:


def get_GVI(year,season,Date): #year:民國 ex:110 ; Year:西元
    result_si=get_stockinf(year,season)
    result_sp=get_stockprice(Date)
    result = pd.merge(result_si,result_sp, on="ID", how="inner",indicator=True)
    result['ROE']=result['EPS']/result['Price_value']
    result['PBR']=result['收盤價']/result['Price_value']
    result['GVI']=(1/result['PBR'])*(1+result['ROE'])**5
    result['Rank']=result['GVI'].rank(method='max')
    result=result.sort_values(by=['GVI'],ascending=False)
    result.to_csv('result_summary.csv')
    plot=px.scatter(result,x='ROE', y='PBR',log_y=True,range_y=[0.01, 100],text='Name')
    plot.show()
    return result.head(50)
    return plot


# In[ ]:





# In[ ]:





# In[ ]:




