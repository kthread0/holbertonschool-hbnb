"""Tests for the User model."""

import pytest


class TestUser:
    """Test cases for User model."""

    def test_user_creation_valid(self, app):
        """Test creating a valid user."""
        from app.models.user import User
        from app.extensions import db
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(user)
            db.session.commit()

            assert user.first_name == "John"
            assert user.last_name == "Doe"
            assert user.email == "john@example.com"
            # Password is now hashed, not plain text
            assert user.password != "password123"
            assert user.is_admin is False
            assert user.id is not None
            assert user.created_at is not None
            assert user.updated_at is not None

    def test_user_creation_with_admin(self, app):
        """Test creating an admin user."""
        from app.models.user import User
        with app.app_context():
            user = User(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password="admin123",
                is_admin=True
            )
            assert user.is_admin is True

    def test_user_invalid_first_name_empty(self, app):
        """Test user creation fails with empty first name."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="",
                    last_name="Doe",
                    email="john@example.com",
                    password="password123"
                )
            assert "First name is required" in str(exc.value)

    def test_user_invalid_first_name_too_long(self, app):
        """Test user creation fails with first name over 50 chars."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="A" * 51,
                    last_name="Doe",
                    email="john@example.com",
                    password="password123"
                )
            assert "First name is required" in str(exc.value)

    def test_user_invalid_last_name_empty(self, app):
        """Test user creation fails with empty last name."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="John",
                    last_name="",
                    email="john@example.com",
                    password="password123"
                )
            assert "Last name is required" in str(exc.value)

    def test_user_invalid_last_name_too_long(self, app):
        """Test user creation fails with last name over 50 chars."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="John",
                    last_name="D" * 51,
                    email="john@example.com",
                    password="password123"
                )
            assert "Last name is required" in str(exc.value)

    def test_user_invalid_email(self, app):
        """Test user creation fails with invalid email."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="John",
                    last_name="Doe",
                    email="invalid-email",
                    password="password123"
                )
            assert "Invalid email format" in str(exc.value)

    def test_user_invalid_email_no_domain(self, app):
        """Test user creation fails with email without domain."""
        from app.models.user import User
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                User(
                    first_name="John",
                    last_name="Doe",
                    email="john@",
                    password="password123"
                )
            assert "Invalid email format" in str(exc.value)

    def test_user_login_success(self, app):
        """Test successful password verification."""
        from app.models.user import User
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            assert user.verify_password("password123") is True

    def test_user_login_failure_wrong_email(self, app):
        """Test verify_password with wrong password fails."""
        from app.models.user import User
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            # Using verify_password instead of login method
            assert user.verify_password("wrongpassword") is False

    def test_user_login_failure_wrong_password(self, app):
        """Test verify_password fails with wrong password."""
        from app.models.user import User
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            assert user.verify_password("wrongpassword") is False

    def test_user_to_dict(self, app):
        """Test user to_dict conversion."""
        from app.models.user import User
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            user_dict = user.to_dict()
            assert user_dict['first_name'] == "John"
            assert user_dict['last_name'] == "Doe"
            assert user_dict['email'] == "john@example.com"
            assert user_dict['is_admin'] is False
            assert 'password' not in user_dict  # Password should not be in dict
            assert 'id' in user_dict
            assert 'created_at' in user_dict
            assert 'updated_at' in user_dict

    def test_user_add_place(self, app):
        """Test adding a place to user."""
        from app.models.user import User
        from app.models.place import Place
        from app.extensions import db
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(user)
            db.session.commit()

            place = Place(
                title="Test Place",
                description="A test place",
                price=100.0,
                latitude=25.0,
                longitude=-80.0,
                owner=user
            )
            db.session.add(place)
            db.session.commit()

            assert len(user.places) == 1

    def test_user_add_review(self, app):
        """Test adding a review to user."""
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.extensions import db
        with app.app_context():
            owner = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            reviewer = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                password="password456"
            )
            db.session.add(owner)
            db.session.add(reviewer)
            db.session.commit()

            place = Place(
                title="Test Place",
                description="A test place",
                price=100.0,
                latitude=25.0,
                longitude=-80.0,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            review = Review(
                text="Great place!",
                rating=5,
                place=place,
                user=reviewer
            )
            db.session.add(review)
            db.session.commit()

            assert len(reviewer.reviews) == 1

    def test_user_update(self, app):
        """Test updating user attributes."""
        from app.models.user import User
        from app.extensions import db
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(user)
            db.session.commit()

            old_updated_at = user.updated_at
            user.update({'first_name': 'Jane', 'last_name': 'Smith'})
            assert user.first_name == "Jane"
            assert user.last_name == "Smith"
            assert user.updated_at >= old_updated_at
