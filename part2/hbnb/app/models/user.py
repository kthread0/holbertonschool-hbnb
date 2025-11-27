"""User model for the HBnB application."""

import re
from app.extensions import db, bcrypt
from app.models import BaseModel


class User(BaseModel):
    """User class representing a user in the system.

    Attributes:
        first_name: User's first name (max 50 chars).
        last_name: User's last name (max 50 chars).
        email: User's unique email address.
        password: User's hashed password.
        is_admin: Whether the user has admin privileges.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships will be added later
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password="", is_admin=False):
        """Initialize a new User instance.

        Args:
            first_name: User's first name.
            last_name: User's last name.
            email: User's email address.
            password: User's password (will be hashed).
            is_admin: Admin status (default False).
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)
        else:
            self.password = ""
        self._validate()

    def _validate(self):
        """Validate user attributes."""
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError(
                "First name is required and must be <= 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError(
                "Last name is required and must be <= 50 characters")
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")

    @staticmethod
    def _is_valid_email(email):
        """Validate email format using regex.

        Args:
            email: Email string to validate.

        Returns:
            Boolean indicating if email is valid.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def hash_password(self, password):
        """Hash the password before storing it.

        Args:
            password: Plain text password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify if the provided password matches the hashed password.

        Args:
            password: Plain text password to verify.

        Returns:
            Boolean indicating if password matches.
        """
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place to user's owned places.

        Args:
            place: Place instance to add.
        """
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Add a review to user's reviews.

        Args:
            review: Review instance to add.
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """Convert user to dictionary representation.

        Note: Password is never returned.

        Returns:
            Dictionary with user data.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
