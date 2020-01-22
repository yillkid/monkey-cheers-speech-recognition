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
handler = WebhookHandler('CHANNEL_SECRET')

line_bot_api.push_message('USER_ID', TextSendMessage(text='Hello World!'))
