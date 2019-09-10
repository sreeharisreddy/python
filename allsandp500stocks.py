# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:35:10 2019

@author: sreeharis
"""

import bs4 as bs 
#beautiful soup is the library to parse html
import pickle
import requests
import os
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

def save_sp500_tickers(url,cssclass):
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text,"lxml")
    table = soup.find('table',{'class':cssclass})
    tickers = []
   
    for row in table.findAll('tr')[1:]:   
      ticker = row.findAll('td')[0].text.replace("\n","")
      tickers.append(ticker)
      
    with open("D:\pythonexamples/sp500.pickle","wb") as f:
      pickle.dump(tickers,f)   
    return tickers
  
def getsp500():
  return save_sp500_tickers('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',"wikitable sortable")

#save_sp500_tickers('https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9',"tbldata14 bdrtpg")

#df = pd.read_csv("D:\pythonexamples\ind_niftynext50list.csv")
#print(df['Symbol'])

def getDataFromYahoo(reload_sp500=False):
  if reload_sp500:
    tickers = getsp500()
  else:
    with open("D:\pythonexamples/sp500.pickle","rb") as f:
      tickers = pickle.load(f)
      #print(tickers)
    if not os.path.exists("D:\pythonexamples/data/sp500"):
        os.makedirs("D:\pythonexamples/data/sp500")

    start = dt.date(2018,1,1)
    end = dt.date(2019,9,6)
    print(tickers)
    for ticker in tickers:
      try:
        if not os.path.exists("D:\pythonexamples/data/sp500/{}.csv".format(ticker)):
          print("Downloading................{}{}{}".format(ticker,start,end))
          df = web.DataReader(ticker,'yahoo',start,end,pause=0.)
          df.to_csv("D:\pythonexamples/data/sp500/{}.csv".format(ticker))
        else:
          print("Already have {} ".format(ticker))
      except:
          print("Not able to read {}".format(ticker))          
     
#getDataFromYahoo(False)

def compile_data():
    with open("D:\pythonexamples/sp500.pickle","rb") as f:
      tickers = pickle.load(f)
      
    main_df=pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        if os.path.exists("D:\pythonexamples/data/sp500/{}.csv".format(ticker)):
          df = pd.read_csv("D:\pythonexamples/data/sp500/{}.csv".format(ticker))
          df.set_index('Date',inplace=True)
          df.rename(columns = {'Adj Close':ticker}, inplace=True)         
          df.drop(['High','Low','Open','Close','Volume'], 1, inplace=True)     
          
          if main_df.empty:
              main_df = df
          else:
              main_df = main_df.join(df,how='outer')
              
          if count % 10 == 0:
              print (count)
    print(main_df.head())
    main_df.to_csv('D:\pythonexamples/sp500_joined_closes.csv')

    
#compile_data()

def vizualize_data():
  df = pd.read_csv('D:\pythonexamples/sp500_joined_closes.csv')
#  df['AAPL'].plot()
#  plt.show()
  
  df_corr = df.corr()
  print(df_corr.head())
  
  data = df_corr.values
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)
  
  heatmap = ax.pcolor(data,cmap=plt.cm.RdYlGn)
  fig.colorbar(heatmap)
  ax.set_xticks(np.arange(data.shape[1])+0.5,minor=False)
  ax.set_yticks(np.arange(data.shape[0])+0.5,minor=False)
  ax.invert_yaxis()
  ax.xaxis.tick_top()
  
  column_labels = df_corr.columns
  row_labels = df_corr.index
  ax.set_xticklabels(column_labels)
  ax.set_yticklabels(row_labels)
  plt.xticks(rotation=90)
  heatmap.set_clim(-1,1)  #clim is the color limit  positive is +1 and negative is -1
  plt.tight_layout()
  plt.show()
  
  
vizualize_data()
