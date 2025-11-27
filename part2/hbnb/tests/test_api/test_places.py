"""Tests for the Places API endpoints."""

import pytest
import uuid


class TestPlacesAPI:
    """Test cases for Places API."""

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

    def create_owner(self, client, app):
        """Create a test owner and return id and token."""
        unique_email = f"owner_{uuid.uuid4().hex[:8]}@example.com"
        token = self.get_auth_token(client, unique_email, 'password123')

        from app.services.facade import HBnBFacade
        facade = HBnBFacade()
        user = facade.get_user_by_email(unique_email)
        return user.id, token

    def test_create_place(self, client, app):
        """Test creating a place via API."""
        with app.app_context():
            owner_id, token = self.create_owner(client, app)
            response = client.post('/api/v1/places/',
                                   json={
                                       'title': 'Beach House',
                                       'description': 'A lovely beach house',
                                       'price': 150.0,
                                       'latitude': 25.7617,
                                       'longitude': -80.1918,
                                       'owner_id': owner_id
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 201
            data = response.get_json()
            assert data['title'] == 'Beach House'

    def test_create_place_invalid_owner(self, client, app):
        """Test creating place with invalid owner fails."""
        with app.app_context():
            _, token = self.create_owner(client, app)
            # The API uses the JWT identity for owner, so this will create with the token owner
            # Test directly creating with bad owner through facade
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            import pytest
            with pytest.raises(ValueError):
                facade.create_place({
                    'title': 'Beach House',
                    'description': 'A lovely beach house',
                    'price': 150.0,
                    'latitude': 25.7617,
                    'longitude': -80.1918,
                    'owner_id': 'nonexistent-id'
                })

    def test_create_place_invalid_price(self, client, app):
        """Test creating place with negative price fails."""
        with app.app_context():
            owner_id, token = self.create_owner(client, app)
            response = client.post('/api/v1/places/',
                                   json={
                                       'title': 'Beach House',
                                       'description': 'A lovely beach house',
                                       'price': -50.0,
                                       'latitude': 25.7617,
                                       'longitude': -80.1918,
                                       'owner_id': owner_id
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 400

    def test_get_all_places(self, client, app):
        """Test getting all places."""
        with app.app_context():
            owner_id, token = self.create_owner(client, app)
            # Create a place first
            client.post('/api/v1/places/',
                        json={
                            'title': 'Beach House',
                            'description': 'A lovely beach house',
                            'price': 150.0,
                            'latitude': 25.7617,
                            'longitude': -80.1918,
                            'owner_id': owner_id
                        },
                        headers={'Authorization': f'Bearer {token}'})
            response = client.get('/api/v1/places/')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)

    def test_get_place_by_id(self, client, app):
        """Test getting a place by ID."""
        with app.app_context():
            owner_id, token = self.create_owner(client, app)
            # Create a place first
            create_response = client.post('/api/v1/places/',
                                          json={
                                              'title': 'Beach House',
                                              'description': 'A lovely beach house',
                                              'price': 150.0,
                                              'latitude': 25.7617,
                                              'longitude': -80.1918,
                                              'owner_id': owner_id
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            place_id = create_response.get_json()['id']

            response = client.get(f'/api/v1/places/{place_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == place_id

    def test_get_place_not_found(self, client, app):
        """Test getting non-existent place returns 404."""
        with app.app_context():
            response = client.get('/api/v1/places/nonexistent-id')
            assert response.status_code == 404

    def test_update_place(self, client, app):
        """Test updating a place."""
        with app.app_context():
            owner_id, token = self.create_owner(client, app)
            # Create a place first
            create_response = client.post('/api/v1/places/',
                                          json={
                                              'title': 'Beach House',
                                              'description': 'A lovely beach house',
                                              'price': 150.0,
                                              'latitude': 25.7617,
                                              'longitude': -80.1918,
                                              'owner_id': owner_id
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            place_id = create_response.get_json()['id']

            response = client.put(f'/api/v1/places/{place_id}',
                                  json={
                'title': 'Ocean View House',
                'description': 'A lovely beach house',
                'price': 200.0,
                'latitude': 25.7617,
                'longitude': -80.1918
            },
                headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 200
            data = response.get_json()
            assert data['title'] == 'Ocean View House'

    def test_delete_place(self, client, app):
        """Test deleting a place."""
        with app.app_context():
            # Get admin token for delete
            admin_token = self.get_auth_token(
                client, 'admin_place@test.com', 'admin123', is_admin=True)

            owner_id, token = self.create_owner(client, app)
            # Create a place first
            create_response = client.post('/api/v1/places/',
                                          json={
                                              'title': 'Beach House',
                                              'description': 'A lovely beach house',
                                              'price': 150.0,
                                              'latitude': 25.7617,
                                              'longitude': -80.1918,
                                              'owner_id': owner_id
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            place_id = create_response.get_json()['id']

            # Owner can delete their own place
            response = client.delete(f'/api/v1/places/{place_id}',
                                     headers={'Authorization': f'Bearer {token}'})
            assert response.status_code in [200, 204]
