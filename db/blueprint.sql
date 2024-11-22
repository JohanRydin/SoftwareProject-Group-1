CREATE DATABASE storage IF NOT EXISTS storage;
USE storage; 
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";



--- TABLE STRUCTURES: ---


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
