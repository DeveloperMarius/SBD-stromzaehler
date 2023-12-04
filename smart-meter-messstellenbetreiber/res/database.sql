CREATE TABLE IF NOT EXISTS 'logs'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'timestamp' BIGINT NOT NULL,
    'endpoint' VARCHAR(200) NOT NULL,
    'method' VARCHAR(10) NOT NULL,
    'jwt_id' VARCHAR(200) NULL DEFAULT NULL,
    'message' TEXT
);


CREATE TABLE IF NOT EXISTS 'addresses'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'street' VARCHAR(200),
    'plz' Integer,
    'city' VARCHAR(200),
    'state' VARCHAR(200),
    'country' VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS 'persons'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'firstname' VARCHAR(200) NOT NULL,
    'lastname' VARCHAR(200) NOT NULL,
    'gender' INTEGER,
    'phone' VARCHAR(200),
    'email' VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS 'stromzaehler'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'secret_key' VARCHAR(200),
    'address' Integer NOT NULL,
    'landlord' Integer NOT NULL,
    'owner' INT,
    Foreign Key ('address') REFERENCES addresses ('id') ON DELETE CASCADE,
    Foreign Key ('landlord') REFERENCES persons ('id') ON DELETE CASCADE,
    Foreign Key ('owner') REFERENCES persons ('id') ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS 'stromzaehler_logs'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'stromzaehler' INTEGER NOT NULL,
    'source_id' INTEGER NOT NULL,
    'timestamp' BIGINT NOT NULL,
    'message' TEXT,
    Foreign Key ('stromzaehler') REFERENCES stromzaehler ('id') ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 'stromzaehler_readings'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'stromzaehler' INTEGER NOT NULL,
    'source_id' INTEGER NOT NULL,
    'timestamp' BIGINT NOT NULL,
    'value' INTEGER NOT NULL,
    Foreign Key ('stromzaehler') REFERENCES stromzaehler ('id') ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 'settings' (
    'key' VARCHAR(200) NOT NULL,
    'value' VARCHAR(200) NOT NULL
);
