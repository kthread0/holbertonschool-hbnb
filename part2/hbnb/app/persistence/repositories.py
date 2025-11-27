"""Entity-specific repositories for the HBnB application."""

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class UserRepository(SQLAlchemyRepository):
    """Repository for User entity with custom methods."""

    def __init__(self):
        """Initialize the UserRepository."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email.

        Args:
            email: User's email address.

        Returns:
            User instance or None.
        """
        return self.model.query.filter_by(email=email).first()


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with custom methods."""

    def __init__(self):
        """Initialize the PlaceRepository."""
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Retrieve all places owned by a user.

        Args:
            owner_id: ID of the owner.

        Returns:
            List of Place instances.
        """
        return self.model.query.filter_by(owner_id=owner_id).all()


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity with custom methods."""

    def __init__(self):
        """Initialize the ReviewRepository."""
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a place.

        Args:
            place_id: ID of the place.

        Returns:
            List of Review instances.
        """
        return self.model.query.filter_by(place_id=place_id).all()

    def get_reviews_by_user(self, user_id):
        """Retrieve all reviews by a user.

        Args:
            user_id: ID of the user.

        Returns:
            List of Review instances.
        """
        return self.model.query.filter_by(user_id=user_id).all()


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity with custom methods."""

    def __init__(self):
        """Initialize the AmenityRepository."""
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name.

        Args:
            name: Amenity name.

        Returns:
            Amenity instance or None.
        """
        return self.model.query.filter_by(name=name).first()
