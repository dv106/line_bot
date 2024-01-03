from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = 'uEM5HgKtoMZf3GsNDzLXKr3tPoqj7Swl6+LuqSeR68TaDknsQ3b08TBjQ7NMg2UJYo8OY7FLnw9Avxa2Tv9iSGR2ZYMonS67dRaOm8ZiN2AwPGLqM1OcqVOgeBXD2VubquiPQtBF0aJaLqFn8EpoYgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '30f45a97f96ef6acd7e3d27470fc55e5'

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
