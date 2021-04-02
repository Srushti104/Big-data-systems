from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from stockAPI import app, API_KEY, API_KEY_NAME, api_key_query, get_api_key

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Welcome to the security test!"

def test_company(api_key: APIKey = Depends(get_api_key)):
    response = client.get("/Company/asm?access_token=1234567asdfgh")
    if APIKey:
     assert response.status_code == 200
     assert len(response.json()) != 0

def test_year(api_key: APIKey = Depends(get_api_key)):
    response = client.get("Year/2002?access_token=1234567asdfgh")
    if APIKey:
      assert response.status_code == 200
      assert len(response.json()) != 0

def test_date(api_key: APIKey = Depends(get_api_key)):
    response = client.get("/Date/2016-06-29?ETFS_STOCKS=ETF&access_token=1234567asdfgh")
    if APIKey:
        assert response.status_code == 200
        assert len(response.json()) != 0

def test_company_error(api_key: APIKey = Depends(get_api_key)):
    response = client.get("/Company/hello?access_token=1234567asdfgh")
    if APIKey:
        assert response.status_code == 404
        assert len(response.json())!=0

def test_bad_api_key(api_key: APIKey = Depends(get_api_key)):
    response = client.get("Year/2002?access_token=shshgsfag")
    if APIKey:
      assert response.status_code == 403
      assert len(response.json()) != 0