from pydantic import Field
from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv
load_dotenv()

class __Services(BaseSettings):
    PORT: int = Field(default=9182, validation_alias="service_port")
    HOST: str = Field(default="0.0.0.0", validation_alias="service_host")

class __SQLConf(BaseSettings):
    SQL_URI: str
    USER_DETAILS_DB: str = Field(default="user_details", validation_alias="USER_DETAILS_DB")
    CATEGORIES_DB: str = Field(default="categories", validation_alias="CATEGORIES_DB")
    TRANSACTION_DB: str = Field(default="transaction", validation_alias="TRANSACTION_DB")

class __API_DOCS_CONF(BaseSettings):
    SW_OPENAPI_URL: str = Field(default="/openapi.json")
    SW_DOCS_URL: str = Field(default="/docs")
    RE_DOCS_URL: str = Field(default="/redocs")
    SECURE_ACCESS: bool = Field(default=True)

class __ENCRYPTION_CONF(BaseSettings):
    FERNET_KEY: ClassVar[bytes] = b'Wz0n4anWWGF1JNShLgbryoauBea3XAB72qw6B0K2V5I='


SERVICE_CONF = __Services()
SQL_CONF = __SQLConf()
API_CONF = __API_DOCS_CONF()
ENCRY_DECRY_CONF = __ENCRYPTION_CONF()

__all__ = ["SERVICE_CONF", "SQL_CONF", "API_CONF", "ENCRY_DECRY_CONF"]
