from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_engine = create_engine("sqlite:///sensor_measurements.db", echo=True)

_Session = sessionmaker(bind=sql_engine)
session = _Session()

Base = declarative_base()
