import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import json

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.llms

app = Flask(__name__)

load_dotenv()

# 讀取環境變數中的金鑰
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("CHANNEL_SECRET")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

examples = [
    {
        "question": "你好嗎！",
        "answer": "主人, 我很好"
    },
    {
        "question": "今天禮拜幾?",
        "answer": "主人, 今天禮拜一"
    },
    {
        "question": "天氣好嗎！",
        "answer": "主人, 是的, 今天天氣確實不錯"
    }
]
example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"]
)

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
        # 取出文字的前兩個字元，轉換成小寫
        ai_msg = msg[:2].lower()
        reply_msg = ''
        # 取出文字的前兩個字元是 ai:
        if ai_msg == 'ai':
            # 只有在滿足條件時才回覆訊息
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[2:],
                max_tokens=256,
                temperature=0.5,
            )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response["choices"][0]["text"].replace('\n', '')
        else:
            reply_msg = msg

        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk, text_message)
    except:
        print('error')
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
