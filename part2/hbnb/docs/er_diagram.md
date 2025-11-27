# HBnB Database ER Diagram

This document contains the Entity-Relationship diagram for the HBnB database schema.

```mermaid
erDiagram
    USER {
        string id PK "UUID"
        string first_name "VARCHAR(50)"
        string last_name "VARCHAR(50)"
        string email UK "VARCHAR(120)"
        string password "VARCHAR(128)"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at
        datetime updated_at
    }

    PLACE {
        string id PK "UUID"
        string title "VARCHAR(100)"
        text description
        decimal price "DECIMAL(10,2)"
        float latitude
        float longitude
        string owner_id FK "References USER"
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        string id PK "UUID"
        text text
        int rating "1-5"
        string user_id FK "References USER"
        string place_id FK "References PLACE"
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        string id PK "UUID"
        string name UK "VARCHAR(50)"
        string description "VARCHAR(255)"
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        string place_id PK,FK "References PLACE"
        string amenity_id PK,FK "References AMENITY"
    }

    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "linked to"
```

## Relationships

### One-to-Many Relationships

1. **User to Place**: A User can own many Places, but each Place belongs to exactly one User (owner).
2. **User to Review**: A User can write many Reviews, but each Review is written by exactly one User.
3. **Place to Review**: A Place can have many Reviews, but each Review is for exactly one Place.

### Many-to-Many Relationships

1. **Place to Amenity**: A Place can have many Amenities, and an Amenity can be associated with many Places. This is implemented through the `place_amenity` association table.

## Constraints

- **Unique Email**: Each user must have a unique email address.
- **Unique Amenity Name**: Each amenity must have a unique name.
- **One Review per User per Place**: A user can only leave one review for each place (enforced by unique constraint on `user_id` + `place_id`).
- **Rating Range**: Reviews must have a rating between 1 and 5.
- **Users Cannot Review Own Places**: Users cannot create a review for a place they own.

## Foreign Key Relationships

| Table | Column | References |
|-------|--------|------------|
| places | owner_id | users(id) |
| reviews | user_id | users(id) |
| reviews | place_id | places(id) |
| place_amenity | place_id | places(id) |
| place_amenity | amenity_id | amenities(id) |
