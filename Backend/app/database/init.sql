CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role VARCHAR(255) NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INTEGER,
    CONSTRAINT fk_role
        FOREIGN KEY (role_id)
        REFERENCES roles (id)
        ON DELETE SET NULL
);