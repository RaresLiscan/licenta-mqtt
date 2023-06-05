from .base import Base, session, sql_engine
from sqlalchemy import Column, Integer, Numeric, BigInteger, Identity
import time

last_add_timestamp = 0


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column("id", Integer, Identity(start=1, cycle=True), primary_key=True)
    timestamp = Column("timestamp", BigInteger)
    humidity = Column("humidity", Numeric)
    temperature = Column("temperature", Numeric)

    def __init__(self, timestamp, humidity, temperature):
        self.timestamp = timestamp
        self.humidity = humidity
        self.temperature = temperature

    def __init__(self, humidity, temperature):
        self.timestamp = (time.time() * 1000).__floor__()
        self.humidity = humidity
        self.temperature = temperature

    def __repr__(self):
        return f"({self.timestamp}: [{self.humidity}, {self.temperature}])"


Base.metadata.create_all(sql_engine)


def add_data(humidity, temperature):
    current_timestamp = (time.time() * 1000).__floor__()
    if current_timestamp - last_add_timestamp > 1000:
        measurement = Measurement(humidity, temperature)
        session.add(measurement)
        session.commit()


def read_all_measurements():
    results = session.query(Measurement).all()
    return results
