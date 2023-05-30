from typing import Any
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return (
            f"({self.ssn} {self.firstname} {self.lastname} {self.gender}, {self.age})"
        )


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# person = Person(1231, "Mike", "Smith", "m", 46)

# session.add(person)
# session.commit()

# p1 = Person(332, "Anna", "Blue", "f", 33)
# p2 = Person(13241, "Bob", "Blue", "m", 35)

# session.add(p1)
# session.add(p2)
# session.commit()

# results = session.query(Person).filter(Person.firstname.in_(["Anna", "Mike"]))

# for r in results:
#     print(r)


current_timestamp = time.time()
print(current_timestamp.__floor__())

# engine = create_engine("postgresql://postgres:1234@localhost:5432/mqtt-dev")
