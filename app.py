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

app = Flask(__name__)

line_bot_api = LineBotApi('Rpw5/5mrocA6BZAcLFlZajTvC2KuaKsM7tfufAQfN7/dx3W85lcEW2sBYAW3kvZCIIS6eSkvC+7DvrrYxoEwbzBD3ribugQzrczdBaAjfzHr+e/iGzdTb6AGm6NgzPf0BlMYmke9yB8RRW1VilSAJAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0a4c886abd721b5a8662799f5f116ea')


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
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()