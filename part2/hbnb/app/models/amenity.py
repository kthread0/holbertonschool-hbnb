"""Amenity model for the HBnB application."""

from app.extensions import db
from app.models import BaseModel


class Amenity(BaseModel):
    """Amenity class representing an amenity for places.

    Attributes:
        name: Amenity name (max 50 chars, unique).
        description: Optional description of the amenity.
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description=""):
        """Initialize a new Amenity instance.

        Args:
            name: Amenity name.
            description: Optional description.
        """
        super().__init__()
        self.name = name
        self.description = description
        self._validate()

    def _validate(self):
        """Validate amenity attributes."""
        if not self.name or len(self.name) > 50:
            raise ValueError(
                "Amenity name is required and must be <= 50 characters")

    def to_dict(self):
        """Convert amenity to dictionary representation.

        Returns:
            Dictionary with amenity data.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
