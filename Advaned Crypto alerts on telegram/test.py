import requests
import json
from bob_telegram_tools.bot import TelegramBot
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('datasets/BTC.csv')

secrets_filename = 'tokens/id'
api_keys = {}
with open(secrets_filename, 'r') as f:
    api_keys = json.loads(f.read())


bot = TelegramBot(api_keys['token'], int(api_keys['user_id']))

plt.plot(df['Close'])

bot.send_plot(plt)

bot.clean_tmp_dir()

print('plot sucessfulyy sent')

just_url='https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=" is going in bearish squeeze and ADX values are"'.format(api_keys['token'],api_keys['user_id'])
requests.get(just_url)
print('Success')