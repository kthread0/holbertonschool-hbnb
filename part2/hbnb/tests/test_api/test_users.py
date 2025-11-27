"""Tests for the Users API endpoints."""

import pytest
import uuid


class TestUsersAPI:
    """Test cases for Users API."""

    def get_admin_token(self, client):
        """Helper to get admin JWT token."""
        # Create an admin user first
        from app.services.facade import HBnBFacade
        from flask import current_app
        with current_app.app_context():
            facade = HBnBFacade()
            try:
                facade.create_user({
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'email': 'admin@test.com',
                    'password': 'admin123',
                    'is_admin': True
                })
            except ValueError:
                pass  # Already exists

        # Login to get token
        response = client.post('/api/v1/auth/login', json={
            'email': 'admin@test.com',
            'password': 'admin123'
        })
        return response.get_json().get('access_token')

    def test_create_user(self, client, app):
        """Test creating a user via API."""
        with app.app_context():
            token = self.get_admin_token(client)
            unique_email = f"john_{uuid.uuid4().hex[:8]}@example.com"
            response = client.post('/api/v1/users/',
                                   json={
                                       'first_name': 'John',
                                       'last_name': 'Doe',
                                       'email': unique_email,
                                       'password': 'password123'
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 201
            data = response.get_json()
            assert data['first_name'] == 'John'
            assert data['email'] == unique_email
            assert 'id' in data

    def test_create_user_invalid_email(self, client, app):
        """Test creating user with invalid email fails."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/users/',
                                   json={
                                       'first_name': 'John',
                                       'last_name': 'Doe',
                                       'email': 'invalid-email',
                                       'password': 'password123'
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 400

    def test_create_user_missing_fields(self, client, app):
        """Test creating user with missing fields fails."""
        with app.app_context():
            token = self.get_admin_token(client)
            response = client.post('/api/v1/users/',
                                   json={
                                       'first_name': 'John'
                                   },
                                   headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 400

    def test_get_all_users(self, client, app):
        """Test getting all users."""
        with app.app_context():
            token = self.get_admin_token(client)
            unique_email = f"john_{uuid.uuid4().hex[:8]}@example.com"
            # Create a user first
            client.post('/api/v1/users/',
                        json={
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'email': unique_email,
                            'password': 'password123'
                        },
                        headers={'Authorization': f'Bearer {token}'})
            response = client.get('/api/v1/users/')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)

    def test_get_user_by_id(self, client, app):
        """Test getting a user by ID."""
        with app.app_context():
            token = self.get_admin_token(client)
            unique_email = f"john_{uuid.uuid4().hex[:8]}@example.com"
            # Create a user first
            create_response = client.post('/api/v1/users/',
                                          json={
                                              'first_name': 'John',
                                              'last_name': 'Doe',
                                              'email': unique_email,
                                              'password': 'password123'
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            user_id = create_response.get_json()['id']

            response = client.get(f'/api/v1/users/{user_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == user_id

    def test_get_user_not_found(self, client, app):
        """Test getting non-existent user returns 404."""
        with app.app_context():
            response = client.get('/api/v1/users/nonexistent-id')
            assert response.status_code == 404

    def test_update_user(self, client, app):
        """Test updating a user."""
        with app.app_context():
            token = self.get_admin_token(client)
            unique_email = f"john_{uuid.uuid4().hex[:8]}@example.com"
            # Create a user first
            create_response = client.post('/api/v1/users/',
                                          json={
                                              'first_name': 'John',
                                              'last_name': 'Doe',
                                              'email': unique_email,
                                              'password': 'password123'
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            user_id = create_response.get_json()['id']

            response = client.put(f'/api/v1/users/{user_id}',
                                  json={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': unique_email,
                'password': 'password123'
            },
                headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 200
            data = response.get_json()
            assert data['first_name'] == 'Jane'

    def test_delete_user(self, client, app):
        """Test deleting a user."""
        with app.app_context():
            token = self.get_admin_token(client)
            unique_email = f"john_{uuid.uuid4().hex[:8]}@example.com"
            # Create a user first
            create_response = client.post('/api/v1/users/',
                                          json={
                                              'first_name': 'John',
                                              'last_name': 'Doe',
                                              'email': unique_email,
                                              'password': 'password123'
                                          },
                                          headers={'Authorization': f'Bearer {token}'})
            user_id = create_response.get_json()['id']

            response = client.delete(f'/api/v1/users/{user_id}',
                                     headers={'Authorization': f'Bearer {token}'})
            assert response.status_code in [200, 204]

            # Verify user is deleted
            get_response = client.get(f'/api/v1/users/{user_id}')
            assert get_response.status_code == 404
