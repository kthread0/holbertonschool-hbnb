"""Reviews API endpoints for the HBnB application."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Model for review input
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

# Model for review output
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class ReviewList(Resource):
    """Resource for handling review collection operations."""

    @api.doc('list_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self):
        """List all reviews.

        Returns:
            List of all reviews.
        """
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews]

    @api.doc('create_review')
    @api.expect(review_model)
    @api.marshal_with(review_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication).

        Returns:
            The created review data.
        """
        current_user_id = get_jwt_identity()

        try:
            # Set user_id from JWT token
            review_data = api.payload.copy()
            review_data['user_id'] = current_user_id

            # Check if user owns the place (can't review own place)
            place = facade.get_place(review_data.get('place_id'))
            if not place:
                api.abort(404, 'Place not found')

            if place.owner_id == current_user_id:
                api.abort(400, 'You cannot review your own place')

            # Check if user already reviewed this place
            existing_reviews = facade.get_reviews_by_place(
                review_data.get('place_id'))
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    api.abort(400, 'You have already reviewed this place')

            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            if 'not found' in str(e):
                api.abort(404, str(e))
            api.abort(400, str(e))


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Resource for handling single review operations."""

    @api.doc('get_review')
    @api.marshal_with(review_output_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID.

        Args:
            review_id: The review's unique identifier.

        Returns:
            The review data.
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_model)
    @api.marshal_with(review_output_model)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Validation Error')
    @jwt_required()
    def put(self, review_id):
        """Update a review (owner or admin only).

        Args:
            review_id: The review's unique identifier.

        Returns:
            The updated review data.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        # Check ownership (unless admin)
        if not is_admin and review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner or admin only).

        Args:
            review_id: The review's unique identifier.

        Returns:
            Empty response on success.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        # Check ownership (unless admin)
        if not is_admin and review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, 'Review not found')
        return '', 204


@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Resource for handling reviews for a specific place."""

    @api.doc('list_place_reviews')
    @api.marshal_list_with(review_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place.

        Args:
            place_id: The place's unique identifier.

        Returns:
            List of reviews for the place.
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews]
