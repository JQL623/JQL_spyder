#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 19:49:23 2020

@author: JQL_2020_4_15
"""
###############################
#####store data:pickle.dump(),pickle.load()

from bs4 import BeautifulSoup as soup
import pickle
import requests

url='http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
resp = requests.get(url)
data = soup(resp.text, 'lxml')
table = data.find('table', {'class': 'wikitable sortable'})
detail = table.findAll('tr')[1:]
tickers = []
for row in detail:
    detail_ticker = row.findAll('td')[0]
    ticker = detail_ticker.text
    tickers.append(ticker)
    return tickers
######### store data into a pickle file:pickle.dump(),read data from a pickle file: pickle.load()
with open("sp500tickers.pickle","wb") as f:
    pickle.dump(tickers,f)

with open("sp500tickers.pickle","rb") as f:
    aaa=pickle.load(f)

###############################
#####store data:joblib.dump(),joblib.load()
import joblib

joblib.dump(tickers,'sp500tickers.csv')


joblib.load('sp500tickers.csv')