import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database
from backend.log.factory import Logger

logger = Logger(__name__)

# Connect and create an SQLAlchemy session
DATABASE_NAME = "cymitra"
SCHEMA_NAME = "apihome"

# TODO: Move this to .env
# USER_P075am_PASSWORD = "Wyr73x@BgQQ;4"

# engine = create_engine(
#     f"postgres://p075am:{USER_P075am_PASSWORD}@localhost/{DATABASE_NAME}"
# )

# engine = create_engine(DATABASE_URI)

# Create db if not exists
# if not database_exists(engine.url):
#     create_database(engine.url)

# # Create schema if not exists(Schema is equivalent of database in mysql)
# if not engine.dialect.has_schema(engine, SCHEMA_NAME):
#     engine.execute(sqlalchemy.schema.CreateSchema(SCHEMA_NAME))

# Session = sessionmaker()
# Session.configure(bind=engine)
# TODO: Need to read more about sessions. Currently, using it as singleton. But can we create on-demand and use?
# db_session = Session()

db_session = None
Base = declarative_base()
# All tables will be created under this schema
Base.metadata.schema = SCHEMA_NAME

from backend.db.model import user
from backend.db.model import api_spec
from backend.db.model import api_inventory
from backend.db.model import api_validate
from backend.db.model import api_run
from backend.db.model import user_login
from backend.db.model import user_api_run_limit


def configure_engine(DATABASE_URI):
    """
    One-time database configuration
    """
    engine = create_engine(DATABASE_URI)
    print(DATABASE_URI)
    # Create db if not exists
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create schema if not exists(Schema is equivalent of database in mysql)
    if not engine.dialect.has_schema(engine, SCHEMA_NAME):
        engine.execute(sqlalchemy.schema.CreateSchema(SCHEMA_NAME))

    return engine


def configure_db_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    global db_session
    db_session = Session()


def init_db(DATABASE_URI):
    try:
        engine = configure_engine(DATABASE_URI)
        configure_db_session(engine)
        Base.metadata.create_all(engine)
        logger.info("Database init complete...")
    except SQLAlchemyError as se:
        error = str(se.__dict__["orig"])
        logger.error(f"Could not initialize database. Error: {error}")
        raise (se)
    except Exception as e:
        logger.error(f"Could not initialize database. Error: {str(e)}")
        raise (e)


def get_session():
    return db_session


# TODO: Close session at end of application
