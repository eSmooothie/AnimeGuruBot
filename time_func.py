from datetime import datetime
import pytz

TIME_ZONE = pytz.timezone('Asia/Manila')

MORNING_QUOTE_TIME = 10
AFTERNOON_QUOTE_TIME = 15
EVENING_QUOTE_TIME = 21

def getCurrentTime():
  now = datetime.now(TIME_ZONE)

  return now
