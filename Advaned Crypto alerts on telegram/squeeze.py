import os, pandas
import plotly.graph_objects as go
import pandas_ta as ta
import requests
from bob_telegram_tools.bot import TelegramBot
import matplotlib.pyplot as plt
import json

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


secrets_filename = 'tokens/id'
api_keys = {}
with open(secrets_filename, 'r') as f:
    api_keys = json.loads(f.read())


bot = TelegramBot(api_keys['token'], int(api_keys['user_id']))



dataframes = {}

for filename in os.listdir('datasets'):
    symbol = filename.split(".")[0]
    
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue

    df['20sma'] = ta.sma(df['Close'],length=20)
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (1 * df['stddev'])
    df['upper_band'] = df['20sma'] + (1 * df['stddev'])
    
    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1)
    df['diff']=(df['upper_band']-df['lower_band'])/df['20sma']

    ADX=ta.adx(df['High'],df['Low'],df['Close'],length=14)
    RSI=ta.rsi(df['Close'],length=14)


    def tight_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    def above_keltner(df):
        return df['Open'] > df['upper_keltner']

    def is_consolidating(df):
        re_close=df[-10:]
        max_close= re_close['Close'].max()
        min_close=re_close['Close'].min()
        
        if min_close > (max_close*0.98):
            return True

    df['above_keltner']=df.apply(above_keltner,axis=1)

    df['tight_squeeze_on'] = df.apply(tight_squeeze, axis=1)

# if out of squeeze and dmp > dmn or dmp < dmn and adx < 20 then it  cannot be decided
# but if out o squeeze and dmp > dmn and adx > 20 then it is bullish
# and if out of squeeze and dmp < dmn and adx > 20 then it is bearish
    if is_consolidating(df):
        cons_url='https://api.telegram.org/bot{}/sendMessage?chat_id=&text="{} is consolidating"'.format(api_keys['token'],api_keys['user_id'],symbol)
        requests.get(cons_url)
        print("{} is consolidating".format(symbol))
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
        ax1.plot(df['Close'],color='b')

        bot.send_plot(plt)

        bot.clean_tmp_dir()

    


    if  df.iloc[-2]['tight_squeeze_on'] and not df.iloc[-1]['tight_squeeze_on'] and ADX.iloc[-1]['DMP_14'] > ADX.iloc[-1]['DMN_14']:
        tight_url='https://api.telegram.org/bot{}/sendMessage?chat_id={}&text="{} is going in bullish squeeze and ADX values are p{} and N{} and ADX=={}"'.format(api_keys['token'],api_keys['user_id'],symbol,ADX.iloc[-1]['DMP_14'],ADX.iloc[-1]['DMN_14'],ADX.iloc[-1]['ADX_14'])
        requests.get(tight_url)
        print("{} is going in bullish squeeze".format(symbol))
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)
        ax1.plot(df['Close'],color='b',alpha=0.3)
        ax1.plot(df['upper_band'],color='r')
        ax1.plot(df['lower_band'],color='r')
        ax1.plot(df['upper_keltner'],color='b')
        ax1.plot(df['lower_keltner'],color='b')
        ax2.plot(ADX['DMP_14'],color='b')
        ax2.plot(ADX['DMN_14'],color='r')
        ax2.plot(ADX['ADX_14'],color='y')
        ax2.axhline(20,linestyle='--',color='k',alpha=0.5)


        bot.send_plot(plt)

        bot.clean_tmp_dir()

        

    elif df.iloc[-2]['tight_squeeze_on'] and not df.iloc[-1]['tight_squeeze_on'] and ADX.iloc[-1]['DMP_14'] < ADX.iloc[-1]['DMN_14']:
        just_url='https://api.telegram.org/bot{}/sendMessage?chat_id={}&text="{} is going in bearish squeeze and ADX values are P{} N{} and ADX == {}"'.format(api_keys['token'],api_keys['user_id'],symbol,ADX.iloc[-1]['DMP_14'],ADX.iloc[-1]['DMN_14'],ADX.iloc[-1]['ADX_14'])
        requests.get(just_url)
        print("{} is going in bearish squeeze".format(symbol))
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)
        ax1.plot(df['Close'],color='b',alpha=0.3)
        ax1.plot(df['upper_band'],color='r')
        ax1.plot(df['lower_band'],color='r')
        ax1.plot(df['upper_keltner'],color='b')
        ax1.plot(df['lower_keltner'],color='b')
        ax2.plot(ADX['DMP_14'],color='b')
        ax2.plot(ADX['DMN_14'],color='r')
        ax2.plot(ADX['ADX_14'],color='y')
        ax2.axhline(20,linestyle='--',color='k',alpha=0.5)



        bot.send_plot(plt)

        bot.clean_tmp_dir()
        

    elif df.iloc[-1]['above_keltner'] and ADX.iloc[-1]['DMP_14'] > ADX.iloc[-1]['DMN_14']:
        just_url='https://api.telegram.org/bot{}/sendMessage?chat_id={}&text="{} is going in bullish keltner squeeze"'.format(api_keys['token'],api_keys['user_id'],symbol)
        requests.get(just_url)
        print("{} is crossing upper keltner band".format(symbol))

        plt.figure(figsize=(10,5))
        plt.plot(df['Close'],color='b',alpha=0.3)
        plt.plot(df['upper_keltner'],color='b')
        plt.plot(df['lower_keltner'],color='b')
        

        bot.send_plot(plt)

        bot.clean_tmp_dir()

        plt.figure(figsize=(10,5))
        plt.plot(ADX['DMP_14'],color='b')
        plt.plot(ADX['DMN_14'],color='r')

        bot.send_plot(plt)

        bot.clean_tmp_dir()



   
    else:
        print('Wait')


   
    dataframes[symbol] = df


