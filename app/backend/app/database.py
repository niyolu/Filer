from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from . import config

settings: config.Settings = config.get_settings()


port = "3306"
database = "db"

CONN_STR = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_pw}@{settings.db_host}:{port}/{database}"

engine = create_engine(CONN_STR)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()