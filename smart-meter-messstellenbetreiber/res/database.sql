CREATE TABLE IF NOT EXISTS 'logs'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'timestamp' DATETIME NOT NULL,
    'endpoint' VARCHAR(200) NOT NULL,
    'method' VARCHAR(10) NOT NULL,
    'jwt_id' VARCHAR(200) NULL,
    'message' TEXT
);

CREATE TABLE IF NOT EXISTS 'settings' (
    'key' VARCHAR(200) NOT NULL,
    'value' VARCHAR(200) NOT NULL
);
