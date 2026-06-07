from . import bddGen
import inspect
import hashlib
from datetime import datetime

# -----------------------------------
# Retourne le nom de la fonction courante
# -----------------------------------
def func_name():
    return inspect.currentframe().f_back.f_code.co_name


def verifAuthData(login, mdp):
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
    sql = "SELECT * FROM User where login=%s and mdp=%s"
    param = (login, mdpC)
    return bddGen.selectOneData(func_name(), sql, param)

def verifVolExist(departure, arrival):
    sql = "SELECT * FROM Vol where idDepart=%s and idArrivee=%s"
    param = (departure, arrival)
    return bddGen.selectOneData(func_name(), sql, param)


def update_userMdpData(newmdp, idUser):
    sql = "UPDATE user SET mdp=%s WHERE idUser=%s;"
    param = (newmdp, idUser)
    return bddGen.updateData(func_name(), sql, param, None)

def add_membreData(rform, msg=None):
    sql = """ INSERT INTO User
    (nom, prenom, login, mdp, role, avatar)
    VALUES (%s, %s, %s, %s, %s, %s); """
    
    #verification admin
    if rform['role'] == 'admin':
        if rform['mdpAdmin'] != 'secret':
            raise TypeError("admin key incorrect")
        
    #remplir les champs vide
    if rform['username'] == '' or rform['mdp'] == '' or rform['avatar'] == '':
        raise TypeError("remplir les champs exigez")

    #verifier que l'user n'existe pas deja

    sql2 = "SELECT * FROM User WHERE login=%s"
    param2 = (rform['username'],)
    if bddGen.selectOneData(func_name(), sql2, param2):
        raise TypeError("utilisateur deja existant")
    
    mdp = rform['mdp']
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
    avatar = rform['avatar']


    param = (rform['lastname'], rform['firstname'], rform['username'], mdpC, rform.get('role'), avatar)

    return bddGen.addData(func_name(), sql, param, msg)


def add_notamData(rform, session, msg=None):
    idUser = session['idUser']
    idNotam = rform.get("idNotam")
    typeNotam = rform.get("typeNotam")
    dateStartNotam = rform.get("dateStartNotam")
    dateEndNotam = rform.get("dateEndNotam")
    startCreneau = rform.get("startCreneau")
    endCreneau = rform.get("endCreneau")
    creneau = startCreneau+'H-'+endCreneau+'H'
    descNotam = rform.get("descNotam")
    lowerFLNotam = rform.get("lowerFLNotam")
    upperFLNotam = rform.get("upperFLNotam")
    airport = rform.get("airport")
    object = rform.get("object")
    flightTypes = "".join(sorted(rform.getlist("flightType")))
    
    sql = """
        INSERT INTO Notam
        (
            idNotam,
            typeNotam,
            date_debut,
            date_fin,
            creneau,
            description,
            limite_inferieur,
            limite_superieur,
            typeVol,
            idAerodrome,
            idUser,
            idObjet
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """
    param = (idNotam, typeNotam, dateStartNotam, dateEndNotam, creneau, descNotam, lowerFLNotam, upperFLNotam, flightTypes, airport, idUser, object)
    
    for a in param:
        if a=='':
            raise TypeError("Please fill all the fields")
    
    try:
        int(idNotam)
    except:
        raise TypeError("Please choose a valid ID")
    
    if datetime.strptime(dateEndNotam, "%Y-%m-%dT%H:%M") < datetime.strptime(dateStartNotam, "%Y-%m-%dT%H:%M"):
        raise TypeError("Please select a valid date range")
    
    if int(endCreneau)-int(startCreneau)<0:
        raise TypeError("Please select a valid time slot")

    if int(lowerFLNotam)>int(upperFLNotam):
        raise TypeError("Please select a valid levels range")
    
    sql2 = "SELECT * FROM notam WHERE idNotam=%s"
    param2 = (idNotam,)
    if bddGen.selectOneData(func_name(), sql2, param2):
        raise TypeError("A Notam with this ID already exists")
    
    return bddGen.addData(func_name(), sql, param, msg)

def del_notamData(idNotam, msg=None):
    sql = "DELETE FROM Notam WHERE idNotam=%s;"
    param = (idNotam,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def del_aeroportData(idAeroport, msg=None):
    sql = "DELETE FROM aerodrome WHERE idAerodrome=%s;"
    param = (idAeroport,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def del_volData(idVol, msg=None):
    sql = "DELETE FROM Vol WHERE idVol=%s;"
    param = (idVol,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def add_volData(rform, session, msg=None):
    sql = """
        INSERT INTO Vol
        (typeVol, nomVol, idUser, idDepart, idArrivee, date_depart, date_arrivee)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    param = (
        rform.get("typeVol"),
        rform.get("nameVol"),
        session["idUser"],
        rform.get("airportdepart"),
        rform.get("airportarrival"),
        rform.get("dateStartVol"),
        rform.get("dateEndVol")
    )
    # Ne pas laissez de champs libres
    for a in param:
        if a == '':
            raise TypeError("remplir les champs exigez")

    # Vérifie que le vol n’existe pas déjà avec le même départ, arrivée et les dates.
    sql2 = """
        SELECT * FROM Vol
        WHERE idDepart=%s AND idArrivee=%s AND date_depart=%s AND date_arrivee=%s
    """
    param_verif = (rform.get("airportdepart"), rform.get("airportarrival"), rform.get("dateStartVol"), rform.get("dateEndVol"))
    if bddGen.selectOneData(func_name(), sql2, param_verif):
        raise TypeError("Vol already exists")

    return bddGen.addData(func_name(), sql, param, msg)



def add_degagementsData(idVol, degagements, msg=None):
    sql = """
        INSERT INTO degagement_vol
        (idVol, idDegagement)
        VALUES (%s, %s);
    """
    #ajout des aérodromes de dégagement appartenant à la liste
    for idDegagement in degagements:
        param = (idVol, idDegagement)
        bddGen.addData(func_name(), sql, param, msg)

def add_volUserData(idVol, idUser, msg=None):
    sql = """
        INSERT INTO vol_user
        (idVol, idUser)
        VALUES (%s, %s);
    """
    param = (idVol, idUser)
    return bddGen.addData(func_name(), sql, param, msg)



def add_airportData(rform, msg=None):
    sql = """ INSERT INTO aerodrome
    (codeAerodrome, nomAerodrome, region, departement, ville, pays)
    VALUES (%s, %s, %s, %s, %s, %s); """
    param = ( rform['codeAerodrome'], rform['nomAerodrome'], rform['region'], rform['departement'], rform['ville'], rform['pays'] )

        #verification champs nuls :
    for a in param:
        if a=='':
            raise TypeError("remplir les champs exigez")
        
        #verification deja existant :
    sql2 = "SELECT * FROM aerodrome WHERE codeAerodrome=%s"
    param2 = (rform['codeAerodrome'],)
    if bddGen.selectOneData(func_name(), sql2, param2):
        raise TypeError("code Aerodrome deja existant")

    return bddGen.addData(func_name(), sql, param, msg)

def update_notam(idNotam, newdesc):
    sql = "UPDATE Notam SET description=%s WHERE idNotam=%s;"
    param = (newdesc, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def get_airports():
    # Renvoie la liste de tous les aéroports
    sql = f"SELECT * FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_objects():
    # Renvoie la liste de tous les objets
    sql = "SELECT * FROM objets"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_notams():
    # Renvoie la liste de tous les notams
    sql = f"SELECT * FROM Notam"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_vols():
    # Renvoie la liste des notams d'un aérodrome
    sql = f"SELECT * FROM Vol"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_notamsVol(idAero):
    # Renvoie la liste de tous les notams d'un aérodrome
    sql = "SELECT * FROM Notam WHERE idAerodrome=%s"
    param = (idAero,)
    r = bddGen.selectData(func_name(), sql, param)
    return r if r!=None else []

def get_deroutement(idVol):
    # Renvoie la liste de tous les notams des aérodromes de déroutement d'un vol
    l = []
    sql = "SELECT * FROM degagement_vol WHERE idVol=%s"
    param = (idVol,)
    r = bddGen.selectData(func_name(), sql, param)
    sql2 = "SELECT * FROM Notam WHERE idAerodrome=%s"
    for i in r:
        param2 = (i["idDegagement"],)
        r2 = bddGen.selectData(func_name(), sql2, param2)
        for j in r2:
            l.append(j)    # Création d'une liste de dictionnaires contenant les notams de chaque aéroport de déroutement
    return l if l!=None else []

def get_noms():
    # Renvoie la liste des noms des aéroports
    dictnoms = {}
    sql = "SELECT idAerodrome, nomAerodrome FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None)
    for i in r:
        dictnoms[i["idAerodrome"]] = i["nomAerodrome"]
    dictnoms['null'] = ''
    return dictnoms if dictnoms!=None else []

def get_oaci():
    # Renvoie la liste des codes oaci des aéroports
    dictoaci = {}
    sql = "SELECT idAerodrome, codeAerodrome FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None)
    for i in r:
        dictoaci[i["idAerodrome"]] = i["codeAerodrome"]
    return dictoaci if dictoaci!=None else []

def update_idData(idNotam, newvalue):
    sql = "UPDATE Notam SET idNotam=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def update_typeData(idNotam, newvalue):
    sql = "UPDATE Notam SET typeNotam=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def update_windowData(idNotam, newvalue):
    sql = "UPDATE Notam SET creneau=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def update_descData(idNotam, newvalue):
    sql = "UPDATE Notam SET description=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def update_floorData(idNotam, newvalue):
    sql = "UPDATE Notam SET limite_inferieur=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def update_ceilingData(idNotam, newvalue):
    sql = "UPDATE Notam SET limite_superieur=%s WHERE idNotam=%s;"
    param = (newvalue, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def get_tousLesVols(idUser):
    # Renvoie la liste de tous les vols d'un utilisateur
    sql = "SELECT * FROM vol_user WHERE idUser=%s"
    param = (idUser,)
    r = bddGen.selectData(func_name(), sql, param)
    return r if r!=None else []

def get_aeroVol(idVol):
    # Renvoie la liste de tous les aérodromes d'un vol
    sql = "SELECT idDepart, idArrivee FROM vol WHERE idVol=%s"
    param = (idVol,)
    r = bddGen.selectData(func_name(), sql, param)
    return r[0] if r!=None else []

def get_idDeroute(idVol):
    # Renvoie la liste de tous les aéroports de dégagement d'un vol
    l = []
    sql = "SELECT idDegagement FROM degagement_vol WHERE idVol=%s"
    param = (idVol,)
    r = bddGen.selectData(func_name(), sql, param)
    for i in r:
        l.append(i['idDegagement'])
    return l if l!=None else []
