from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(os.getenv('ADMIN_ID'))]
DATABASE = os.getenv("DATABASE")
