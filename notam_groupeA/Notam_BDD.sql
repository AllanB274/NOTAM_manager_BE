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

CREATE TABLE IF NOT EXISTS aerodrome
(
    idAerodrome INT NOT NULL AUTO_INCREMENT,
    codeAerodrome VARCHAR(4) NOT NULL,
    nomAerodrome VARCHAR(50),
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
    FOREIGN KEY (idDepart) REFERENCES aerodrome(idAerodrome),
    FOREIGN KEY (idArrivee) REFERENCES aerodrome(idAerodrome)
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
    FOREIGN KEY (idAerodrome) REFERENCES aerodrome(idAerodrome) ON DELETE CASCADE ON UPDATE CASCADE,
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
    FOREIGN KEY (idDegagement) REFERENCES aerodrome(idAerodrome)
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

INSERT INTO aerodrome (codeAerodrome,nomAerodrome,region,departement,ville,pays)
VALUES
('LFBO','Blagnac','Occitanie','Haute Garonne','Toulouse','France'),
('LFLC','Aeroport de clermont ferrand','Auvergne','Puy de domes','Clermont Ferrand','France'),
('LFBD','Bordeaux-Mérignac','Nouvelle Aquitaine','Gironde', 'Bordeaux','France'),
('LFPG','Roissy Charles-de-Gaulle','Ile-de-France',"Val d'Oise", 'Paris','France');


INSERT INTO Objets(nomObjet)
VALUES
('cochon volant'),
('travaux');

INSERT INTO Notam(idNotam, typeNotam, date_debut, date_fin, creneau, description, limite_inferieur, limite_superieur, typeVol, idAerodrome, idUser, idObjet)
VALUES
('156156', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', 'OULALALALAAAAA LES TRAVAUUUUUX', "FL005", 'FL200', 'IV', 1, 1, 1),
('156157', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', 'OULALALALAAAAA LES TRAVAUUUUUX2', "FL005", 'FL200', 'IV', 2, 1, 1),
('156159', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', "heureusement que j'avais demandé à Ryan de faire plein d'exemples de notams", "FL005", 'FL200', 'IV', 2, 1, 1),
('156158', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', 'OULALALALAAAAA LES TRAVAUUUUUX3', "FL005", 'FL200', 'IV', 3, 1, 1),
('156160', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', "j'adore les bases de données", "FL005", 'FL200', 'IV', 4, 1, 1),
('156161', 'NOTAMN', "2025-11-11 23:13:45", "2026-11-11 23:13:45", '13H-15H', "j'encule les bases de données", "FL005", 'FL200', 'IV', 4, 1, 1);

INSERT INTO Vol(typeVol, nomVol, idUser, idDepart, idArrivee, date_depart, date_arrivee)
VALUES
('I', 'la mère de Ryan', 1, 2, 3, "2026-01-01 00:00:00", "2026-01-01 00:00:01");

INSERT INTO degagement_vol(idVol, idDegagement)
VALUES
('1', '1'),
('1', '4');