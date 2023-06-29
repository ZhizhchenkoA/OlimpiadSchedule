from dotenv import load_dotenv
import os
from db import init_db
from db.init_db import Interaction

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = eval(str(os.getenv('ADMIN_IDS')))
BOT_NAME = os.getenv('BOT_NAME')
DATABASE = os.getenv('DRIVER_DB') + os.path.dirname(init_db.__file__) * int(os.getenv('IS_SQLITE')) + '/' * int(
    os.getenv('IS_SQLITE')) + os.getenv('DATABASE')
DATABASE = DATABASE.replace('\\', '/')
BOT_ID = int(os.getenv('BOT_ID'))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')

db = Interaction(DATABASE)
