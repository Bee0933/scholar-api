from database import Session, engine, Base
from models import User, History 


# create database with tables
Base.metadata.create_all(bind=engine)