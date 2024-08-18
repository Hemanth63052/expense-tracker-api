import uvicorn
from dotenv import load_dotenv

load_dotenv()

from scripts.config import SERVICE_CONF

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVICE_CONF.HOST, port=SERVICE_CONF.PORT)
