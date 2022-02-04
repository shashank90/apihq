import sqlalchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

# Connect and create an SQLAlchemy session
DATABASE_NAME = "cymitra"
SCHEMA_NAME = "apihq"
engine = create_engine(f"postgres://p075am:p075am@localhost/{DATABASE_NAME}")
# Create db if not exists
if not database_exists(engine.url):
    create_database(engine.url)
# Create schema if not exists(Schema is equivalent of database in mysql)
if not engine.dialect.has_schema(engine, SCHEMA_NAME):
    engine.execute(sqlalchemy.schema.CreateSchema(SCHEMA_NAME))

Session = sessionmaker()
Session.configure(bind=engine)
# TODO: Need to read more about sessions. Currently, using it as singleton. But can we create on-demand and use?
db_session = Session()
Base = declarative_base()
# All tables will be created under this schema
Base.metadata.schema = SCHEMA_NAME

from db.model import user
from db.model import api_spec
from db.model import api_inventory
from db.model import api_audit
from db.model import api_scan


def init_db():
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError as se:
        error = str(se.__dict__["orig"])
        print(error)


def get_session():
    return db_session


# TODO: Close session at end of application
