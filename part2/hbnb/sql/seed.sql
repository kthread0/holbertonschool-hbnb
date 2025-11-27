-- SQL Script for Initial Data Population
-- This script inserts the administrator user and initial amenities

-- Insert Administrator User
-- Password: admin1234 (hashed with bcrypt)
-- Note: The password hash below was generated using bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcSAg/9S2',  -- bcrypt hash of 'admin1234'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, description, created_at, updated_at)
VALUES 
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'WiFi', 'Wireless Internet Access', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Swimming Pool', 'Outdoor swimming pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'Air Conditioning', 'Central air conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Verify the data was inserted correctly
SELECT 'Users inserted:' as status, COUNT(*) as count FROM users;
SELECT 'Amenities inserted:' as status, COUNT(*) as count FROM amenities;
