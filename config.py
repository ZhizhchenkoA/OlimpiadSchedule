from dotenv import load_dotenv
import os
from db import init_db
from db.init_db import Interaction

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(os.getenv('ADMIN_ID'))]
DATABASE = os.getenv('DRIVER_DB') + os.path.dirname(init_db.__file__) * int(os.getenv('IS_SQLITE')) + '/' * int(
    os.getenv('IS_SQLITE')) + os.getenv('DATABASE')
DATABASE = DATABASE.replace('\\', '/')

db = Interaction(DATABASE)
