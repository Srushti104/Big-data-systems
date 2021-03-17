from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import boto3
from datetime import datetime

# Defined Functions
from stock_price import fetch_current_price
from id_generator import get_unique_id

app = FastAPI()

# Your DynamoDB table name
dynamo_table = 'customer-trades'

# Connect to DynamoDB
resource = boto3.resource('dynamodb', region_name='us-east-1')

# Connect to the table
table = resource.Table(dynamo_table)


class Stock(BaseModel):
    customer_id: int
    name: str
    position: str
    qty: int


@app.get("/")
def read_root():
    return {"Course": "CSYE7245"}


# Get the current stock price
@app.get("/stock_price/{name}")
def get_stock(name: str):
    stock_price = fetch_current_price(name)
    return {"name": name, "price": stock_price}


# Place trades
@app.post("/trade/{customer_id}")
def trade_stock(customer_id: int, name: str, qty: int, position: str):
    # Get the price of the stock
    stock_price = fetch_current_price(name)

    # Generate an unique transaction ID for the trade
    id = get_unique_id(10)

    # Push data into DynamoDB
    response = table.put_item(
        Item={
            'id': id,
            'customer_id': customer_id,
            'name': name,
            'price': str(stock_price),
            'quantity': qty,
            'position': position,
            'trade_time': str(datetime.now())
        }
    )

    return {"transaction_id": id, "customer_id": customer_id, "price": stock_price, "position": position,
            "dynamo_put_operation_response": response}


# Get all trades for a given customer ID
@app.get("/get_trades/{customer_id}")
def get_trades(customer_id: int):
    # Scan DynamoDB
    response = table.scan(
        AttributesToGet=['id', 'customer_id', 'name', 'price', 'quantity', 'position', 'trade_time']
    )

    filteredResult = [d for d in response['Items'] if d['customer_id'] == customer_id]

    return {"customer_id": customer_id, "trades": filteredResult}
