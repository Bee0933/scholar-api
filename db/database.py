from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from decouple import config 

# get connection string from env vars
con_str = config('connection_string')

# create connection to pg-db engine with echo of SQL DDL's
engine = create_engine(con_str, echo=True)

# create instance of base class for schema
Base = declarative_base()

# creats db session instance
Session = sessionmaker()