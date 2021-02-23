import csv
import random
from time import time
from decimal import Decimal
from faker import Faker
import boto3
import string
import random
import os

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')


RECORD_COUNT = 100
fake = Faker()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_csv_file():
    filename = 'data-' + id_generator(10) + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'first_name', 'last_name', 'email', 'product_id', 'qty',
                      'amount', 'description', 'address', 'city', 'state',
                      'country']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {   'id': id_generator(12),
                    'first_name': fake.name(),
                    'last_name': fake.name(),
                    'email': fake.email(),
                    'product_id': fake.random_int(min=100, max=199),
                    'qty': fake.random_int(min=1, max=9),
                    'amount': fake.random_int(min=1000, max=9000),
                    'description': fake.sentence(),
                    'address': fake.street_address(),
                    'city': fake.city(),
                    'state': fake.state(),
                    'country': fake.country()
                }
            )


    upload_to_s3(filename)

# Enter your S3 Bucket name here
bucket_name = ''

def upload_to_s3(filename):
    s3.Bucket(bucket_name).upload_file(Filename=filename, Key='demo/' + filename)
    print ('Upload Complete')


create_csv_file()

