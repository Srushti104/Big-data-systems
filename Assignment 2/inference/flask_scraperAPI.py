from os import listdir
from os.path import isfile, join

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Specify your Data Directory here
data_dir = '/Users/akshaybhoge/PycharmProjects/Edgar/inference-data/'
companies = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]


class Item(BaseModel):
    company: str
    year: int


@app.get("/call-transcripts/{company}/{year}")
def get_data(company: str, year: int):
    if company in companies and year == 2021:
        with open(data_dir + company) as f:
            s = f.read()
        return {"company": company, "transcript": s}
    else:
        raise HTTPException(status_code=404, detail="Company not found")


if __name__ == '__main__':
    uvicorn.run(app, port=8081, host='0.0.0.0')
