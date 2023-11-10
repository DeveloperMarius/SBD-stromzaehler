CREATE TABLE IF NOT EXISTS 'logs'(
    'id' INTEGER NOT NULL PRIMARY KEY,
    'timestamp' BIGINT NOT NULL,
    'message' TEXT
);

CREATE TABLE IF NOT EXISTS 'settings' (
    'key' VARCHAR(200) NOT NULL,
    'value' VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'readings' (
    'id' INTEGER NOT NULL PRIMARY KEY,
    'timestamp' BIGINT NOT NULL,
    'value' INTEGER NOT NULL
);
