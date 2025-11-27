"""Services package for the HBnB application.

Provides the facade pattern implementation for business logic.
"""

from app.services.facade import HBnBFacade

# Singleton facade instance to be shared across the application
facade = HBnBFacade()
