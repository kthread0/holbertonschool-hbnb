"""Tests for the Reviews API endpoints."""

import pytest
import uuid


class TestReviewsAPI:
    """Test cases for Reviews API."""

    def get_auth_token(self, client, email, password, is_admin=False):
        """Helper to get JWT token."""
        from app.services.facade import HBnBFacade
        from flask import current_app
        with current_app.app_context():
            facade = HBnBFacade()
            try:
                facade.create_user({
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': email,
                    'password': password,
                    'is_admin': is_admin
                })
            except ValueError:
                pass  # Already exists

        response = client.post('/api/v1/auth/login', json={
            'email': email,
            'password': password
        })
        return response.get_json().get('access_token')

    def setup_place_and_users(self, client, app):
        """Create owner, reviewer, place and return their details."""
        from app.services.facade import HBnBFacade

        owner_email = f"owner_{uuid.uuid4().hex[:8]}@example.com"
        reviewer_email = f"reviewer_{uuid.uuid4().hex[:8]}@example.com"

        owner_token = self.get_auth_token(client, owner_email, 'password123')
        reviewer_token = self.get_auth_token(
            client, reviewer_email, 'password456')

        facade = HBnBFacade()
        owner = facade.get_user_by_email(owner_email)
        reviewer = facade.get_user_by_email(reviewer_email)

        # Create a place
        create_response = client.post('/api/v1/places/',
                                      json={
                                          'title': 'Beach House',
                                          'description': 'A lovely beach house',
                                          'price': 150.0,
                                          'latitude': 25.7617,
                                          'longitude': -80.1918,
                                          'owner_id': owner.id
                                      },
                                      headers={'Authorization': f'Bearer {owner_token}'})
        place_id = create_response.get_json()['id']

        return {
            'owner_id': owner.id,
            'owner_token': owner_token,
            'reviewer_id': reviewer.id,
            'reviewer_token': reviewer_token,
            'place_id': place_id
        }

    def test_create_review(self, client, app):
        """Test creating a review via API."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            response = client.post('/api/v1/reviews/',
                                   json={
                                       'text': 'Great place!',
                                       'rating': 5,
                                       'user_id': data['reviewer_id'],
                                       'place_id': data['place_id']
                                   },
                                   headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            assert response.status_code == 201
            result = response.get_json()
            assert result['text'] == 'Great place!'
            assert result['rating'] == 5

    def test_create_review_own_place_fails(self, client, app):
        """Test creating a review for own place fails."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            response = client.post('/api/v1/reviews/',
                                   json={
                                       'text': 'Great place!',
                                       'rating': 5,
                                       'user_id': data['owner_id'],
                                       'place_id': data['place_id']
                                   },
                                   headers={'Authorization': f"Bearer {data['owner_token']}"})
            assert response.status_code == 400

    def test_create_review_invalid_rating(self, client, app):
        """Test creating review with invalid rating fails."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            response = client.post('/api/v1/reviews/',
                                   json={
                                       'text': 'Great place!',
                                       'rating': 10,
                                       'user_id': data['reviewer_id'],
                                       'place_id': data['place_id']
                                   },
                                   headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            assert response.status_code == 400

    def test_create_review_place_not_found(self, client, app):
        """Test creating review for non-existent place fails."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            response = client.post('/api/v1/reviews/',
                                   json={
                                       'text': 'Great place!',
                                       'rating': 5,
                                       'user_id': data['reviewer_id'],
                                       'place_id': 'nonexistent-id'
                                   },
                                   headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            assert response.status_code in [400, 404]

    def test_get_all_reviews(self, client, app):
        """Test getting all reviews."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            # Create a review first
            client.post('/api/v1/reviews/',
                        json={
                            'text': 'Great place!',
                            'rating': 5,
                            'user_id': data['reviewer_id'],
                            'place_id': data['place_id']
                        },
                        headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            response = client.get('/api/v1/reviews/')
            assert response.status_code == 200
            result = response.get_json()
            assert isinstance(result, list)

    def test_get_review_by_id(self, client, app):
        """Test getting a review by ID."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            # Create a review first
            create_response = client.post('/api/v1/reviews/',
                                          json={
                                              'text': 'Great place!',
                                              'rating': 5,
                                              'user_id': data['reviewer_id'],
                                              'place_id': data['place_id']
                                          },
                                          headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            review_id = create_response.get_json()['id']

            response = client.get(f'/api/v1/reviews/{review_id}')
            assert response.status_code == 200
            result = response.get_json()
            assert result['id'] == review_id

    def test_get_review_not_found(self, client, app):
        """Test getting non-existent review returns 404."""
        with app.app_context():
            response = client.get('/api/v1/reviews/nonexistent-id')
            assert response.status_code == 404

    def test_update_review(self, client, app):
        """Test updating a review."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            # Create a review first
            create_response = client.post('/api/v1/reviews/',
                                          json={
                                              'text': 'Good place',
                                              'rating': 4,
                                              'user_id': data['reviewer_id'],
                                              'place_id': data['place_id']
                                          },
                                          headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            review_id = create_response.get_json()['id']

            response = client.put(f'/api/v1/reviews/{review_id}',
                                  json={
                'text': 'Great place!',
                'rating': 5
            },
                headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            assert response.status_code == 200
            result = response.get_json()
            assert result['text'] == 'Great place!'
            assert result['rating'] == 5

    def test_delete_review(self, client, app):
        """Test deleting a review."""
        with app.app_context():
            data = self.setup_place_and_users(client, app)
            # Create a review first
            create_response = client.post('/api/v1/reviews/',
                                          json={
                                              'text': 'Great place!',
                                              'rating': 5,
                                              'user_id': data['reviewer_id'],
                                              'place_id': data['place_id']
                                          },
                                          headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            review_id = create_response.get_json()['id']

            response = client.delete(f'/api/v1/reviews/{review_id}',
                                     headers={'Authorization': f"Bearer {data['reviewer_token']}"})
            assert response.status_code in [200, 204]

            # Verify review is deleted
            get_response = client.get(f'/api/v1/reviews/{review_id}')
            assert get_response.status_code == 404
