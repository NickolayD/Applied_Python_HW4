from fastapi.testclient import TestClient
from app import app
import pickle
import json


client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '{"Status":"Everything is OK!"}'


def test_predict():
    with open("list_for_test.pkl", "rb") as f:
        good_list = pickle.load(f)
    response = client.post(
        "/predict",
        data=json.dumps({"array": good_list})
    )
    assert response.status_code == 200
    assert response.text == '{"Vegetable":"Бобы (Bean)"}'


def test_predict_badsize():
    response = client.post(
        "/predict",
        data=json.dumps({"array": [0 for _ in range(10)]})
    )
    assert response.status_code == 1001
    assert response.json() == {"detail": "Wrong data size."}
