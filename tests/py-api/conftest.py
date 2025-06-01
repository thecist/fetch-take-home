import pytest
from fastapi.testclient import TestClient
from src.py_api.app import app

@pytest.fixture
def client():
  return TestClient(app)
