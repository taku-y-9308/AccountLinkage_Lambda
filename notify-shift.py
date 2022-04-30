import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
LINE_CHANNEL_ACCESS_TOKEN   = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET         = os.environ['LINE_CHANNEL_SECRET']
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)

def lambda_handler(event, context):
    logger.info(event)
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        LINE_BOT_API.reply_message(line_event.reply_token, TextSendMessage("こんにちは！"))

    LINE_HANDLER.handle(body, signature)
    return 0