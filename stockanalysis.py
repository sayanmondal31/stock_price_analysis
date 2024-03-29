# -*- coding: utf-8 -*-
"""stockanalysis.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RRV7E-B1HWg11NnmA7T59gD4vXx_cuR9
"""

import pandas as pd
import datetime as dtm
import pandas_datareader.data as web
from pandas import Series,DataFrame

start = dtm.datetime(2010,1,1)
end = dtm.datetime(2017,1,11)

df = web.DataReader('AAPL','yahoo',start,end)

df.tail()

close_px = df['Adj Close']

mavg = close_px.rolling(window = 100).mean()

from matplotlib import style

import matplotlib as mpl

mpl.rc('figure',figsize=(8,7))
mpl.__version__

style.use('ggplot')

close_px.plot(label = 'AAPL')
mavg.plot(label = 'mavg')
plt.legend()

rets = close_px/close_px.shift(1)-1

rets.plot(label = 'Return')

dfcomp = web.DataReader(['AAPL', 'GE', 'GOOG', 'IBM', 'MSFT'],'yahoo',start=start,end=end)['Adj Close']

dfcomp.tail()

retscomp = dfcomp.pct_change()
corr = retscomp.corr()

corr.tail()

plt.scatter(retscomp.AAPL,retscomp.GE)
plt.xlabel('Returns AAPL')
plt.ylabel('Returns GE')

pd.plotting.scatter_matrix(retscomp, diagonal='kde', figsize=(10, 10));

plt.imshow(corr,cmap='hot',interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)),corr.columns)
plt.yticks(range(len(corr)),corr.columns)

plt.scatter(retscomp.mean(), retscomp.std())
plt.xlabel('Expected returns')
plt.ylabel('Risk')
for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (20, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

df.tail()

dfreg = df.loc[:,['Adj Close','Volume']]
dfreg['HL_PCT'] = (df['High']-df['Low']) / df['Close'] * 100.0
dfreg['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

dfreg.tail()

dfreg.fillna(value=-99999, inplace=True)

import math
forecast_out = int(math.ceil(0.01 * len(dfreg)))
forecast_col = 'Adj Close'
dfreg['label'] = dfreg[forecast_col].shift(-forecast_out)

import numpy as np
from sklearn import preprocessing
X = np.array(dfreg.drop(['label'], 1))

X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
y = np.array(dfreg['label'])
y = y[:-forecast_out]

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Linear regression
clfreg = LinearRegression(n_jobs=-1)
clfreg.fit(X_train, y_train)
# Quadratic Regression 2
clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
clfpoly2.fit(X_train, y_train)

# Quadratic Regression 3
clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
clfpoly3.fit(X_train, y_train)

print(clfreg.intercept_)

print(clfreg.coef_)

y_pred =clfreg.predict(X_test)

clfknn = KNeighborsRegressor(n_neighbors=2)
clfknn.fit(X_train, y_train)

confidencereg = clfreg.score(X_test, y_test)
confidencepoly2 = clfpoly2.score(X_test,y_test)
confidencepoly3 = clfpoly3.score(X_test,y_test)
confidenceknn = clfknn.score(X_test, y_test)

confidencereg

confidencepoly2

forecast_set = clfreg.predict(X_lately)
dfreg['Forecast'] = np.nan

#  Linear regression
last_date = dfreg.iloc[-1].name
last_unix = last_date
next_unix = last_unix + dtm.timedelta(days=1)

for i in forecast_set:
    next_date = next_unix
    next_unix += dtm.timedelta(days=1)
    dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)]+[i]
dfreg['Adj Close'].tail(500).plot()
dfreg['Forecast'].tail(500).plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

forecast_set = clfpoly2.predict(X_lately)
dfreg['Forecast'] = np.nan

#quadriatic regression 2
last_date = dfreg.iloc[-1].name
last_unix = last_date
next_unix = last_unix + dtm.timedelta(days=1)

for i in forecast_set:
    next_date = next_unix
    next_unix += dtm.timedelta(days=1)
    dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)]+[i]
dfreg['Adj Close'].tail(500).plot()
dfreg['Forecast'].tail(500).plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

forecast_set = clfpoly3.predict(X_lately)
dfreg['Forecast'] = np.nan

#quadriatic regreesion 3
last_date = dfreg.iloc[-1].name
last_unix = last_date
next_unix = last_unix + dtm.timedelta(days=1)

for i in forecast_set:
    next_date = next_unix
    next_unix += dtm.timedelta(days=1)
    dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)]+[i]
dfreg['Adj Close'].tail(500).plot()
dfreg['Forecast'].tail(500).plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

