# -*- coding: utf-8 -*-
#created by 7/1/2020
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt
style.use('ggplot')

stock=pd.read_csv('GC=F.csv')
stock1=pd.read_csv('NQ=F.csv')

xx = stock.drop(columns=['Date'])
xx.corr()

stock_correlation=pd.DataFrame.corrwith(stock, stock1, axis=0, drop=False, method='pearson')
aaa=stock.corr(method='pearson')

a1 = stock1.set_index('Date')
a2 = a1.reset_index()

from os import path,mkdir,getcwd,chdir
if path.exists('test.py'):
    print('Yes')
elif not path.exists('test.py'):
    print('No')

my_path='/Users/jq/JQL_all_spyder/JQL_stock'
mkdir(my_path+'/'+'bbbbbbbbb')
next_path=my_path+'/'+'bbbbbbbbb'
for n in range(3):
    plt.savefig(next_path+'/my_fig'+str(n))


import glob
glob.glob(next_path+'/'+'*.png')











