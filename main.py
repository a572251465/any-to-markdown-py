from fastapi import FastAPI
from dotenv import load_dotenv
from src.config import add_logging_config
from src.models import EnvEnumModel
from src.routes import mount_routes
from src.middlewares import binding_logging_funs
import os

load_dotenv(override=True, dotenv_path=".custom.env")
## 添加 logging 日志
add_logging_config()

app = FastAPI(
    version="0.0.1",
    title="web service",
    description="[any to markdown] web service",
    root_path=os.getenv(EnvEnumModel.root_prefix.value)
)

## 挂载 子页面的路由
mount_routes(app=app)
## 挂载 fastapi 中间件
binding_logging_funs(app=app)