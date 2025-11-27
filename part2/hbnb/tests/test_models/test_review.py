"""Tests for the Review model."""

import pytest


class TestReview:
    """Test cases for Review model."""

    def test_review_creation_valid(self, app):
        """Test creating a valid review."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            review = Review(
                text="Great place to stay!",
                rating=5,
                place=place,
                user=reviewer
            )
            db.session.add(review)
            db.session.commit()

            assert review.text == "Great place to stay!"
            assert review.rating == 5
            assert review.place_id == place.id
            assert review.user_id == reviewer.id
            assert review.id is not None

    def test_review_invalid_text_empty(self, app):
        """Test review creation fails with empty text."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="",
                    rating=5,
                    place=place,
                    user=reviewer
                )
            assert "Review text is required" in str(exc.value)

    def test_review_invalid_rating_too_low(self, app):
        """Test review creation fails with rating below 1."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="Bad place",
                    rating=0,
                    place=place,
                    user=reviewer
                )
            assert "Rating must be between 1 and 5" in str(exc.value)

    def test_review_invalid_rating_too_high(self, app):
        """Test review creation fails with rating above 5."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="Amazing place",
                    rating=6,
                    place=place,
                    user=reviewer
                )
            assert "Rating must be between 1 and 5" in str(exc.value)

    def test_review_invalid_rating_none(self, app):
        """Test review creation fails with None rating."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="Good place",
                    rating=None,
                    place=place,
                    user=reviewer
                )
            assert "Rating must be between 1 and 5" in str(exc.value)

    def test_review_invalid_place_none(self, app):
        """Test review creation fails with no place."""
        from app.models.review import Review
        from app.models.user import User
        from app.extensions import db
        with app.app_context():
            reviewer = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                password="password456"
            )
            db.session.add(reviewer)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="Good place",
                    rating=4,
                    place=None,
                    user=reviewer
                )
            assert "Place is required" in str(exc.value)

    def test_review_invalid_user_none(self, app):
        """Test review creation fails with no user."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
        from app.extensions import db
        with app.app_context():
            owner = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(owner)
            db.session.commit()

            place = Place(
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            with pytest.raises(ValueError) as exc:
                Review(
                    text="Good place",
                    rating=4,
                    place=place,
                    user=None
                )
            assert "User is required" in str(exc.value)

    def test_review_to_dict(self, app):
        """Test review to_dict conversion."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            review = Review(
                text="Great place to stay!",
                rating=5,
                place=place,
                user=reviewer
            )
            review_dict = review.to_dict()
            assert review_dict['text'] == "Great place to stay!"
            assert review_dict['rating'] == 5
            assert review_dict['place_id'] == place.id
            assert review_dict['user_id'] == reviewer.id
            assert 'id' in review_dict
            assert 'created_at' in review_dict
            assert 'updated_at' in review_dict

    def test_review_update(self, app):
        """Test updating review attributes."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            review = Review(
                text="Good place",
                rating=4,
                place=place,
                user=reviewer
            )
            db.session.add(review)
            db.session.commit()

            review.update({'text': 'Excellent place!', 'rating': 5})
            assert review.text == "Excellent place!"
            assert review.rating == 5

    def test_review_all_ratings(self, app):
        """Test all valid rating values 1-5."""
        from app.models.review import Review
        from app.models.place import Place
        from app.models.user import User
        from app.extensions import db
        with app.app_context():
            owner = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            db.session.add(owner)
            db.session.commit()

            place = Place(
                title="Beach House",
                description="A lovely beach house",
                price=150.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            for i, rating in enumerate(range(1, 6)):
                reviewer = User(
                    first_name=f"Reviewer{i}",
                    last_name="Test",
                    email=f"reviewer{i}@example.com",
                    password="password123"
                )
                db.session.add(reviewer)
                db.session.commit()

                review = Review(
                    text=f"Rating {rating}",
                    rating=rating,
                    place=place,
                    user=reviewer
                )
                assert review.rating == rating
