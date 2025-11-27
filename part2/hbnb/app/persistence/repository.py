"""Repository pattern implementation for data persistence."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repository pattern.

    Defines the interface for data persistence operations.
    """

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository.

        Args:
            obj: Object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID.

        Args:
            obj_id: ID of the object to retrieve.

        Returns:
            The object if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository.

        Returns:
            List of all objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object with new data.

        Args:
            obj_id: ID of the object to update.
            data: Dictionary with updated attributes.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object from the repository.

        Args:
            obj_id: ID of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value.

        Args:
            attr_name: Name of the attribute.
            attr_value: Value to match.

        Returns:
            The first matching object, or None.
        """
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface.

    Stores objects in a dictionary for quick access by ID.
    """

    def __init__(self):
        """Initialize the in-memory storage."""
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository.

        Args:
            obj: Object to add (must have an 'id' attribute).
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID.

        Args:
            obj_id: ID of the object to retrieve.

        Returns:
            The object if found, None otherwise.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects from the repository.

        Returns:
            List of all objects.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with new data.

        Args:
            obj_id: ID of the object to update.
            data: Dictionary with updated attributes.

        Returns:
            The updated object if found, None otherwise.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object from the repository.

        Args:
            obj_id: ID of the object to delete.

        Returns:
            True if deleted, False if not found.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value.

        Args:
            attr_name: Name of the attribute.
            attr_value: Value to match.

        Returns:
            The first matching object, or None.
        """
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None
        )

    def get_all_by_attribute(self, attr_name, attr_value):
        """Retrieve all objects matching a specific attribute value.

        Args:
            attr_name: Name of the attribute.
            attr_value: Value to match.

        Returns:
            List of all matching objects.
        """
        return [
            obj for obj in self._storage.values()
            if getattr(obj, attr_name, None) == attr_value
        ]


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the Repository interface.

    Uses SQLAlchemy for database persistence.
    """

    def __init__(self, model):
        """Initialize with a SQLAlchemy model class.

        Args:
            model: The SQLAlchemy model class to use.
        """
        self.model = model

    @property
    def db(self):
        """Lazy import of db to avoid circular imports."""
        from app.extensions import db
        return db

    def add(self, obj):
        """Add an object to the database.

        Args:
            obj: SQLAlchemy model instance to add.
        """
        self.db.session.add(obj)
        self.db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID.

        Args:
            obj_id: ID of the object to retrieve.

        Returns:
            The object if found, None otherwise.
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects from the database.

        Returns:
            List of all objects.
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with new data.

        Args:
            obj_id: ID of the object to update.
            data: Dictionary with updated attributes.

        Returns:
            The updated object if found, None otherwise.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object from the database.

        Args:
            obj_id: ID of the object to delete.

        Returns:
            True if deleted, False if not found.
        """
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value.

        Args:
            attr_name: Name of the attribute.
            attr_value: Value to match.

        Returns:
            The first matching object, or None.
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

    def get_all_by_attribute(self, attr_name, attr_value):
        """Retrieve all objects matching a specific attribute value.

        Args:
            attr_name: Name of the attribute.
            attr_value: Value to match.

        Returns:
            List of all matching objects.
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).all()
