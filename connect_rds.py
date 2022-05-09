import sys,os,logging,pymysql

rds_host = os.environ['RDS_HOST']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

logger = logging.getLogger
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host,user=username,passwd=password,db=db_name,connect_timeout=5)

except pymysql.MySQLError as e:
    logging.error('ERROR: Unexpected error: Could not connect to MySQL instance.')
    logging.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    pass