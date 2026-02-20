import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_NAME: str = os.getenv("DB_NAME", "expenses.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
    DEBUG: bool = os.getenv("DEBUG", False) == "True"