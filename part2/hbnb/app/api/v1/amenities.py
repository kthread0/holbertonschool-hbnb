"""Amenities API endpoints for the HBnB application."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Model for amenity input
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name'),
    'description': fields.String(description='Amenity description')
})

# Model for amenity output
amenity_output_model = api.model('AmenityOutput', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Amenity description'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    """Resource for handling amenity collection operations."""

    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_output_model)
    def get(self):
        """List all amenities (public endpoint).

        Returns:
            List of all amenities.
        """
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only).

        Returns:
            The created amenity data.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')

        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Resource for handling single amenity operations."""

    @api.doc('get_amenity')
    @api.marshal_with(amenity_output_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get an amenity by ID (public endpoint).

        Args:
            amenity_id: The amenity's unique identifier.

        Returns:
            The amenity data.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_output_model)
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Validation Error')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only).

        Args:
            amenity_id: The amenity's unique identifier.

        Returns:
            The updated amenity data.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')

        try:
            amenity = facade.update_amenity(amenity_id, api.payload)
            if not amenity:
                api.abort(404, 'Amenity not found')
            return amenity.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity deleted')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only).

        Args:
            amenity_id: The amenity's unique identifier.

        Returns:
            Empty response on success.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')

        success = facade.delete_amenity(amenity_id)
        if not success:
            api.abort(404, 'Amenity not found')
        return '', 204
