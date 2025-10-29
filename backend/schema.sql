CREATE DATABASE IF NOT EXISTS f1_data_cache;

USE f1_data_cache;

-- CREATE THE TEAMS TABLE
CREATE TABLE IF NOT EXISTS Teams (
    team_name VARCHAR(50) PRIMARY KEY,
    team_color VARCHAR(7) NOT NULL
)

-- CREATE DRIVERS TABLE
CREATE TABLE IF NOT EXISTS Drivers(
    driver_number SMALLINT PRIMARY KEY,
    team_name VARCHAR(50) NOT NULL,
    name_acronym VARCHAR(3) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    broadcast_name VARCHAR(50) NOT NULL,
    headshot_url TEXT,
    country_code VARCHAR(10),
    last_updated DATETIME,
    -- Define the Foreign Key constraint linking to the Teams table
    CONSTRAINT fk_team
        FOREIGN KEY (team_name)
        REFERENCES Teams(team_name)
        ON DELETE CASCADE
)
