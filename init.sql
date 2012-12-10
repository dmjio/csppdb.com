
-- -----------------------------------------------------
-- Table `Twitter`.`Users`
-- -----------------------------------------------------
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS `Users` ;

CREATE  TABLE IF NOT EXISTS `Users` (
  `Username` VARCHAR(25) NOT NULL UNIQUE,
  `Password` VARCHAR(160) NOT NULL,
  `First` VARCHAR(45) NULL ,
  `Last` VARCHAR(45) NULL ,
  `Web` VARCHAR(45) NULL ,
  `Popular` INT UNSIGNED NOT NULL DEFAULT 0,
  `Created` DATETIME NULL ,
  `Updated` DATETIME NULL ,
  `Email` VARCHAR(100) NULL ,
  `Blurb` VARCHAR(150) NULL ,
  `IMG` VARCHAR(255) NULL ,
  PRIMARY KEY (`Username`)) ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Tweets` ;

CREATE  TABLE IF NOT EXISTS `Tweets` (
  `TweetID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Content` VARCHAR(150) NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,
  `Created` DATETIME NOT NULL,
  FOREIGN KEY(Username) REFERENCES Users(Username),
  PRIMARY KEY (`TweetID`, `Username`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Hash`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Hash` ;
  
CREATE  TABLE IF NOT EXISTS `Hash` (
  `HashTagID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Tag` VARCHAR(45) NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `Created` DATETIME NOT NULL,
    FOREIGN KEY(TweetID) REFERENCES Tweets(TweetID),
  PRIMARY KEY (`HashTagID`, `TweetID`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Mentions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Mentions` ;

CREATE  TABLE IF NOT EXISTS `Mentions` (
  `MentionID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,   
  `Created` DATETIME NOT NULL,
    FOREIGN KEY(Username) REFERENCES Users(Username),
    FOREIGN KEY(TweetID) REFERENCES Tweets(TweetID),

  PRIMARY KEY (`MentionID`,`Username`, `TweetID`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Urls`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Urls` ;

CREATE  TABLE IF NOT EXISTS `Urls` (
  `UrlID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `TweetID` INT UNSIGNED NOT NULL ,
  `URL` VARCHAR(150) NOT NULL ,
  `Created` DATETIME NOT NULL,
  FOREIGN KEY(TweetID) REFERENCES Tweets(TweetID),
  PRIMARY KEY (`UrlID`, `TweetID`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Followers` ;

CREATE  TABLE IF NOT EXISTS `Followers` (
  `User` VARCHAR(25) NOT NULL ,
  `Follower` VARCHAR(25) NOT NULL ,
    FOREIGN KEY(User) REFERENCES Users(Username),
    FOREIGN KEY(Follower) REFERENCES Users(Username),
  PRIMARY KEY (`User`, `Follower`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`ReTweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ReTweets` ;
  
CREATE TABLE IF NOT EXISTS `ReTweets` (
  `Username` VARCHAR(25) NOT NULL,
  `TweetID` INT UNSIGNED NOT NULL,
  `Created` DATETIME NOT NULL,
  FOREIGN KEY(Username) REFERENCES Users(Username),
  FOREIGN KEY(TweetID) REFERENCES Tweets(TweetID),
  PRIMARY KEY (`Username`, `TweetID`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Favorites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Favorites` ;

CREATE  TABLE IF NOT EXISTS `Favorites` (
  `Username` VARCHAR(25) NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`Username`, `TweetID`))ENGINE=INNODB;

-- -----------------------------------------------------
-- Table `Twitter`.`Likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Likes` ;

CREATE TABLE IF NOT EXISTS `Likes` (
  `TweetID` INT UNSIGNED NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,
  FOREIGN KEY(Username) REFERENCES Users(Username),
  FOREIGN KEY(TweetID) REFERENCES Tweets(TweetID),
  PRIMARY KEY (`TweetID`, `Username`))ENGINE=INNODB;


DROP PROCEDURE IF EXISTS `ADD_USER` ;
DROP PROCEDURE IF EXISTS `ADD_URL` ;
DROP PROCEDURE IF EXISTS `UPDATE_USER` ;
DROP PROCEDURE IF EXISTS `TWEETCOUNT` ;
DROP PROCEDURE IF EXISTS `USERCOUNT` ;
DROP PROCEDURE IF EXISTS `ADD_TWEET` ;
DROP PROCEDURE IF EXISTS `DELETE_TWEET` ;
DROP PROCEDURE IF EXISTS `FOLLOW_USER` ;
DROP PROCEDURE IF EXISTS `UNFOLLOW_USER` ;
DROP PROCEDURE IF EXISTS `ADD_HASH` ;
DROP PROCEDURE IF EXISTS `RETWEET` ;
DROP PROCEDURE IF EXISTS `ADD_FAVORITE` ;
DROP PROCEDURE IF EXISTS `ADD_MENTION` ;
DROP PROCEDURE IF EXISTS `LIKE_TWEET` ;

-- Stored routine(s) 
CREATE PROCEDURE ADD_USER(
  uUsername VARCHAR(25),
  uPassword VARCHAR(160),
  uEmail VARCHAR(100))
  INSERT INTO Users (Username, Password, Email, Created, Updated) VALUES
  (uUsername, uPassword, uEmail, NOW(), NOW());

CREATE PROCEDURE UPDATE_USER(
  uUsername VARCHAR(25),
  uFirst VARCHAR(45),
  uLast VARCHAR(45),
  uWeb VARCHAR(45),
  uEmail VARCHAR(100),
  uBlurb VARCHAR(150))
  UPDATE Users 
    SET
    First = uFirst, 
    Last = uLast, 
    Web = uWeb, 
    Updated = NOW(), 
    Email = uEmail, 
    Blurb = uBlurb
  WHERE UserName = uUsername;
  
SET foreign_key_checks = 1;

-- Stored routine(s) 2
CREATE PROCEDURE TWEETCOUNT() SELECT COUNT(*) as 'Total Tweet Count' FROM Tweets;
CREATE PROCEDURE USERCOUNT() SELECT COUNT(*) as 'Total User Count' FROM Users;

-- Stored routine(s) 3
CREATE PROCEDURE ADD_TWEET(tUserName VARCHAR(25), tContent VARCHAR(150))
INSERT INTO Tweets (UserName, Content, Created) 
VALUES (tUserName, tContent, NOW());

CREATE PROCEDURE DELETE_TWEET(uTweetID INT)
DELETE FROM Tweets WHERE TweetID = uTweetID;

-- Other procedures I will need... I am only testing the scenarios for the ones above ^
-- Follow relationships
CREATE PROCEDURE FOLLOW_USER(Follower VARCHAR(25), UserToFollow VARCHAR(25))
INSERT INTO Followers (User, Follower) 
VALUES (Follower, UserToFollow);

CREATE PROCEDURE UNFOLLOW_USER(tUserToFollow VARCHAR(25), tFollower VARCHAR(25))
DELETE FROM Followers WHERE User = tUserToFollow AND Follower = tFollower;

-- Add a hash
CREATE PROCEDURE ADD_HASH(tTag VARCHAR(45), tTweetID INT)
INSERT INTO HASH (Tag, TweetID, Created)
VALUES (tTag, tTweetID, NOW());

-- Add Urls
CREATE PROCEDURE ADD_URL(tUrl VARCHAR(150), tTweetID INT)
INSERT INTO URLS (TweetID, URL, Created)
VALUES (tTweetID, tUrl, NOW());

-- Retweets
CREATE PROCEDURE RETWEET (tUsername VARCHAR(25), tTweetID INT)
INSERT INTO RETWEETS (Username, TweetID, Created)
VALUES (tUsername, tTweetID, NOW());

-- Favorites
CREATE PROCEDURE ADD_FAVORITE (tUsername VARCHAR(25), tTweetID INT)
INSERT INTO FAVORITES (TweetID, Username)
VALUES (tTweetID, tUsername);

-- Mention
CREATE PROCEDURE ADD_MENTION(tTweetID INT, tUsername VARCHAR(25))
INSERT INTO MENTIONS (TweetID, Username, Created)
VALUES (tTweetID, tUsername, NOW());

-- Favorites
CREATE PROCEDURE LIKE_TWEET (tUsername VARCHAR(25), tTweetID INT)
INSERT INTO Likes (TweetID, Username)
VALUES (tTweetID, tUsername);


