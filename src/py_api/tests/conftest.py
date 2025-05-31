import pytest
from fastapi.testclient import TestClient
from ..app import app

@pytest.fixture
def client():
  return TestClient(app)

# Sample receipt store and point cache for testing
@pytest.fixture
def memory_stores():
  return {}, {}