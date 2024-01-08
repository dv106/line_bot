import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import json

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI

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

llm = OpenAI()


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

        response = llm.predict(prompt.format(input=msg))
        reply_msg = response["choices"][0]["text"].replace('\n', '')
        
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk, text_message)
    except:
        print('error')
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
