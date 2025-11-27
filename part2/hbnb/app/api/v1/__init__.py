"""API v1 package initialization.

Registers all API namespaces for version 1 of the HBnB API.
"""

from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns


def init_api(app):
    """Initialize the API with all namespaces.

    Args:
        app: Flask application instance.

    Returns:
        Configured Api instance.
    """
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API - A clone of AirBnB',
        doc='/api/v1/'
    )

    # Register namespaces
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return api
