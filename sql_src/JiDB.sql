DROP DATABASE IF EXISTS JiDB;
CREATE DATABASE JiDB;
USE JiDB;
CREATE TABLE Users(
	UID INT NOT NULL AUTO_INCREMENT,
    BUDGET INT DEFAULT 0,
    UName VARCHAR(255) NOT NULL,
    UPassword VARCHAR(255) NOT NULL,
    UAccount VARCHAR(255) NOT NULL,
    UNickname VARCHAR(255) DEFAULT 'Nickname',
    isrightHander BOOLEAN DEFAULT TRUE,
    isDarkMode BOOLEAN DEFAULT FALSE,
    NoticeTime DATE DEFAULT NULL, -- NULL/None indicates that users do not want to have a specific notice time
    PRIMARY KEY (UID)
);

CREATE TABLE Ledgers(
    UID INT NOT NULL,
    LedgerSum INT DEFAULT 0 NOT NULL,
    LName VARCHAR(255) NOT NULL,
    PRIMARY KEY (UID, LName)
);

CREATE TABLE Datas(
	UID INT NOT NULL,
    LName VARCHAR(255) NOT NULL,
	DID INT AUTO_INCREMENT NOT NULL,
    Price INT DEFAULT 0 NOT NULL,
    DName VARCHAR(255) NOT NULL,
    DType VARCHAR(255) NOT NULL,
    DDate DATE NOT NULL, -- Front-end should provide current date
    PRIMARY KEY (DID)
);


ALTER TABLE Ledgers
ADD CONSTRAINT `fk_Ledgers_to_Users_UID` FOREIGN KEY (UID) REFERENCES Users(UID)ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Datas
ADD CONSTRAINT `fk_Datas_to_Ledgers_LID` FOREIGN KEY (UID, LName) REFERENCES Ledgers(UID, LName) ON DELETE CASCADE ON UPDATE CASCADE;