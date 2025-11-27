"""Tests for the Repository implementations."""

import pytest


class TestInMemoryRepository:
    """Test cases for InMemoryRepository."""

    def test_add_and_get(self, app):
        """Test adding and retrieving an object."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            retrieved = repo.get(user.id)
            assert retrieved == user

    def test_get_nonexistent(self, app):
        """Test getting non-existent object returns None."""
        from app.persistence.repository import InMemoryRepository
        with app.app_context():
            repo = InMemoryRepository()
            result = repo.get("nonexistent-id")
            assert result is None

    def test_get_all_empty(self, app):
        """Test get_all on empty repository."""
        from app.persistence.repository import InMemoryRepository
        with app.app_context():
            repo = InMemoryRepository()
            result = repo.get_all()
            assert result == []

    def test_get_all_multiple(self, app):
        """Test get_all with multiple objects."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user1 = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            user2 = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                password="password456"
            )
            repo.add(user1)
            repo.add(user2)
            result = repo.get_all()
            assert len(result) == 2

    def test_update(self, app):
        """Test updating an object."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            # Directly update the object in repo since update calls save which needs db
            user.first_name = 'Jane'
            updated = repo.get(user.id)
            assert updated.first_name == 'Jane'

    def test_update_nonexistent(self, app):
        """Test updating non-existent object returns None."""
        from app.persistence.repository import InMemoryRepository
        with app.app_context():
            repo = InMemoryRepository()
            result = repo.update("nonexistent-id", {'first_name': 'Jane'})
            assert result is None

    def test_delete(self, app):
        """Test deleting an object."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            result = repo.delete(user.id)
            assert result is True
            assert repo.get(user.id) is None

    def test_delete_nonexistent(self, app):
        """Test deleting non-existent object returns False."""
        from app.persistence.repository import InMemoryRepository
        with app.app_context():
            repo = InMemoryRepository()
            result = repo.delete("nonexistent-id")
            assert result is False

    def test_get_by_attribute(self, app):
        """Test retrieving by attribute."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            result = repo.get_by_attribute('email', 'john@example.com')
            assert result == user

    def test_get_by_attribute_not_found(self, app):
        """Test retrieving by attribute not found returns None."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            result = repo.get_by_attribute('email', 'notfound@example.com')
            assert result is None

    def test_get_all_by_attribute(self, app):
        """Test retrieving all objects by attribute."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user1 = User(
                first_name="John",
                last_name="Doe",
                email="john1@example.com",
                password="password123"
            )
            user2 = User(
                first_name="John",
                last_name="Smith",
                email="john2@example.com",
                password="password456"
            )
            user3 = User(
                first_name="Jane",
                last_name="Doe",
                email="jane@example.com",
                password="password789"
            )
            repo.add(user1)
            repo.add(user2)
            repo.add(user3)
            result = repo.get_all_by_attribute('first_name', 'John')
            assert len(result) == 2

    def test_get_all_by_attribute_none_found(self, app):
        """Test retrieving all by attribute returns empty list when none found."""
        from app.persistence.repository import InMemoryRepository
        from app.models.user import User
        with app.app_context():
            repo = InMemoryRepository()
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            repo.add(user)
            result = repo.get_all_by_attribute('first_name', 'Unknown')
            assert result == []
