"""Users API endpoints for the HBnB application."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Model for user input/output
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class UserList(Resource):
    """Resource for handling user collection operations."""

    @api.doc('list_users')
    @api.marshal_list_with(user_output_model)
    def get(self):
        """List all users.

        Returns:
            List of all users.
        """
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only).

        Returns:
            The created user data.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')

        try:
            # Check if email is already in use
            email = api.payload.get('email')
            if facade.get_user_by_email(email):
                api.abort(400, 'Email already registered')

            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Resource for handling single user operations."""

    @api.doc('get_user')
    @api.marshal_with(user_output_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID.

        Args:
            user_id: The user's unique identifier.

        Returns:
            The user data (password excluded).
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_output_model)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Validation Error')
    @jwt_required()
    def put(self, user_id):
        """Update a user (self or admin only).

        Regular users can only update their own first_name and last_name.
        Admins can update any user's data including email and password.

        Args:
            user_id: The user's unique identifier.

        Returns:
            The updated user data.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')

        # Check authorization
        if not is_admin and current_user_id != user_id:
            api.abort(403, 'Unauthorized action')

        # Regular users cannot modify email or password
        payload = api.payload.copy()
        if not is_admin:
            if 'email' in payload or 'password' in payload:
                api.abort(400, 'You cannot modify email or password')

        # If admin is updating email, check for uniqueness
        if is_admin and 'email' in payload:
            existing_user = facade.get_user_by_email(payload['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, 'Email already in use')

        try:
            updated_user = facade.update_user(user_id, payload)
            return updated_user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user (admin only).

        Args:
            user_id: The user's unique identifier.

        Returns:
            Empty response on success.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')

        success = facade.delete_user(user_id)
        if not success:
            api.abort(404, 'User not found')
        return '', 204
