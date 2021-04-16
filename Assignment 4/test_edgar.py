from fastapi.testclient import TestClient
from edgar import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "EDGAR CALL-EARNINGS"

def test_readfile():
    response = client.get("/Edgar/AGEN")
    # if APIKey:
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_PII_entities():
    response = client.get("/Edgar?s3_path=s3%3A%2F%2Ftextfiles2%2Fcall_transcripts%2FAGEN")
    #if APIKey:
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_date():
    response = client.get("/new?s3_path=s3%3A%2F%2Ftextfiles2%2Fcall_transcripts%2FAGEN&Mask_Entity=NAME&deidentify_Ent=ADDRESS")
    assert response.status_code == 200
    assert len(response.json()) != 0
