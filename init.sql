

-- -----------------------------------------------------
-- Table `Twitter`.`Users`
-- -----------------------------------------------------
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
  PRIMARY KEY (`Username`));

-- -----------------------------------------------------
-- Table `Twitter`.`Tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Tweets` ;

CREATE  TABLE IF NOT EXISTS `Tweets` (
  `TweetID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Content` VARCHAR(150) NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,
  `Created` DATETIME NOT NULL,
  PRIMARY KEY (`TweetID`, `Username`));

-- -----------------------------------------------------
-- Table `Twitter`.`Hash`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Hash` ;
  
CREATE  TABLE IF NOT EXISTS `Hash` (
  `HashTagID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Tag` VARCHAR(45) NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `Created` DATETIME NOT NULL,
  PRIMARY KEY (`HashTagID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Mentions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Mentions` ;

CREATE  TABLE IF NOT EXISTS `Mentions` (
  `MentionID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,   
  `Created` DATETIME NOT NULL,
  PRIMARY KEY (`MentionID`,`UserName`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Urls`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Urls` ;

CREATE  TABLE IF NOT EXISTS `Urls` (
  `UrlID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `TweetID` INT UNSIGNED NOT NULL ,
  `URL` VARCHAR(150) NOT NULL ,
  `Created` DATETIME NOT NULL,
  PRIMARY KEY (`UrlID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Followers` ;

CREATE  TABLE IF NOT EXISTS `Followers` (
  `User` VARCHAR(25) NOT NULL ,
  `Follower` VARCHAR(25) NOT NULL ,
  PRIMARY KEY (`User`, `Follower`));

-- -----------------------------------------------------
-- Table `Twitter`.`ReTweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ReTweets` ;
  
CREATE TABLE IF NOT EXISTS `ReTweets` (
  `Username` VARCHAR(25) NOT NULL,
  `TweetID` INT UNSIGNED NOT NULL,
  `Created` DATETIME NOT NULL,
  PRIMARY KEY (`Username`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Favorites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Favorites` ;

CREATE  TABLE IF NOT EXISTS `Favorites` (
  `Username` VARCHAR(25) NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`Username`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Likes` ;

CREATE TABLE IF NOT EXISTS `Likes` (
  `TweetID` INT UNSIGNED NOT NULL ,
  `Username` VARCHAR(25) NOT NULL ,
  PRIMARY KEY (`TweetID`, `Username`));

