import pytest
from flask import Flask


@pytest.fixture
def test_app():
    return Flask('testapp')
