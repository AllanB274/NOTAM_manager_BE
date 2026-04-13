CREATE DATABASE IF NOT EXISTS Notam_BDD;

USE Notam_BDD;

CREATE TABLE IF NOT EXISTS User
(
    idUser INT NOT NULL AUTO_INCREMENT,
    prenom VARCHAR(20),
    nom VARCHAR(20),
    role ENUM('admin','client'),
    PRIMARY KEY (idUser)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Aerodrome
(
    idAerodrome VARCHAR(20) NOT NULL,
    nomAerodrome VARCHAR(20),
    region VARCHAR(20),
    departement VARCHAR(20),
    ville VARCHAR(20),
    pays VARCHAR(20),
    PRIMARY KEY (idAerodrome)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Vol
(
    idVol INT NOT NULL AUTO_INCREMENT,
    typeVol VARCHAR(20),
    nomVol VARCHAR(20),
    idUser INT,
    idDepart INT,
    idArrivee INT,
    date_depart DATETIME,
    date_arrivee DATETIME,
    PRIMARY KEY (idVol),
    FOREIGN KEY (idUser) REFERENCES User(idUser),
    FOREIGN KEY (idDepart) REFERENCES Aerodrome(idAerodrome),
    FOREIGN KEY (idArrivee) REFERENCES Aerodrome(idAerodrome)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Objets
(
    idObjet INT NOT NULL AUTO_INCREMENT,
    nomObjet VARCHAR(20),
    PRIMARY KEY (idObjet)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Notam
(
    idNotam VARCHAR(20) NOT NULL,
    typeNotam ENUM('NOTAMR','NOTAMN','NOTAMC'),
    date_declaration DATE,
    date_debut DATETIME,
    date_fin DATETIME,
    creneau VARCHAR(20),
    description VARCHAR(20),
    limite_inferieur VARCHAR(20),
    limite_superieur VARCHAR(20),
    typeVol VARCHAR(20),
    idAerodrome INT,
    idUser INT,
    idObjet INT,
    PRIMARY KEY (idNotam),
    FOREIGN KEY (idAerodrome) REFERENCES Aerodrome(idAerodrome),
    FOREIGN KEY (idUser) REFERENCES User(idUser),
    FOREIGN KEY (idObjet) REFERENCES Objets(idObjet)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS degagement_vol
(
    idDV INT NOT NULL AUTO_INCREMENT,
    idVol INT,
    idDegagement INT,
    PRIMARY KEY (idDV),
    FOREIGN KEY (idVol) REFERENCES Vol(idVol),
    FOREIGN KEY (idDegagement) REFERENCES Aerodrome(idAerodrome)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Vol_User
(
    idVU INT NOT NULL AUTO_INCREMENT,
    idVol INT,
    idUser INT,
    PRIMARY KEY (idVU),
    FOREIGN KEY (idVol) REFERENCES Vol(idVol),
    FOREIGN KEY (idUser) REFERENCES User(idUser)
) ENGINE=InnoDB CHARSET=utf8;

