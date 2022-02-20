# TW-stock-wed-scrap 
This repository is for data scraping of TW stock information from Taiwan Stock Exchange and Taipei Exchange. 
I used requests, pandas, os, matplotlib, and plotly for this scraping project, and carculate GVI per share.

#＃Functions
### Get Book Value per Share
```Python
get_BVPS(year,season) # ex: get_BVPS(110, 1) ; year: Common Era - 1911  //python
``` 

### Get Earning per share
```Python
get_EPS(year,season) # ex: get_EPS(110, 1) ; year: Common Era - 1911  //python
``` 

### Get Stock information: return a csv with BVPS and EPS (result_si.csv)
```Python
get_stockinf(year,season) # ex: get_stockinf(110, 1) ; year: Common Era - 1911  //python
``` 

### Get Stock price: return a csv with stock price information (result_SE.csv)
```Python
get_stockprice(Date) # ex: get_stockinf(20200212) ; Date: Common Era+ Month+ date //python
``` 

### Get GVI: return a csv with stock information and growth value index (result_summary.csv)
```Python
get_GVI(year,season,Date) # ex: get_GVI(110,1,20210212) //python
``` 

## Data source
1. `[台灣證券交易所](https://www.twse.com.tw/zh/)`
2. `[證券櫃檯買賣中心](https://www.tpex.org.tw/web/index.php?l=zh-tw)`

## 免責聲明
僅供作為參考，不作為商業用途。若因資料不正確或其他原因等疏漏造成損失，本人不負任何法律責任。
