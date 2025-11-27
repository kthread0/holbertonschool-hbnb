"""Place/Listing model for the HBnB application."""

from app.extensions import db
from app.models import BaseModel

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'),
              primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'),
              primary_key=True)
)


class Place(BaseModel):
    """Place class representing a listing in the system.

    Attributes:
        title: Place title (max 100 chars).
        description: Place description.
        price: Price per night (positive float).
        latitude: Geographic latitude (-90 to 90).
        longitude: Geographic longitude (-180 to 180).
        owner_id: ID of the user who owns the place.
        amenities: List of amenities available.
        reviews: List of reviews for the place.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                         nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True,
                              cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude,
                 owner=None, owner_id=None):
        """Initialize a new Place instance.

        Args:
            title: Place title.
            description: Place description.
            price: Price per night.
            latitude: Geographic latitude.
            longitude: Geographic longitude.
            owner: User instance who owns the place (optional).
            owner_id: ID of owner (used if owner object not provided).
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if owner:
            self.owner_id = owner.id
        elif owner_id:
            self.owner_id = owner_id
        self._validate()

    def _validate(self):
        """Validate place attributes."""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be <= 100 characters")
        if self.price is None or self.price < 0:
            raise ValueError("Price must be a positive value")
        if self.latitude is not None and (self.latitude < -90 or
                                          self.latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        if self.longitude is not None and (self.longitude < -180 or
                                           self.longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")

    def add_amenity(self, amenity):
        """Add an amenity to the place.

        Args:
            amenity: Amenity instance to add.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place.

        Args:
            amenity: Amenity instance to remove.
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def add_review(self, review):
        """Add a review to the place.

        Args:
            review: Review instance to add.
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """Convert place to dictionary representation.

        Returns:
            Dictionary with place data.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [a.to_dict() for a in self.amenities] if self.amenities else [],
            'reviews': [r.to_dict() for r in self.reviews] if self.reviews else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
