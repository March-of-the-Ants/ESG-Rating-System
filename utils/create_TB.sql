CREATE TABLE IF NOT EXISTS Product
 (
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8) NOT NULL,
            Type varchar(8) NOT NULL
            );

CREATE TABLE IF NOT EXISTS News 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8),
           Title text,
           Content text
            );

CREATE TABLE IF NOT EXISTS Jobplanet 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8) NOT NULL,
           Title text,
          Review text,
          Score float(2)
            );


CREATE TABLE IF NOT EXISTS Dart 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8),
           MajorSHRatio float(5),
          AdtOpinion text,
          EmphsMatter text
            );


CREATE TABLE IF NOT EXISTS Patent 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8) NOT NULL,
           Title text NOT NULL,
          Content text NOT NULL

            );


CREATE TABLE IF NOT EXISTS Report 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpID int NOT NULL,
            Year varchar(8) NOT NULL,
           Ecnt float,
          Scnt float,
          Gcnt float,
          TonePolarity float, 
          Escore float,
          Sscore float,
          Gscore float,
          TotalScore float,
          Egrade varchar(8),
          Sgrade varchar(8),
          Ggrade varchar(8),
          TotalGrade varchar(8),
          TotalRanking float,
          IndRanking float
            );


CREATE TABLE IF NOT EXISTS Company 
(
            ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            CmpName varchar(32)  NOT NULL,
            StockCode varchar(32)  NOT NULL,
            Owner  varchar(32)  NOT NULL,
            BizNo varchar(32)  NOT NULL,
            EstDate Date,
            Address text,
            Industry varchar(32)  NOT NULL,
            Product text        
            );
            