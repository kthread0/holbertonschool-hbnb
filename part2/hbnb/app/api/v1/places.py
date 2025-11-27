"""Places API endpoints for the HBnB application."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place/Listing operations')

# Model for amenity within place
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

# Model for owner within place
owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

# Model for place input
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Model for place output
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner user ID'),
    'owner': fields.Nested(owner_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class PlaceList(Resource):
    """Resource for handling place collection operations."""

    @api.doc('list_places')
    @api.marshal_list_with(place_output_model)
    def get(self):
        """List all places (public endpoint).

        Returns:
            List of all places.
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places]

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new place (requires authentication).

        Returns:
            The created place data.
        """
        current_user_id = get_jwt_identity()
        try:
            # Set the owner_id to the authenticated user's ID
            place_data = api.payload.copy()
            place_data['owner_id'] = current_user_id
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            if 'Owner not found' in str(e):
                api.abort(404, str(e))
            api.abort(400, str(e))


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Resource for handling single place operations."""

    @api.doc('get_place')
    @api.marshal_with(place_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID (public endpoint).

        Args:
            place_id: The place's unique identifier.

        Returns:
            The place data.
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict()

    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_output_model)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Validation Error')
    @jwt_required()
    def put(self, place_id):
        """Update a place (owner or admin only).

        Args:
            place_id: The place's unique identifier.

        Returns:
            The updated place data.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        # Check ownership (unless admin)
        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_place')
    @api.response(204, 'Place deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (owner or admin only).

        Args:
            place_id: The place's unique identifier.

        Returns:
            Empty response on success.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        # Check ownership (unless admin)
        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        success = facade.delete_place(place_id)
        if not success:
            api.abort(404, 'Place not found')
        return '', 204
