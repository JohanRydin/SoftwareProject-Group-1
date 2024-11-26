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

    genreID INT AUTO_INCREMENT PRIMARY KEY,

    Name VARCHAR(50) UNIQUE NOT NULL

);



CREATE TABLE gamePref (

    userID INT,

    gameID INT,

    PRIMARY KEY (userID, gameID),

    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE

);

CREATE TABLE wishlist (

    userID INT,

    gameID INT,

    PRIMARY KEY (userID, gameID),

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
INSERT INTO User (username) VALUES ('Erik'), ('Lisa'), ('Josefine');

-- Insert genres
INSERT INTO Genre (Name) VALUES ('Action'), ('RPG'), ('Horror');

-- Insert data into gamePref
INSERT INTO gamePref (userID, gameID) 
VALUES 
    (1, 1), 
    (1, 2), 
    (2, 3), 
    (3, 3), 
    (3, 4);

-- Insert data into wishlist
INSERT INTO wishlist (userID, gameID) 
VALUES 
    (1, 5), 
    (3, 6), 
    (3, 7);

-- Insert data into genrePref
INSERT INTO genrePref (userID, genreID) 
VALUES 
    (1, 1), 
    (2, 2), 
    (3, 2), 
    (3, 3);
