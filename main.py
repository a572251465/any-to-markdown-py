from fastapi import FastAPI
from dotenv import load_dotenv
from src.config import add_logging_config
from loguru import logger

load_dotenv(".env")
## 添加 logging 日志
add_logging_config()

app = FastAPI()