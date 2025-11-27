"""Tests for the HBnBFacade service."""

import pytest


class TestHBnBFacade:
    """Test cases for HBnBFacade."""

    # ==================== User Tests ====================

    def test_create_user(self, app):
        """Test creating a user through facade."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            user = facade.create_user(user_data)
            assert user.first_name == 'John'
            assert user.email == 'john@example.com'
            assert user.id is not None

    def test_create_user_duplicate_email(self, app):
        """Test creating user with duplicate email fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            facade.create_user(user_data)
            with pytest.raises(ValueError) as exc:
                facade.create_user(user_data)
            assert "Email already registered" in str(exc.value)

    def test_get_user(self, app):
        """Test getting a user by ID."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            created = facade.create_user(user_data)
            retrieved = facade.get_user(created.id)
            assert retrieved.id == created.id

    def test_get_user_not_found(self, app):
        """Test getting non-existent user returns None."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            result = facade.get_user("nonexistent-id")
            assert result is None

    def test_get_user_by_email(self, app):
        """Test getting user by email."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            created = facade.create_user(user_data)
            retrieved = facade.get_user_by_email('john@example.com')
            assert retrieved.id == created.id

    def test_get_all_users(self, app):
        """Test getting all users."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            users = facade.get_all_users()
            assert len(users) == 2

    def test_update_user(self, app):
        """Test updating a user."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            created = facade.create_user(user_data)
            updated = facade.update_user(created.id, {'first_name': 'Jane'})
            assert updated.first_name == 'Jane'

    def test_update_user_email_duplicate(self, app):
        """Test updating user email to existing email fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            user2 = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            with pytest.raises(ValueError) as exc:
                facade.update_user(user2.id, {'email': 'john@example.com'})
            assert "Email already registered" in str(exc.value)

    def test_delete_user(self, app):
        """Test deleting a user."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }
            created = facade.create_user(user_data)
            result = facade.delete_user(created.id)
            assert result is True
            assert facade.get_user(created.id) is None

    # ==================== Amenity Tests ====================

    def test_create_amenity(self, app):
        """Test creating an amenity."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            amenity = facade.create_amenity(
                {'name': 'WiFi', 'description': 'Fast internet'})
            assert amenity.name == 'WiFi'
            assert amenity.id is not None

    def test_get_amenity(self, app):
        """Test getting an amenity by ID."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            created = facade.create_amenity({'name': 'WiFi'})
            retrieved = facade.get_amenity(created.id)
            assert retrieved.id == created.id

    def test_get_all_amenities(self, app):
        """Test getting all amenities."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            facade.create_amenity({'name': 'WiFi'})
            facade.create_amenity({'name': 'Pool'})
            amenities = facade.get_all_amenities()
            assert len(amenities) == 2

    def test_update_amenity(self, app):
        """Test updating an amenity."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            created = facade.create_amenity({'name': 'WiFi'})
            updated = facade.update_amenity(created.id, {'name': 'Fast WiFi'})
            assert updated.name == 'Fast WiFi'

    def test_delete_amenity(self, app):
        """Test deleting an amenity."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            created = facade.create_amenity({'name': 'WiFi'})
            result = facade.delete_amenity(created.id)
            assert result is True
            assert facade.get_amenity(created.id) is None

    # ==================== Place Tests ====================

    def test_create_place(self, app):
        """Test creating a place."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'description': 'A lovely beach house',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            assert place.title == 'Beach House'
            assert place.owner_id == owner.id

    def test_create_place_with_amenities(self, app):
        """Test creating a place with amenities."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            amenity = facade.create_amenity({'name': 'WiFi'})
            place = facade.create_place({
                'title': 'Beach House',
                'description': 'A lovely beach house',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id,
                'amenities': [amenity.id]
            })
            assert len(place.amenities) == 1
            assert place.amenities[0].id == amenity.id

    def test_create_place_owner_not_found(self, app):
        """Test creating place with non-existent owner fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            with pytest.raises(ValueError) as exc:
                facade.create_place({
                    'title': 'Beach House',
                    'description': 'A lovely beach house',
                    'price': 150.0,
                    'latitude': 25.7617,
                    'longitude': -80.1918,
                    'owner_id': 'nonexistent-id'
                })
            assert "Owner not found" in str(exc.value)

    def test_get_place(self, app):
        """Test getting a place by ID."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            created = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            retrieved = facade.get_place(created.id)
            assert retrieved.id == created.id

    def test_get_all_places(self, app):
        """Test getting all places."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            facade.create_place({
                'title': 'Mountain Cabin',
                'price': 200.0,
                'latitude': 40.0,
                'longitude': -105.0,
                'owner_id': owner.id
            })
            places = facade.get_all_places()
            assert len(places) == 2

    def test_update_place(self, app):
        """Test updating a place."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            created = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            updated = facade.update_place(
                created.id, {'title': 'Ocean View House'})
            assert updated.title == 'Ocean View House'

    def test_delete_place(self, app):
        """Test deleting a place."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            created = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            result = facade.delete_place(created.id)
            assert result is True
            assert facade.get_place(created.id) is None

    # ==================== Review Tests ====================

    def test_create_review(self, app):
        """Test creating a review."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            review = facade.create_review({
                'text': 'Great place!',
                'rating': 5,
                'user_id': reviewer.id,
                'place_id': place.id
            })
            assert review.text == 'Great place!'
            assert review.rating == 5

    def test_create_review_own_place_fails(self, app):
        """Test creating a review for own place fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            with pytest.raises(ValueError) as exc:
                facade.create_review({
                    'text': 'Great place!',
                    'rating': 5,
                    'user_id': owner.id,
                    'place_id': place.id
                })
            assert "Cannot review your own place" in str(exc.value)

    def test_create_review_place_not_found(self, app):
        """Test creating review for non-existent place fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            with pytest.raises(ValueError) as exc:
                facade.create_review({
                    'text': 'Great place!',
                    'rating': 5,
                    'user_id': reviewer.id,
                    'place_id': 'nonexistent-id'
                })
            assert "Place not found" in str(exc.value)

    def test_create_review_user_not_found(self, app):
        """Test creating review with non-existent user fails."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            with pytest.raises(ValueError) as exc:
                facade.create_review({
                    'text': 'Great place!',
                    'rating': 5,
                    'user_id': 'nonexistent-id',
                    'place_id': place.id
                })
            assert "User not found" in str(exc.value)

    def test_get_review(self, app):
        """Test getting a review by ID."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            created = facade.create_review({
                'text': 'Great place!',
                'rating': 5,
                'user_id': reviewer.id,
                'place_id': place.id
            })
            retrieved = facade.get_review(created.id)
            assert retrieved.id == created.id

    def test_get_all_reviews(self, app):
        """Test getting all reviews."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            facade.create_review({
                'text': 'Great place!',
                'rating': 5,
                'user_id': reviewer.id,
                'place_id': place.id
            })
            reviews = facade.get_all_reviews()
            assert len(reviews) == 1

    def test_get_reviews_by_place(self, app):
        """Test getting reviews by place."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer1 = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            reviewer2 = facade.create_user({
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'email': 'bob@example.com',
                'password': 'password789'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            facade.create_review({
                'text': 'Great place!',
                'rating': 5,
                'user_id': reviewer1.id,
                'place_id': place.id
            })
            facade.create_review({
                'text': 'Nice!',
                'rating': 4,
                'user_id': reviewer2.id,
                'place_id': place.id
            })
            reviews = facade.get_reviews_by_place(place.id)
            assert len(reviews) == 2

    def test_update_review(self, app):
        """Test updating a review."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            created = facade.create_review({
                'text': 'Good place',
                'rating': 4,
                'user_id': reviewer.id,
                'place_id': place.id
            })
            updated = facade.update_review(
                created.id, {'text': 'Great place!', 'rating': 5})
            assert updated.text == 'Great place!'
            assert updated.rating == 5

    def test_delete_review(self, app):
        """Test deleting a review."""
        from app.services.facade import HBnBFacade
        with app.app_context():
            facade = HBnBFacade()
            owner = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            })
            reviewer = facade.create_user({
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'password': 'password456'
            })
            place = facade.create_place({
                'title': 'Beach House',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': owner.id
            })
            created = facade.create_review({
                'text': 'Great place!',
                'rating': 5,
                'user_id': reviewer.id,
                'place_id': place.id
            })
            result = facade.delete_review(created.id)
            assert result is True
            assert facade.get_review(created.id) is None
