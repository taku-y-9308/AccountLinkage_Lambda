from email import message
import sys,os,logging,psycopg2
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
    signature = event["headers"]["x-line-signature"]
    body = event["body"]
    with conn.cursor() as cur:
        cur.execute('select date,begin,finish,user_id,username from "ShiftManagementApp_shift" inner join "ShiftManagementApp_user" on "ShiftManagementApp_shift".user_id = "ShiftManagementApp_user".id;')
        conn.commit()
        results = cur.fetchall()
        message = ""
        for result in results:
            print(f"date:{result[0]} start:{result[1]} end:{result[2]} user_id:{result[3]} username:{result[4]}")
            message += f"date:{result[0]} start:{result[1]} end:{result[2]}"
    conn.commit()
    conn.close()

    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        LINE_BOT_API.reply_message(line_event.reply_token, TextSendMessage(message))

    LINE_HANDLER.handle(body, signature)
    return 0