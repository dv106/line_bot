import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import json


app = Flask(__name__)

load_dotenv()

# 讀取環境變數中的金鑰
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("CHANNEL_SECRET")
#openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = "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"

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

'''
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    # 在這裡加入 ChatGPT 的呼叫，取得回覆
    # chatgpt_reply = get_chatgpt_reply(user_message)
    chatgpt_reply = "Hello from ChatGPT!"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=chatgpt_reply))

def get_chatgpt_reply(user_message):
    # 使用 requests 函數向 ChatGPT 發送請求，取得回覆
    chatgpt_api_url = 'https://your-chatgpt-api-url.com'  # 將這裡替換為實際的 ChatGPT API URL
    response = requests.post(chatgpt_api_url, json={'user_message': user_message})
    
    if response.status_code == 200:
        chatgpt_reply = response.json().get('chatgpt_reply')
        return chatgpt_reply
    else:
        return "ChatGPT encountered an error."
'''
'''
@app.route("/callback", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'
'''

@app.route("/callback", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        # 取出文字的前五個字元，轉換成小寫
        ai_msg = msg[0].lower()
        reply_msg = ''
        # 取出文字的前五個字元是 hi ai:
        if ai_msg == 'h':
            line_bot_api.reply_message(tk,"ai test")
            # 將第六個字元之後的訊息發送給 OpenAI
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[0],
                max_tokens=256,
                temperature=0.5,
                )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response["choices"][0]["text"].replace('\n','')
        else:
            reply_msg = msg
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except:
        print('error')
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
