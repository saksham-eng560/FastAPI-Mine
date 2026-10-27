from fastapi import FastAPI
from fastapi.testclient import TestClient
from testtt import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")

    assert response.status_code == 200 #status code check

    assert response.json() == {"Hello": "World"} #response check