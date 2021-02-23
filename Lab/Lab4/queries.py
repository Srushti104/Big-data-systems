from base import Session
from customer import Customer

session = Session()

def get_all_data():
    print('Getting All Data')

    customers = session.query(Customer).all()
    for customer in customers:
        print(customer.id)
        print(customer.name)
        print(customer.age)
        print(customer.address)


def update_record():
    session.query(Customer) \
        .filter(Customer.id == 4) \
        .update({Customer.name: 'Updated'})

    session.commit()

get_all_data()
update_record()
get_all_data()