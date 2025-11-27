"""Application factory for the HBnB application."""

from flask import Flask
from app.extensions import db, bcrypt, jwt


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to use (default: DevelopmentConfig).

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize API (import here to avoid circular imports)
    from app.api.v1 import init_api
    init_api(app)

    return app
