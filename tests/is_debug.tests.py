import os
from dotenv import load_dotenv

load_dotenv(".custom.env")

def is_debug() -> bool:
    return  os.getenv("debug", "True") == "True" 

print(os.getenv("debug"))
print(type(os.getenv("debug")))
print(is_debug())