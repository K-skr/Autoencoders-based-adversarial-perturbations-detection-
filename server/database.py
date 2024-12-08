import mysql.connector
from dotenv import load_dotenv
load_dotenv()

import os
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    database = os.getenv("DATABASE"),
    password=os.getenv("DB_PASSWORD")
)

