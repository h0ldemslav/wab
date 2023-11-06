CREATE DATABASE review;

CREATE TABLE coffee_shops (
    id UUID PRIMARY KEY 
);

INSERT INTO coffee_shops (id) VALUES (
    '3559dbec-d500-4e6e-ac6d-812a66c4dc40'
);

CREATE TABLE users (
    id UUID PRIMARY KEY
);

INSERT INTO users (id) VALUES (
    'bb79fb9d-99be-45c3-89a1-9e30c95c9544'
);

CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    coffee_shop_id UUID NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL,
    rating INT NOT NULL,
    descript TEXT,
    CONSTRAINT fk_coffee_shop FOREIGN KEY (coffee_shop_id) REFERENCES coffee_shops (id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE (coffee_shop_id, user_id)
);