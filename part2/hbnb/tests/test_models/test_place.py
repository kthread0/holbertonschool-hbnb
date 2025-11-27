"""Tests for the Place model."""

import pytest


class TestPlace:
    """Test cases for Place model."""

    def test_place_creation_valid(self, app):
        """Test creating a valid place."""
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

            assert place.title == "Beach House"
            assert place.description == "A lovely beach house"
            assert place.price == 150.0
            assert place.latitude == 25.7617
            assert place.longitude == -80.1918
            assert place.owner_id == owner.id
            assert place.id is not None

    def test_place_invalid_title_empty(self, app):
        """Test place creation fails with empty title."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="",
                    description="Description",
                    price=100.0,
                    latitude=0.0,
                    longitude=0.0,
                    owner=owner
                )
            assert "Title is required" in str(exc.value)

    def test_place_invalid_title_too_long(self, app):
        """Test place creation fails with title over 100 chars."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="A" * 101,
                    description="Description",
                    price=100.0,
                    latitude=0.0,
                    longitude=0.0,
                    owner=owner
                )
            assert "Title is required" in str(exc.value)

    def test_place_invalid_price_negative(self, app):
        """Test place creation fails with negative price."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="Beach House",
                    description="Description",
                    price=-50.0,
                    latitude=0.0,
                    longitude=0.0,
                    owner=owner
                )
            assert "Price must be a positive value" in str(exc.value)

    def test_place_invalid_latitude_too_low(self, app):
        """Test place creation fails with latitude below -90."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="Beach House",
                    description="Description",
                    price=100.0,
                    latitude=-91.0,
                    longitude=0.0,
                    owner=owner
                )
            assert "Latitude must be between -90 and 90" in str(exc.value)

    def test_place_invalid_latitude_too_high(self, app):
        """Test place creation fails with latitude above 90."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="Beach House",
                    description="Description",
                    price=100.0,
                    latitude=91.0,
                    longitude=0.0,
                    owner=owner
                )
            assert "Latitude must be between -90 and 90" in str(exc.value)

    def test_place_invalid_longitude_too_low(self, app):
        """Test place creation fails with longitude below -180."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="Beach House",
                    description="Description",
                    price=100.0,
                    latitude=0.0,
                    longitude=-181.0,
                    owner=owner
                )
            assert "Longitude must be between -180 and 180" in str(exc.value)

    def test_place_invalid_longitude_too_high(self, app):
        """Test place creation fails with longitude above 180."""
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

            with pytest.raises(ValueError) as exc:
                Place(
                    title="Beach House",
                    description="Description",
                    price=100.0,
                    latitude=0.0,
                    longitude=181.0,
                    owner=owner
                )
            assert "Longitude must be between -180 and 180" in str(exc.value)

    def test_place_add_amenity(self, app):
        """Test adding an amenity to a place."""
        from app.models.place import Place
        from app.models.user import User
        from app.models.amenity import Amenity
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
                description="Description",
                price=100.0,
                latitude=0.0,
                longitude=0.0,
                owner=owner
            )
            amenity = Amenity(name="WiFi")
            db.session.add(place)
            db.session.add(amenity)
            db.session.commit()

            place.add_amenity(amenity)
            db.session.commit()
            assert len(place.amenities) == 1
            assert amenity in place.amenities

    def test_place_add_amenity_duplicate(self, app):
        """Test adding duplicate amenity does not add twice."""
        from app.models.place import Place
        from app.models.user import User
        from app.models.amenity import Amenity
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
                description="Description",
                price=100.0,
                latitude=0.0,
                longitude=0.0,
                owner=owner
            )
            amenity = Amenity(name="WiFi")
            db.session.add(place)
            db.session.add(amenity)
            db.session.commit()

            place.add_amenity(amenity)
            place.add_amenity(amenity)
            db.session.commit()
            assert len(place.amenities) == 1

    def test_place_remove_amenity(self, app):
        """Test removing an amenity from a place."""
        from app.models.place import Place
        from app.models.user import User
        from app.models.amenity import Amenity
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
                description="Description",
                price=100.0,
                latitude=0.0,
                longitude=0.0,
                owner=owner
            )
            amenity = Amenity(name="WiFi")
            db.session.add(place)
            db.session.add(amenity)
            db.session.commit()

            place.add_amenity(amenity)
            db.session.commit()
            place.remove_amenity(amenity)
            db.session.commit()
            assert len(place.amenities) == 0

    def test_place_add_review(self, app):
        """Test adding a review to a place."""
        from app.models.place import Place
        from app.models.user import User
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
                title="Beach House",
                description="Description",
                price=100.0,
                latitude=0.0,
                longitude=0.0,
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
            assert len(place.reviews) == 1

    def test_place_to_dict(self, app):
        """Test place to_dict conversion."""
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

            place_dict = place.to_dict()
            assert place_dict['title'] == "Beach House"
            assert place_dict['description'] == "A lovely beach house"
            assert place_dict['price'] == 150.0
            assert place_dict['latitude'] == 25.7617
            assert place_dict['longitude'] == -80.1918
            assert place_dict['owner_id'] == owner.id
            assert 'id' in place_dict
            assert 'created_at' in place_dict
            assert 'updated_at' in place_dict

    def test_place_update(self, app):
        """Test updating place attributes."""
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
                description="Description",
                price=100.0,
                latitude=0.0,
                longitude=0.0,
                owner=owner
            )
            db.session.add(place)
            db.session.commit()

            place.update({'title': 'Mountain Cabin', 'price': 200.0})
            assert place.title == "Mountain Cabin"
            assert place.price == 200.0
