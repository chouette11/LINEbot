from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, 
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage
)
import os
from linebot.models.actions import MessageAction, PostbackAction, URIAction
from linebot.models.template import ButtonsTemplate, CarouselColumn, CarouselTemplate

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
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute('INSERT INTO product (id, price, age, name) VALUES (%s, %s, %s, %s)', (3, 100, 20, a))
                cur.execute('SELECT * from product;')
                return 
            except:
                mes = "exception"
                return mes

    # それ以外はオウム返し
    return mes_from

@app.route("/aaa", methods=['POST'])
def aaa(event):
     line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage('aaaa'))


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
        TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cs-cart.jp/wp-content/uploads/2020/05/chrome0001.png',
                        title='chrome拡張機能',
                        text='chromeの拡張機能をJavaScriptとhtml,cssを用いて作成します！',
                        actions=[
                            MessageAction(
                                label='これにする！',
                                text='拡張機能'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://fathomless-sierra-30007.herokuapp.com/assets/images/java.png',
                        title='LINEbot',
                        text='LINEbotをpythonを用いて作成します！',
                        actions=[
                            MessageAction(
                                label='これにする！',
                                text='LINEbot'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ascii.jp/img/2020/02/26/2355326/o/7a804288de5f6df7.jpg',
                        title='電卓アプリ',
                        text='電卓のアプリを１からFlutterを用いて作成します！',
                        actions=[
                            MessageAction(
                                label='これにする！',
                                text='電卓'
                            )
                        ]
                    ),
                ]
            )
        )
    )



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)