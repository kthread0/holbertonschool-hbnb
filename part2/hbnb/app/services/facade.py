"""Facade pattern implementation for the HBnB business logic layer."""

from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repositories import (
    UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
)
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade class providing a unified interface to the business logic.

    Acts as the interface between the presentation layer (API) and
    the business logic/persistence layers.
    """

    def __init__(self):
        """Initialize repositories for all entity types."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ==================== User Methods ====================

    def create_user(self, user_data):
        """Create a new user.

        Args:
            user_data: Dictionary with user attributes.

        Returns:
            The created User instance.

        Raises:
            ValueError: If email already exists.
        """
        existing_user = self.user_repo.get_by_attribute(
            'email', user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password', ''),
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID.

        Args:
            user_id: ID of the user.

        Returns:
            User instance or None.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email.

        Args:
            email: User's email address.

        Returns:
            User instance or None.
        """
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users.

        Returns:
            List of all User instances.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information.

        Args:
            user_id: ID of the user to update.
            user_data: Dictionary with updated attributes.

        Returns:
            Updated User instance or None.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Check if email is being updated and if it's unique
        if 'email' in user_data and user_data['email'] != user.email:
            existing = self.user_repo.get_by_attribute(
                'email', user_data['email'])
            if existing:
                raise ValueError("Email already registered")

        # Handle password update - hash the new password
        if 'password' in user_data:
            user.hash_password(user_data.pop('password'))

        # Update other fields
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save()
        return user

    def delete_user(self, user_id):
        """Delete a user.

        Args:
            user_id: ID of the user to delete.

        Returns:
            True if deleted, False otherwise.
        """
        return self.user_repo.delete(user_id)

    # ==================== Place Methods ====================

    def create_place(self, place_data):
        """Create a new place.

        Args:
            place_data: Dictionary with place attributes.

        Returns:
            The created Place instance.

        Raises:
            ValueError: If owner not found.
        """
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner
        )

        # Handle amenities if provided
        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID.

        Args:
            place_id: ID of the place.

        Returns:
            Place instance or None.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places.

        Returns:
            List of all Place instances.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information.

        Args:
            place_id: ID of the place to update.
            place_data: Dictionary with updated attributes.

        Returns:
            Updated Place instance or None.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        # Update other fields
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        place.save()
        return place

    def delete_place(self, place_id):
        """Delete a place.

        Args:
            place_id: ID of the place to delete.

        Returns:
            True if deleted, False otherwise.
        """
        return self.place_repo.delete(place_id)

    # ==================== Review Methods ====================

    def create_review(self, review_data):
        """Create a new review.

        Args:
            review_data: Dictionary with review attributes.

        Returns:
            The created Review instance.

        Raises:
            ValueError: If place or user not found.
        """
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')

        place = self.place_repo.get(place_id)
        user = self.user_repo.get(user_id)

        if not place:
            raise ValueError("Place not found")
        if not user:
            raise ValueError("User not found")

        # Check if user is not the owner
        if place.owner_id == user_id:
            raise ValueError("Cannot review your own place")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID.

        Args:
            review_id: ID of the review.

        Returns:
            Review instance or None.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews.

        Returns:
            List of all Review instances.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place.

        Args:
            place_id: ID of the place.

        Returns:
            List of Review instances for the place.
        """
        return self.review_repo.get_reviews_by_place(place_id)

    def update_review(self, review_id, review_data):
        """Update a review's information.

        Args:
            review_id: ID of the review to update.
            review_data: Dictionary with updated attributes.

        Returns:
            Updated Review instance or None.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Only update text and rating
        for key in ['text', 'rating']:
            if key in review_data:
                setattr(review, key, review_data[key])

        review.save()
        return review

    def delete_review(self, review_id):
        """Delete a review.

        Args:
            review_id: ID of the review to delete.

        Returns:
            True if deleted, False otherwise.
        """
        return self.review_repo.delete(review_id)

    # ==================== Amenity Methods ====================

    def create_amenity(self, amenity_data):
        """Create a new amenity.

        Args:
            amenity_data: Dictionary with amenity attributes.

        Returns:
            The created Amenity instance.
        """
        amenity = Amenity(
            name=amenity_data.get('name'),
            description=amenity_data.get('description', '')
        )
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID.

        Args:
            amenity_id: ID of the amenity.

        Returns:
            Amenity instance or None.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities.

        Returns:
            List of all Amenity instances.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information.

        Args:
            amenity_id: ID of the amenity to update.
            amenity_data: Dictionary with updated attributes.

        Returns:
            Updated Amenity instance or None.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)

        amenity.save()
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete an amenity.

        Args:
            amenity_id: ID of the amenity to delete.

        Returns:
            True if deleted, False otherwise.
        """
        return self.amenity_repo.delete(amenity_id)
