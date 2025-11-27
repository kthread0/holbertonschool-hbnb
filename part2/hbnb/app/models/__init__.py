"""Models package for the HBnB application.

Provides base model and entity classes.
"""

import uuid
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """Base model class providing common attributes and methods.

    Attributes:
        id: Unique identifier (UUID).
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize base model attributes."""
        super().__init__(**kwargs)
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp and save to database."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary.

        Args:
            data: Dictionary with attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
