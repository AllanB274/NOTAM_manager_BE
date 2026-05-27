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


def update_userMdpData(newmdp, idUser):
    sql = "UPDATE user SET mdp=%s WHERE idUser=%s;"
    param = (newmdp, idUser)
    return bddGen.updateData(func_name(), sql, param, None)

def add_membreData(rform, msg=None):
    sql = """ INSERT INTO User
    (nom, prenom, login, mdp, role, avatar)
    VALUES (%s, %s, %s, %s, %s, %s); """
    mdp = rform['mdp']
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
    avatar = rform['avatar']
    # Vérification admin
    if rform['role'] == 'admin':
        if rform['mdpAdmin'] != 'secret':
            raise TypeError("admin key incorrect")

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
    # Renvoie la liste de tout les aéroports
    sql = f"SELECT idAerodrome, nomAerodrome FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_notams():
    # Renvoie la liste de tout les notams
    sql = f"SELECT * FROM Notam"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []

def get_vols():
    # Renvoie la liste de tout les vols
    sql = f"SELECT * FROM Vol"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []