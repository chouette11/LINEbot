from flask import Flask, request, abort

import re
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
    if (event.message.text == ('chrome拡張機能' or 'LINEbot' or '電卓アプリ') + ' 詳細'):
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text= event.message.text + 'の紹介です'),
             TextSendMessage(text=event.timestamp)])
    elif(re.search('.{1,9}\n\d', event.message.text) != None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    results = [ 
                        {   
                            "thumbnail_image_url": 'https://cs-cart.jp/wp-content/uploads/2020/05/chrome0001.png',
                            "title": 'chrome拡張機能',
                            "text": "chromeの拡張機能をJavaScriptとhtml,cssを用いて作成します！"
                        },
                        {
                            "thumbnail_image_url": 'https://fathomless-sierra-30007.herokuapp.com/static/images/line.png',
                            "title": 'LINEbot',
                            "text": "LINEbotをpythonを用いて作成します！"
                        },
                        {
                            "thumbnail_image_url": 'https://fathomless-sierra-30007.herokuapp.com/static/images/calculation.jpg',
                            "title": '電卓アプリ',
                            "text": "電卓のアプリをFlutterを用いて１から作成します！"
                        }
                    ]

                    columns = []
                    for column in results: 
                        columns.append(
                        CarouselColumn(
                            thumbnail_image_url=column['thumbnail_image_url'],
                            title=column['title'],
                            text=column['text'],
                            actions=[
                                MessageAction(
                                    label='詳細',
                                    text=column['title']  + ' 詳細'
                                ),
                                MessageAction(
                                    label='これにする！',
                                    text=column['title']
                                )
                            ]
                        ))
                    print("どうしてなん？")
                    cur.execute('SELECT id FROM users')
                    id = event.source.user_id
                    print(id)
                    print(type(id))
                    input = event.message.text.splitlines()
                    cur.execute('INSERT INTO users (id, name, grade) VALUES (%s, %s, %s)', (id, input[0], input[1],))
                    line_bot_api.reply_message(
                        event.reply_token,
                        [TextSendMessage(text='イベントを選択してください'),
                        TemplateSendMessage(
                            alt_text='Carousel template',
                            template=CarouselTemplate(
                                columns=columns
                            )
                        )]
                    )
                except:
                    return 'error'
    elif (event.message.text == 'chrome拡張機能' or event.message.text == "LINEbot" or event.message.text == "電卓アプリ"):
        pro_list = ['chrome拡張機能', 'LINEbot', '電卓アプリ']

        num = 0
        for pro in pro_list:
            if (event.message.text == pro):
                break
            num += 1
        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute('update users set program=340 where id=' + event.message.source.user_id)
                    cur.execute('SELECT * from product;')
                    a = cur.fetchone()
                    return a
                except:
                    mes = "exception"
                    return mes
    else:    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='例のように入力してください'))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)