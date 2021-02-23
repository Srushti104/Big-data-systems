# coding=utf-8

from customer import Customer
from base import Session, engine, Base

# Generate database schema
Base.metadata.create_all(engine)

# Create a new session
session = Session()

cust1 = Customer(4, 'Jane Doe', 25, 'Boston MA', 'jdoe@example.com')
cust2 = Customer(5, 'John Doe', 42, '678 West Ave, Boston MA', 'john@example.com')

session.add(cust1)
session.add(cust2)
session.commit()
session.close()
