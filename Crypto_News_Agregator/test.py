from datetime import timedelta, datetime
from dateutil import parser
from pprint import pprint
from time import sleep
import requests
import feedparser


BOT_TOKEN = '1932485181:AAGZ1x5X2PloIDYP-9PRjsJIGKIksoO1MOI'
CHANNEL_ID = '-1001545160460'
FEED_URL = 'http://www.reddit.com/r/python/.rss'

def send_message(message):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}')

d = feedparser.parse('https://cryptoquant.com/quicktake')

print(d.headers)