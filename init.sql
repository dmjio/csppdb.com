

/* use if necessary */
drop database Twitter; 

CREATE SCHEMA IF NOT EXISTS `Twitter` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ; 

USE `Twitter` ;

-- -----------------------------------------------------
-- Table `Twitter`.`Users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Users` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Users` (
  `UserID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `First` VARCHAR(45) NULL ,
  `Last` VARCHAR(45) NULL ,
  `Password` VARCHAR(32) NULL ,
  `Web` VARCHAR(45) NULL ,
  `Username` VARCHAR(25) NOT NULL ,
  `Tweets` INT UNSIGNED NOT NULL DEFAULT 0 ,
  `Created` DATETIME NULL ,
  `Updated` DATETIME NULL ,
  `Email` VARCHAR(100) NULL ,
  `Blurb` VARCHAR(150) NULL ,
  `IMG` VARCHAR(255) NULL ,
  PRIMARY KEY (`UserID`, `Username`) );

-- -----------------------------------------------------
-- Table `Twitter`.`Tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Tweets` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Tweets` (
  `TweetID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Content` VARCHAR(150) NOT NULL ,
  `TimeStamp` DATETIME NOT NULL ,
  `Rating` INT NULL DEFAULT 0 ,
  `Likes` INT UNSIGNED NULL DEFAULT 0 ,
  `Dislikes` INT UNSIGNED NULL DEFAULT 0 ,
  `UserID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`TweetID`, `UserID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Hash`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Hash` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Hash` (
  `HashTagID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `Tag` VARCHAR(45) NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`HashTagID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Mentions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Mentions` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Mentions` (
  `TweetID` INT UNSIGNED NOT NULL ,
  `UserID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`UserID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`URLS`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`URLS` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`URLS` (
  `URLID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '  ' ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `URL` VARCHAR(150) NOT NULL ,
  PRIMARY KEY (`URLID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Followers` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Followers` (
  `UserID` INT UNSIGNED NOT NULL ,
  `FollowerID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`UserID`, `FollowerID`));

-- -----------------------------------------------------
-- Table `Twitter`.`ReTweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`ReTweets` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`ReTweets` (
  `UserID` INT UNSIGNED NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  `TimeStamp` DATETIME NULL,
  PRIMARY KEY (`UserID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Favorites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Favorites` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Favorites` (
  `UserID` INT UNSIGNED NOT NULL ,
  `TweetID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`UserID`, `TweetID`));

-- -----------------------------------------------------
-- Table `Twitter`.`Likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Twitter`.`Likes` ;

CREATE  TABLE IF NOT EXISTS `Twitter`.`Likes` (
  `TweetID` INT UNSIGNED NOT NULL ,
  `UserID` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`TweetID`, `UserID`));

