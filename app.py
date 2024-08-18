import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    from scripts.config import SERVICE_CONF
    uvicorn.run("main:app", host=SERVICE_CONF.HOST, port=SERVICE_CONF.PORT)
