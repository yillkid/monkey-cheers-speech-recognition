from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
def linebot_write(value):
    try:
        line_bot_api.broadcast(TextSendMessage(text = value))
    except Exception as e:
        print(e)
        pass
