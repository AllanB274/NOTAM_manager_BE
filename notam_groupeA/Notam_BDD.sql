CREATE DATABASE IF NOT EXISTS Notam_BDD;

USE Notam_BDD;

CREATE TABLE IF NOT EXISTS User
(
    idUser INT NOT NULL AUTO_INCREMENT,
    prenom VARCHAR(20),
    nom VARCHAR(20),
    mdp VARCHAR(250),
    login VARCHAR(30),
    role ENUM('admin','client'),
    avatar VARCHAR(250),
    PRIMARY KEY (idUser)
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Aerodrome
(
    idAerodrome INT NOT NULL AUTO_INCREMENT,
    codeAerodrome VARCHAR(4) NOT NULL,
    nomAerodrome VARCHAR(20),
    region VARCHAR(20),
    departement VARCHAR(20),
    ville VARCHAR(20),
    pays VARCHAR(20),
    PRIMARY KEY (idAerodrome)
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Vol
(
    idVol INT NOT NULL AUTO_INCREMENT,
    typeVol ENUM('I','V','IV'),
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
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Objets
(
    idObjet INT NOT NULL AUTO_INCREMENT,
    nomObjet VARCHAR(20),
    PRIMARY KEY (idObjet)
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Notam
(
    idNotam VARCHAR(20) NOT NULL,
    typeNotam ENUM('NOTAMR','NOTAMN','NOTAMC'),
    date_declaration DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_debut DATETIME,
    date_fin DATETIME,
    creneau VARCHAR(11),
    description VARCHAR(1000),
    limite_inferieur VARCHAR(5),
    limite_superieur VARCHAR(5),
    typeVol ENUM('I','V','IV'),
    idAerodrome INT,
    idUser INT,
    idObjet INT,
    PRIMARY KEY (idNotam),
    FOREIGN KEY (idAerodrome) REFERENCES Aerodrome(idAerodrome) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idUser) REFERENCES User(idUser),
    FOREIGN KEY (idObjet) REFERENCES Objets(idObjet)
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS degagement_vol
(
    idDV INT NOT NULL AUTO_INCREMENT,
    idVol INT,
    idDegagement INT,
    PRIMARY KEY (idDV),
    FOREIGN KEY (idVol) REFERENCES Vol(idVol),
    FOREIGN KEY (idDegagement) REFERENCES Aerodrome(idAerodrome)
) ENGINE=InnoDB CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Vol_User
(
    idVU INT NOT NULL AUTO_INCREMENT,
    idVol INT,
    idUser INT,
    PRIMARY KEY (idVU),
    FOREIGN KEY (idVol) REFERENCES Vol(idVol),
    FOREIGN KEY (idUser) REFERENCES User(idUser)
) ENGINE=InnoDB CHARSET=utf8mb4;














INSERT INTO User (prenom,nom,mdp,login,role)
VALUES
('Luc','Leugotte','f8638b979b2f4f793ddb6dbd197e0ee25a7a6ea32b0ae22f5e3c5d119d839e75', 'Lu', 'admin'),
('Allan','Gromolet','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Al', 'client');

INSERT INTO Aerodrome (codeAerodrome,nomAerodrome,region,departement,ville,pays)
VALUES
('LFBO','Blagnac','Occitanie','Haute Garonne','Toulouse','France'),
('LFLC','Aeroport de clermont ferrand','Auvergne','Puy de domes','Clermont Ferrand','France'),
('LFBO','Merignac','Nouvelle Aquitaine','Gironde', 'Bordeau','France');

