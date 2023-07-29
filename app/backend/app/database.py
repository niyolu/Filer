from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import config

settings: config.Settings = config.get_settings()

port = "3306"

CONN_STR = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_pw}@{settings.db_host}:{port}/{settings.db_database}"

engine = create_engine(CONN_STR)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SerializableBase(Base):
    __abstract__ = True
    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
