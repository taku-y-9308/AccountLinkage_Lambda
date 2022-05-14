from email import message
import sys,os,logging,psycopg2,json
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

host = os.environ['HOST']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
dbname = os.environ['DB_NAME']
port = os.environ['PORT']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

try:
    conn = psycopg2.connect(f"dbname={dbname} user={username} password={password} host={host} port={port}")

except psycopg2.OperationalError as e:
    logging.error('ERROR: Unexpected error: Could not connect to PostgreSQL instance.')
    logging.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to heroku PostgreSQL succeeded")
def handler(event, context):
    logger.info(event)
    body_str = event["body"]
    body_dict = json.loads(body_str)
    logger.info(type(body_dict))
    line_user_id = body_dict["events"][0]["source"]["userId"]
    logger.info(f"line_user_id:{line_user_id}")
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    with conn.cursor() as cur:
        
        #シフトを収集
        cur.execute('select date,begin,finish,user_id,username from "ShiftManagementApp_shift" inner join "ShiftManagementApp_user" on "ShiftManagementApp_shift".user_id = "ShiftManagementApp_user".id;')
        results_shifts = cur.fetchall()
        logger.info(results_shifts)
        tomorrow_shift_lists = []
        for result_shift in results_shifts:
            tomorrow_shift_lists.append({
                "user" : result_shift[4],
                "date" : result_shift[0],
                "start" : result_shift[1],
                "end" : result_shift[2]
            })
        logger.info(tomorrow_shift_lists)
        
        #LINE登録しているユーザーを取得
        cur.execute('select * from line_bot;')
        result_notify_list = cur.fetchall()
        logger.info(result_notify_list)
        
        message = ""
    conn.commit()

    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        LINE_BOT_API.reply_message(line_event.reply_token, TextSendMessage(message))

    LINE_HANDLER.handle(body, signature)
    return 0