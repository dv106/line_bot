from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

# 讀取環境變數中的金鑰
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("CHANNEL_SECRET")

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
