from . import bddGen
import inspect
import hashlib

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



def del_notamData(idNotam, msg=None):
    sql = "DELETE FROM Notam WHERE idNotam=%s;"
    param = (idNotam,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def del_volData(idVol, msg=None):
    sql = "DELETE FROM Vol WHERE idVol=%s;"
    param = (idVol,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def add_airportData(rform, msg=None):
    sql = """ INSERT INTO aerodrome
    (codeAerodrome, nomAerodrome, region, departement, ville, pays)
    VALUES (%s, %s, %s, %s, %s, %s); """
    param = ( rform['codeAerodrome'], rform['nomAerodrome'], rform['region'], rform['departement'], rform['ville'], rform['pays'] )
    return bddGen.addData(func_name(), sql, param, msg)

def update_notam(idNotam, newdesc):
    sql = "UPDATE Notam SET description=%s WHERE idNotam=%s;"
    param = (newdesc, idNotam)
    return bddGen.updateData(func_name(), sql, param, None)

def get_airports():
    # Renvoie la liste de tous les aéroports
    sql = f"SELECT idAerodrome, nomAerodrome FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_notams():
    # Renvoie la liste de tous les notams
    sql = f"SELECT * FROM Notam"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_vols():
    # Renvoie la liste de tous les vols
    sql = f"SELECT * FROM Vol"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_notamsVol(idAero):
    # Renvoie la liste de tous les vols
    sql = "SELECT * FROM Notam WHERE idAerodrome=%s"
    param = (idAero,)
    r = bddGen.selectData(func_name(), sql, param)
    return r if r!=None else []

def get_deroutement(idVol):
    # Renvoie la liste de tous les aérodromes de déroutement d'un vol
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
        #print(i["idAerodrome"],i["nomAerodrome"],'oooooooooooooooooooooo')
        dictnoms[i["idAerodrome"]] = i["nomAerodrome"]
    return dictnoms if dictnoms!=None else []