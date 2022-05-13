import sys,os,logging,psycopg2

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
    with conn.cursor() as cur:
        cur.execute('select date,begin,finish,user_id,username from "ShiftManagementApp_shift" inner join "ShiftManagementApp_user" on "ShiftManagementApp_shift".user_id = "ShiftManagementApp_user".id;')
        conn.commit()
        results = cur.fetchall()
        for result in results:
            print(f"date:{result[0]} start:{result[1]} end:{result[2]} user_id:{result[3]} username:{result[4]}")
    conn.commit()
    conn.close()