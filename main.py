from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import psycopg2

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def get_connection():
    dsn = "host=ec2-3-230-199-240.compute-1.amazonaws.com port=5432 dbname=ddncsqqgstd7dp user=udydsahzfderba password=e44058d3925eea26d2ba930f7700b74631b63d5b44534bc13e5b246f1c31cbc9"
    return psycopg2.connect(dsn)

def get_response_message(mes_from):
    # "日付"が入力された時だけDBアクセス
    if mes_from=="日付":
        with get_connection() as conn:
            with conn.cursor(name="cs") as cur:
                try:
                    cur.execute('SELECT * FROM sample')
                    rows = cur.fetchall()
                    return cur.exists("sample")
                except:
                    mes = "exception"
                    return mes

    # それ以外はオウム返し
    return mes_from

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(get_response_message(event.message.text)))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)