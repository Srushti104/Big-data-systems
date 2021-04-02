import snowflake.connector as sf
import uvicorn as uvicorn
from config import config
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from snowflake.connector import DictCursor
from pydantic import BaseModel

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import JSONResponse

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localhost"
#
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
# api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)
#
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, debug=True)

# client = TestClient(app)

ctx = sf.connect(user=config.username, password=config.password, account=config.account, warehouse=config.warehouse,
                 database=config.database)

#app = FastAPI()


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    # api_key_header: str = Security(api_key_header),
    # api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    # elif api_key_header == API_KEY:
    #     return api_key_header
    # elif api_key_cookie == API_KEY:
    #     return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

class Company(BaseModel):
    Date: str
    open: str
    High: str
    Low: str
    Close: str
    Volume: str
    openINT: str
    Company: str
    ETFs_Stocks: str

@app.get("/")
async def homepage():
    return "Welcome to the security test!"
#
@app.get("/openapi.json", tags=["Documentation"])
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
    )
    return response

@app.get("/docs", tags=["Documentation"])
async def get_documentation():
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/Company/{company}")
def getcompany_data(company: str,api_key: APIKey = Depends(get_api_key)):
    cursor = ctx.cursor(DictCursor)
    sql = cursor.execute("Select * from STOCK_DATA.PUBLIC.STOCKS where COMPANY =('"+company+"')")
    result=[]
    for data in sql:
        result.append(data)
        print(data)
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    else:
        return {"company": company, "Data": result}

@app.get("/Year/{Year}")
def getyear_data(Year: str, api_key: APIKey = Depends(get_api_key)):
    cursor = ctx.cursor(DictCursor)
    sql = cursor.execute("select * from STOCK_DATA.PUBLIC.STOCKS a where extract (year from(CAST(a.date as date))) =('"+Year+"') limit 1000")
    result=[]
    for data in sql:
        result.append(data)
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    else:
        return {"company": Year, "Data": result}

@app.get("/Date/{Date}")
def getdate_data(Date: str,ETFS_STOCKS:str,api_key: APIKey = Depends(get_api_key)):
    cursor = ctx.cursor(DictCursor)
    sql = cursor.execute("select * from STOCK_DATA.PUBLIC.STOCKS a where a.DATE ='"+Date+"' and a.ETFS_STOCKS='"+ETFS_STOCKS+"' limit 1000")
    result=[]
    for data in sql:
        result.append(data)
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    else:
        return {"company": Date, "Data": result}

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')