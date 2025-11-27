"""Pytest configuration and fixtures."""

from app.extensions import db
from app import create_app
import sys
import os
import pytest

# Add the app directory to the path so imports work correctly
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    app = create_app('config.TestConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def app_context(app):
    """Provide app context for tests."""
    with app.app_context():
        yield


@pytest.fixture(scope='function')
def facade(app):
    """Create a fresh facade for each test within app context."""
    from app.services.facade import HBnBFacade
    with app.app_context():
        yield HBnBFacade()
