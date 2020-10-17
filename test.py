import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
from collections import Counter
style.use('ggplot')

################################################
################################################get stock data
def save_100_tickers():
    resp = requests.get('https://finance.yahoo.com/most-active?offset=0&count=100')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'W(100%)'})
    tickers=[]
    for i in table.findAll('tr')[1:]:
        deta=i.findAll('td')[0].text
        tickers.append(deta)
    with open("100tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def get_stock_from_yahoo():

    with open("100tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    if not os.path.exists('100stock'):
        os.makedirs('100stock')

    start = dt.datetime(2019, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('100stock/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            #df = df.drop("Symbol", axis=1)
            df.to_csv('100stock/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


def stock_close_data():
    with open("100tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('100stock/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
        main_df.fillna(0,inplace=True)
    main_df.to_csv('100stock_closes.csv')
################################################
################################################

def visualize_data():
    df = pd.read_csv('100stock_closes.csv')
    df_corr = df.corr()
    #print(df_corr.head())
    df_corr.to_csv('100corr.csv')
    data1 = df_corr.values
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig1.colorbar(heatmap1)

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    # ax1.invert_yaxis()
    # ax1.xaxis.tick_top()
    # column_labels = df_corr.columns
    # row_labels = df_corr.index
    # ax1.set_xticklabels(column_labels)
    # ax1.set_yticklabels(row_labels)
    # plt.xticks(rotation=90)
    # heatmap1.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()


def next7days_stock():
    hm_days = 7
    df = pd.read_csv('100stock_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    for m in tickers:
        for i in range(1, hm_days+1):
            df['{}_{}d'.format(m, i)] = (df[m].shift(-i) - df[m]) / df[m]
            df.fillna(0, inplace=True)
            daf=df.iloc[:,100:]
    daf.to_csv('next7days_stock.csv')
    return tickers, daf


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.05
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


'''This will let us see the distributions of classes both in our dataset and in our algorithm's predictions'''

##Couter:dict subclass for counting hashable objects
def extract_featuresets(tickers):
    #tickers, daf = next7days_stock()
    #vals=[]
    for n in tickers:
        daf['{}_target'.format(n)] = list(map( buy_sell_hold,
                                               daf['{}_1d'.format(n)],
                                               daf['{}_2d'.format(n)],
                                               daf['{}_3d'.format(n)],
                                               daf['{}_4d'.format(n)],
                                               daf['{}_5d'.format(n)],
                                               daf['{}_6d'.format(n)],
                                               daf['{}_7d'.format(n)] ))
        vals = df['{}_target'.format(ticker)].values.tolist()
        str_vals = [str(i) for i in vals]
        #print('Data spread:', Counter(str_vals))

        df.fillna(0, inplace=True)
        df = df.replace([np.inf, -np.inf], np.nan)
        df.dropna(inplace=True)

        df_vals = df[[ticker for ticker in tickers]].pct_change()
        df_vals = df_vals.replace([np.inf, -np.inf], 0)
        df_vals.fillna(0, inplace=True)

        X = df_vals.values
        y = df['{}_target'.format(ticker)].values
    return X, y, df
    target_data=[daf['{}_target'.format(x)] for x in tickers]


from sklearn import svm, neighbors
from sklearn.model_selection import cross_validate
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def do_ml(ticker):

    X,y,df = extract_featuresets(tickers)
    X_train, X_test, y_train, y_test = cross_validate.train_test_split(X,
                                                        y,
                                                        test_size=0.25)