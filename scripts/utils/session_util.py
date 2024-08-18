import datetime
from sqlalchemy import MetaData, create_engine, Engine, TIMESTAMP
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import Session, DeclarativeBase
from scripts.config import SQL_CONF

class Base(DeclarativeBase):
    """
    Base class for all database models.
    """

    type_annotation_map = {datetime.datetime: TIMESTAMP(timezone=True)}

class SessionUtil:
    def __init__(self):
        self.user_engines = {}
        self.database_uri = SQL_CONF.SQL_URI

    def get_session(self, database: str, metadata: MetaData = None) -> Session:
        engine = self._get_engine(database=database, metadata=metadata)
        return Session(
            bind=engine,
            autocommit=False,
            autoflush=False,
            future=True,
        )

    def _get_engine(self, database: str, metadata: MetaData):
        if database not in self.user_engines:
            engine = create_engine(
                f"{self.database_uri}/{database}",
                connect_args={"connect_timeout": 2},
                pool_size=1,
                pool_pre_ping=True,
                pool_use_lifo=True,
                future=True,
            )
            self.user_engines[database] = engine
        self.create_default_dependencies(_engine=self.user_engines[database], metadata=metadata or Base.metadata)
        return self.user_engines[database]

    @staticmethod
    def create_default_dependencies(_engine:Engine, metadata:MetaData):
        if not database_exists(_engine.url):
            create_database(_engine.url)
        metadata.create_all(_engine, checkfirst=True)
