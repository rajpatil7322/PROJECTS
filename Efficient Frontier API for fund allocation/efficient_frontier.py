import os
from datetime import date
from datetime import timedelta
import ccxt
import pandas as pd
from flask import Flask,jsonify
import numpy as np
import requests
import json


app=Flask(__name__)

@app.route('/test/<string:n>')
def test(n):
    symbol=n.split()
    return str(symbol)   




@app.route('/port/<string:n>')
def get_data(n):
    days_ago_to_fetch = 730
    def fetch_history(coin):
        endpoint_url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&limit={:d}".format(coin, days_ago_to_fetch)
        res=requests.get(endpoint_url)
        hist = pd.DataFrame(json.loads(res.content)['Data'])
        return hist['close']
    coins=n.split()
    main_df=pd.DataFrame()
    data={}
    for coin in coins:
        data[coin]=fetch_history(coin)
        main_df = pd.concat(data,
                axis = 1)

    
    return_stocks = main_df.pct_change()
    number_of_portfolios = 10000
    RF = 0

    portfolio_returns = []
    portfolio_risk = []
    sharpe_ratio_port = []
    portfolio_weights = []

    for portfolio in range (number_of_portfolios):
        weights=np.random.random_sample(len(coins))
        weights = weights / np.sum(weights)
        annualize_return = np.sum((return_stocks.mean() * weights))*365
        portfolio_returns.append(annualize_return)

        matrix_covariance_portfolio = (return_stocks.cov())*365
        portfolio_standard_deviation= np.sqrt(np.dot(weights.T,np.dot(matrix_covariance_portfolio, weights))) 
        portfolio_risk.append(portfolio_standard_deviation)

        sharpe_ratio = ((annualize_return- RF)/portfolio_standard_deviation)
        sharpe_ratio_port.append(sharpe_ratio)

        portfolio_weights.append(weights)

    portfolio_risk = np.array(portfolio_risk)
    portfolio_returns = np.array(portfolio_returns)
    sharpe_ratio_port = np.array(sharpe_ratio_port)

    porfolio_metrics = [portfolio_returns,portfolio_risk,sharpe_ratio_port, portfolio_weights] 
    portfolio_dfs = pd.DataFrame(porfolio_metrics)
    portfolio_dfs = portfolio_dfs.T
    portfolio_dfs.columns = ['Port Returns','Port Risk','Sharpe Ratio','Portfolio Weights']


    for col in ['Port Returns', 'Port Risk', 'Sharpe Ratio']:
        portfolio_dfs[col] = portfolio_dfs[col].astype(float)

    #portfolio with the highest Sharpe Ratio
    Highest_sharpe_port = portfolio_dfs.iloc[portfolio_dfs['Sharpe Ratio'].idxmax()]
    #portfolio with the minimum risk 
    min_risk = portfolio_dfs.iloc[portfolio_dfs['Port Risk'].idxmin()]


    dist=Highest_sharpe_port['Portfolio Weights']
    return {coins[i]: dist[i] for i in range(len(coins))}   



  

if __name__ =="__main__":
    app.run(debug=True)