CREATE DATABASE IF NOT EXISTS storage;
USE storage; 

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;




-- TABLE STRUCTURES:


CREATE TABLE User (

    userID INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL

);



CREATE TABLE Genre (

    genreID INT PRIMARY KEY,

    genrename VARCHAR(50) UNIQUE NOT NULL

);

CREATE TABLE Game (

    gameID INT PRIMARY KEY,

    gamename VARCHAR(100) UNIQUE NOT NULL,

    shortdescription VARCHAR(300) NOT NULL,

    genres VARCHAR(300) NOT NULL

);



CREATE TABLE gamePref (

    userID INT,

    gameID INT,

    PRIMARY KEY (userID, gameID),

    FOREIGN KEY (gameID) REFERENCES Game(gameID) ON DELETE CASCADE,

    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE

);

CREATE TABLE wishlist (

    userID INT,

    gameID INT,

    PRIMARY KEY (userID, gameID),

    FOREIGN KEY (gameID) REFERENCES Game(gameID) ON DELETE CASCADE,

    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE

);

CREATE TABLE genrePref (

    userID INT,

    genreID INT,

    PRIMARY KEY (userID, genreID),

    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,

    FOREIGN KEY (genreID) REFERENCES Genre(genreID) ON DELETE CASCADE

); 

-- Insert users
INSERT INTO User (username) VALUES ('Erik'), ('Lisa'), ('Josefine'), ('Johan');

-- Import data into Genre from CSV
LOAD DATA LOCAL INFILE '/home/johanpi/SoftwareProject-Group-1/db/genres.csv'
INTO TABLE Genre
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @dummy)
SET genreID = @col1, genrename = @col2;

-- Import data into Game from CSV
LOAD DATA LOCAL INFILE '/home/johanpi/SoftwareProject-Group-1/db/games_description_indexed.csv'
INTO TABLE Game
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3, @dummy4, @col5, @dummy6, @dummy7, @dummy8, @dummy9, @dummy10, @dummy11, @dummy12, @dummy13, @dummy14)
SET gameID = @col1, gamename = @col2, shortdescription = @col3, genres = @col5;

-- Insert data into gamePref
INSERT INTO gamePref (userID, gameID) 
VALUES 
    (1, 1), 
    (1, 98),
    (1, 14), 
    (1, 33),
    (2, 3), 
    (3, 3), 
    (4, 1), 
    (4, 2), 
    (4, 9), 
    (4, 29), 
    (4, 83), 
    (4, 110), 
    (4, 145), 
    (4, 203), 
    (3, 208);

-- Insert data into wishlist
INSERT INTO wishlist (userID, gameID) 
VALUES 
    (1, 2), 
    (1, 3), 
    (1, 14), 
    (1, 33),
    (3, 6), 
    (4, 222), 
    (4, 277), 
    (4, 50), 
    (4, 59), 
    (3, 67);

-- Insert data into genrePref
INSERT INTO genrePref (userID, genreID) 
VALUES 
    (1, 1),
    (1, 4), 
    (1, 5),
    (1, 2), 
    (2, 2), 
    (3, 2), 
    (4, 0), 
    (4, 1), 
    (4, 2), 
    (4, 7), 
    (4, 9), 
    (4, 10), 
    (4, 20), 
    (3, 3);
