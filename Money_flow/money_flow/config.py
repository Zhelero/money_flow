import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.DB_NAME: str = os.getenv("DB_NAME", "expenses.db")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
        self.DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


config = Config()