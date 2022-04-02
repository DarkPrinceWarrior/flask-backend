import sys
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# the instance of engine
# create declarative_base instance
Base = declarative_base()
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.

engine = create_engine('sqlite:///app.sqlite')


# create the db
def create_db():
    Base.metadata.create_all(engine)

