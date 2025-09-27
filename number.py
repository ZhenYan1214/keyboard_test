import os
import threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, PostbackEvent
)
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# ===== LINE Bot 設定 =====
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '1wtaJqwC5T0KdZZkTeEm87wahZ8Cwjs+olv3sEjMyKfb8jvHcFiFUPdZ6ZWo/vuOSPTvrfMsWEKQIk1WRE6BM/TaJAC2cFFW7TgIiCGrlwRrO4NdZ9KVFHz8z+D4isfMStlnrAf8mPIGOqQzZSR+ewdB04t89/1O/w1cDnyilFU=')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '414e66e12afd781c391d0f57d702bbee')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ===== 暫存使用者輸入 =====
user_inputs = {}
user_inputs_lock = threading.Lock()

# ===== 建立血糖輸入 Flex Message =====
def build_flex(input_value="", completed=False):
    display_text = f"最終血糖值: {input_value}" if completed else (input_value if input_value else "請輸入數值")
    
    flex_json = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "paddingAll": "xl",
            "contents": [
                {
                    "type": "text",
                    "text": "🩺 血糖值輸入",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#2B5CE6",
                    "margin": "none"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#E1F5FE"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": display_text,
                            "align": "center",
                            "size": "xxl",
                            "weight": "bold",
                            "color": "#1565C0" if input_value else "#90CAF9",
                            "margin": "lg"
                        }
                    ],
                    "backgroundColor": "#F3F9FF",
                    "cornerRadius": "xl",
                    "paddingAll": "xl",
                    "margin": "lg",
                    "borderWidth": "2px",
                    "borderColor": "#BBDEFB"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "1", "data": "num=1"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "2", "data": "num=2"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "3", "data": "num=3"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "4", "data": "num=4"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "5", "data": "num=5"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "6", "data": "num=6"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "7", "data": "num=7"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "8", "data": "num=8"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "9", "data": "num=9"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "🗑 清除", "data": "clear"},
                                    "flex": 1,
                                    "style": "primary",
                                    "color": "#FF7043",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "0", "data": "num=0"},
                                    "flex": 1,
                                    "style": "secondary",
                                    "color": "#E3F2FD",
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {"type": "postback", "label": "✓ 完成", "data": "done"},
                                    "flex": 1,
                                    "style": "primary",
                                    "color": "#42A5F5",
                                    "height": "sm"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#FAFFFE"
            }
        }
    }
    return flex_json

# ===== 建立血糖管理室 Flex 選單 =====
def build_management_room():
    flex_json = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xl",
            "paddingAll": "xl",
            "contents": [
                {
                    "type": "text",
                    "text": "🏥 血糖管理室",
                    "weight": "bold",
                    "size": "xxl",
                    "align": "center",
                    "color": "#2B5CE6",
                    "margin": "none"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#E1F5FE"
                },
                {
                    "type": "text",
                    "text": "請選擇您需要的功能",
                    "size": "md",
                    "align": "center",
                    "color": "#64B5F6",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "lg",
                    "margin": "xl",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "postback", "label": "📊 開始血糖量測", "data": "action=measure"},
                            "style": "primary",
                            "color": "#42A5F5",
                            "height": "md"
                        },
                        {
                            "type": "button",
                            "action": {"type": "postback", "label": "📋 查看個人紀錄", "data": "action=record"},
                            "style": "secondary",
                            "color": "#E3F2FD",
                            "height": "md"
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#FAFFFE"
            }
        }
    }
    return flex_json

# ===== 首頁測試路由 =====
@app.route('/')
def home():
    return "LINE Bot 血糖管理系統運作正常 ✅"

# ===== Webhook 接收 LINE 事件 =====
@app.route("/callback", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ===== 處理文字訊息事件 =====
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if "血糖管理室" in text:
        flex_msg = FlexSendMessage(alt_text="血糖管理室選單", contents=build_management_room())
        line_bot_api.reply_message(event.reply_token, flex_msg)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「血糖管理室」開啟功能選單。"))

# ===== 處理 Postback 事件 =====
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    with user_inputs_lock:
        if data == "action=measure":
            flex_msg = FlexSendMessage(alt_text="輸入血糖值", contents=build_flex())
            line_bot_api.reply_message(event.reply_token, flex_msg)

        elif data == "action=record":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="這裡會顯示您的血糖紀錄（功能開發中）"))

        else:
            if user_id not in user_inputs:
                user_inputs[user_id] = ""

            if data.startswith("num="):
                user_inputs[user_id] += data.split("=")[1]
                reply_text = f"目前血糖值輸入: {user_inputs[user_id]}"
                flex_msg = FlexSendMessage(alt_text="輸入血糖值", contents=build_flex(user_inputs[user_id]))
            elif data == "clear":
                user_inputs[user_id] = ""
                reply_text = "已清除血糖值輸入"
                flex_msg = FlexSendMessage(alt_text="輸入血糖值", contents=build_flex())
            elif data == "done":
                final_value = user_inputs[user_id]
                reply_text = f"您輸入的血糖值是: {final_value}"
                flex_msg = FlexSendMessage(alt_text="最終血糖值", contents=build_flex(final_value, completed=True))
                user_inputs[user_id] = ""

            line_bot_api.reply_message(event.reply_token, [flex_msg, TextSendMessage(text=reply_text)])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
