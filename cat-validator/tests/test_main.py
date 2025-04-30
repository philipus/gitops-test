from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_valid_cat_with_all_fields():
    response = client.post(
        "/validate",
        json={"name": "Whiskers", "age": 3, "breed": "Siamese"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["data"]["name"] == "Whiskers"
    assert data["data"]["age"] == 3
    assert data["data"]["breed"] == "Siamese"
    assert data["errors"] is None

def test_valid_cat_without_optional_field():
    response = client.post(
        "/validate",
        json={"name": "Mittens", "age": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["data"]["name"] == "Mittens"
    assert data["data"]["age"] == 5
    assert data["data"]["breed"] is None
    assert data["errors"] is None

def test_missing_required_field():
    response = client.post(
        "/validate",
        json={"age": 3}  # Missing name field
    )
    assert response.status_code == 422
    data = response.json()
    assert data["valid"] is False
    assert data["data"] is None
    assert len(data["errors"]) > 0
    assert any("name" in error.lower() for error in data["errors"])

def test_invalid_age_type():
    response = client.post(
        "/validate",
        json={"name": "Luna", "age": "three"}  # Age should be integer
    )
    assert response.status_code == 422
    data = response.json()
    assert data["valid"] is False
    assert data["data"] is None
    assert len(data["errors"]) > 0
    assert any("age" in error.lower() for error in data["errors"])

def test_invalid_json():
    response = client.post(
        "/validate",
        data="invalid json"
    )
    assert response.status_code == 422
    data = response.json()
    assert data["valid"] is False
    assert data["data"] is None
    assert len(data["errors"]) > 0 