from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy of original participants to restore after test
    original = {k: v["participants"][:] for k, v in activities.items()}
    yield
    for k, v in original.items():
        activities[k]["participants"] = v[:]


@pytest.fixture
def client():
    return TestClient(app)
