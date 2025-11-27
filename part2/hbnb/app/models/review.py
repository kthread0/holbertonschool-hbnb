"""Review model for the HBnB application."""

from app.extensions import db
from app.models import BaseModel


class Review(BaseModel):
    """Review class representing a review in the system.

    Attributes:
        text: Review text content.
        rating: Rating from 1 to 5.
        place_id: ID of the place being reviewed.
        user_id: ID of the user who wrote the review.
    """
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'),
                         nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                        nullable=False)

    # Add unique constraint to ensure one review per user per place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id',
                            name='unique_user_place_review'),
    )

    def __init__(self, text, rating, place=None, user=None,
                 place_id=None, user_id=None):
        """Initialize a new Review instance.

        Args:
            text: Review text content.
            rating: Rating value (1-5).
            place: Place instance being reviewed (optional).
            user: User instance who wrote the review (optional).
            place_id: ID of place (used if place object not provided).
            user_id: ID of user (used if user object not provided).
        """
        super().__init__()
        self.text = text
        self.rating = rating
        if place:
            self.place_id = place.id
        elif place_id:
            self.place_id = place_id
        if user:
            self.user_id = user.id
        elif user_id:
            self.user_id = user_id
        self._validate()

    def _validate(self):
        """Validate review attributes."""
        if not self.text:
            raise ValueError("Review text is required")
        if self.rating is None or self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not self.place_id:
            raise ValueError("Place is required")
        if not self.user_id:
            raise ValueError("User is required")

    def to_dict(self):
        """Convert review to dictionary representation.

        Returns:
            Dictionary with review data.
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
