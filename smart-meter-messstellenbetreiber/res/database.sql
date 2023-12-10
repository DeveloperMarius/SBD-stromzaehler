CREATE TABLE IF NOT EXISTS 'logs'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'timestamp' BIGINT NOT NULL,
    'endpoint' VARCHAR(200) NOT NULL,
    'method' VARCHAR(10) NOT NULL,
    'source_type' VARCHAR(200) NULL DEFAULT NULL,
    'source_id' INTEGER NULL DEFAULT NULL,
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
    'phone' VARCHAR(200) NULL DEFAULT NULL,
    'email' VARCHAR(200) NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS 'stromzaehler'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'public_key' VARCHAR(2000),
    'address' INT NOT NULL,
    'landlord' INT NOT NULL,
    'owner' INT NOT NULL,
    Foreign Key ('address') REFERENCES addresses ('id') ON DELETE CASCADE,
    Foreign Key ('landlord') REFERENCES persons ('id') ON DELETE CASCADE,
    Foreign Key ('owner') REFERENCES persons ('id') ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 'kundenportale'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'url' VARCHAR(200) NOT NULL,
    'public_key' VARCHAR(2000) NOT NULL
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

CREATE TABLE IF NOT EXISTS 'alerts' (
    'id' INTEGER NOT NULL PRIMARY KEY,
    'stromzaehler' INTEGER NOT NULL,
    'message' TEXT,
    'timestamp' BIGINT NOT NULL,
    Foreign Key ('stromzaehler') REFERENCES stromzaehler ('id') ON DELETE CASCADE

);
