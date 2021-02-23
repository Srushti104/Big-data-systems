# coding=utf-8

from sqlalchemy import Column, String, Integer, Date
from base import Base

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)
    email = Column(String)

    def __init__(self, id, name, age, address, email):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.email = email
