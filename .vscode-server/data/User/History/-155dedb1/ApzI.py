from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import os


app = Flask(__name__)

# 讀取 LINE BOT API 金鑰
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_BOT_API_KEY')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = f'你說了: {user_message}'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(port=5000)
