from linebot import LineBotApi
from linebot.models import TextSendMessage
import netifaces as ni
import logging
from datetime import datetime
import os

# 讀取 LINE BOT API 金鑰
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_BOT_API_KEY')

#CHANNEL_ACCESS_TOKEN = "uEM5HgKtoMZf3GsNDzLXKr3tPoqj7Swl6+LuqSeR68TaDknsQ3b08TBjQ7NMg2UJYo8OY7FLnw9Avxa2Tv9iSGR2ZYMonS67dRaOm8ZiN2AwPGLqM1OcqVOgeBXD2VubquiPQtBF0aJaLqFn8EpoYgdB04t89/1O/w1cDnyilFU="

# 設定日誌格式
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info('Program started.')

# 取得IP位址
ni.ifaddresses('enp0s8')
ip = ni.ifaddresses('enp0s8')[ni.AF_INET][0]['addr']
logging.info(f'Get IP address {ip}.')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
with open('example.log', 'r') as log_file:
    for line in log_file.readlines()[-2:]:
        line_bot_api.broadcast(TextSendMessage(text = line.strip()))


