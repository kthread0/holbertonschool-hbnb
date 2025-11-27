"""Tests for the Amenities API endpoints."""

import pytest
import uuid


class TestAmenitiesAPI:
    """Test cases for Amenities API."""

    def get_admin_token(self, client):
        """Helper to get admin JWT token."""
        from app.services.facade import HBnBFacade
        from flask import current_app
        admin_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"
        with current_app.app_context():
            facade = HBnBFacade()
            try:
                facade.create_user({
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'email': admin_email,
                    'password': 'admin123',
                    'is_admin': True
                })
            except ValueError:
                pass  # Already exists

        response = client.post('/api/v1/auth/login', json={
            'email': admin_email,
            'password': 'admin123'
        })
        return response.get_json().get('access_token')

    def test_create_amenity(self, client, app):
        """Test creating an amenity via API."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/amenities/',
                                   json={
                                       'name': 'WiFi',
                                       'description': 'High-speed internet'
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 201
            data = response.get_json()
            assert data['name'] == 'WiFi'

    def test_create_amenity_without_description(self, client, app):
        """Test creating amenity without description."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/amenities/',
                                   json={
                                       'name': 'Pool'
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 201
            data = response.get_json()
            assert data['name'] == 'Pool'

    def test_create_amenity_invalid_name_empty(self, client, app):
        """Test creating amenity with empty name fails."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/amenities/',
                                   json={
                                       'name': ''
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 400

    def test_create_amenity_name_too_long(self, client, app):
        """Test creating amenity with name over 50 chars fails."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/amenities/',
                                   json={
                                       'name': 'A' * 51
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 400

    def test_get_all_amenities(self, client, app):
        """Test getting all amenities."""
        with app.app_context():
            token = self.get_admin_token(client)
            # Create an amenity first
            client.post('/api/v1/amenities/',
                        json={'name': 'WiFi'},
                        headers={'Authorization': f'Bearer {token}'})
            response = client.get('/api/v1/amenities/')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)

    def test_get_amenity_by_id(self, client, app):
        """Test getting an amenity by ID."""
        with app.app_context():
            token = self.get_admin_token(client)
            # Create an amenity first
            create_response = client.post('/api/v1/amenities/',
                                          json={'name': 'WiFi'},
                                          headers={'Authorization': f'Bearer {token}'})
            amenity_id = create_response.get_json()['id']

            response = client.get(f'/api/v1/amenities/{amenity_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == amenity_id

    def test_get_amenity_not_found(self, client, app):
        """Test getting non-existent amenity returns 404."""
        with app.app_context():
            response = client.get('/api/v1/amenities/nonexistent-id')
            assert response.status_code == 404

    def test_update_amenity(self, client, app):
        """Test updating an amenity."""
        with app.app_context():
            token = self.get_admin_token(client)
            # Create an amenity first
            create_response = client.post('/api/v1/amenities/',
                                          json={'name': 'WiFi'},
                                          headers={'Authorization': f'Bearer {token}'})
            amenity_id = create_response.get_json()['id']

            response = client.put(f'/api/v1/amenities/{amenity_id}',
                                  json={'name': 'Fast WiFi'},
                                  headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == 'Fast WiFi'

    def test_update_amenity_not_found(self, client, app):
        """Test updating non-existent amenity returns 404."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.put('/api/v1/amenities/nonexistent-id',
                                  json={'name': 'Fast WiFi'},
                                  headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 404

    def test_delete_amenity(self, client, app):
        """Test deleting an amenity."""
        with app.app_context():
            token = self.get_admin_token(client)
            # Create an amenity first
            create_response = client.post('/api/v1/amenities/',
                                          json={'name': 'WiFi'},
                                          headers={'Authorization': f'Bearer {token}'})
            amenity_id = create_response.get_json()['id']

            response = client.delete(f'/api/v1/amenities/{amenity_id}',
                                     headers={'Authorization': f'Bearer {token}'})
            assert response.status_code in [200, 204]

            # Verify amenity is deleted
            get_response = client.get(f'/api/v1/amenities/{amenity_id}')
            assert get_response.status_code == 404

    def test_delete_amenity_not_found(self, client, app):
        """Test deleting non-existent amenity returns 404."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.delete('/api/v1/amenities/nonexistent-id',
                                     headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 404
