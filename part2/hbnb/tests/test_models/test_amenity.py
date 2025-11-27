"""Tests for the Amenity model."""

import pytest


class TestAmenity:
    """Test cases for Amenity model."""

    def test_amenity_creation_valid(self, app):
        """Test creating a valid amenity."""
        from app.models.amenity import Amenity
        from app.extensions import db
        with app.app_context():
            amenity = Amenity(name="WiFi", description="High-speed internet")
            db.session.add(amenity)
            db.session.commit()
            assert amenity.name == "WiFi"
            assert amenity.description == "High-speed internet"
            assert amenity.id is not None
            assert amenity.created_at is not None
            assert amenity.updated_at is not None

    def test_amenity_creation_without_description(self, app):
        """Test creating amenity without description."""
        from app.models.amenity import Amenity
        with app.app_context():
            amenity = Amenity(name="Pool")
            assert amenity.name == "Pool"
            assert amenity.description == ""

    def test_amenity_invalid_name_empty(self, app):
        """Test amenity creation fails with empty name."""
        from app.models.amenity import Amenity
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                Amenity(name="")
            assert "Amenity name is required" in str(exc.value)

    def test_amenity_invalid_name_too_long(self, app):
        """Test amenity creation fails with name over 50 chars."""
        from app.models.amenity import Amenity
        with app.app_context():
            with pytest.raises(ValueError) as exc:
                Amenity(name="A" * 51)
            assert "Amenity name is required" in str(exc.value)

    def test_amenity_name_at_limit(self, app):
        """Test amenity creation succeeds with name at 50 chars."""
        from app.models.amenity import Amenity
        with app.app_context():
            amenity = Amenity(name="A" * 50)
            assert len(amenity.name) == 50

    def test_amenity_to_dict(self, app):
        """Test amenity to_dict conversion."""
        from app.models.amenity import Amenity
        with app.app_context():
            amenity = Amenity(name="WiFi", description="High-speed internet")
            amenity_dict = amenity.to_dict()
            assert amenity_dict['name'] == "WiFi"
            assert amenity_dict['description'] == "High-speed internet"
            assert 'id' in amenity_dict
            assert 'created_at' in amenity_dict
            assert 'updated_at' in amenity_dict

    def test_amenity_update(self, app):
        """Test updating amenity attributes."""
        from app.models.amenity import Amenity
        from app.extensions import db
        with app.app_context():
            amenity = Amenity(name="WiFi")
            db.session.add(amenity)
            db.session.commit()
            old_updated_at = amenity.updated_at
            amenity.update({'name': 'Fast WiFi', 'description': '5G internet'})
            assert amenity.name == "Fast WiFi"
            assert amenity.description == "5G internet"
            assert amenity.updated_at >= old_updated_at
