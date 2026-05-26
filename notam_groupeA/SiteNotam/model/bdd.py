from . import bddGen
import inspect
import hashlib

# -----------------------------------
# Retourne le nom de la fonction courante
# -----------------------------------
def func_name():
    return inspect.currentframe().f_back.f_code.co_name


# -----------------------------------
# Retourne les données de la table identification
# -----------------------------------
def get_membresData():
    sql = "SELECT * FROM identification"
    param = None
    return bddGen.selectData(func_name(),sql, param,  None)

def verifAuthData(login, mdp):
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
    sql = "SELECT * FROM user where login=%s and mdp=%s"
    param = (login, mdpC)
    return bddGen.selectOneData(func_name(), sql, param)


def update_userMdpData(newmdp, idUser):
    sql = "UPDATE user SET mdp=%s WHERE idUser=%s;"
    param = (newmdp, idUser)
    return bddGen.updateData(func_name(), sql, param, None)

def add_membreData(rform, msg=None):
    sql = """ INSERT INTO user
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



def del_membreData(idUser, msg=None):
    sql = "DELETE FROM user WHERE idUser=%s;"
    param = (idUser,)
    return bddGen.deleteData(func_name(),sql, param, msg)

def add_airportData(rform, msg=None):
    sql = """ INSERT INTO aerodrome
    (codeAerodrome, nomAerodrome, region, departement, ville, pays)
    VALUES (%s, %s, %s, %s, %s, %s); """
    param = ( rform['codeAerodrome'], rform['nomAerodrome'], rform['region'], rform['departement'], rform['ville'], rform['pays'] )
    return bddGen.addData(func_name(), sql, param, msg)

def update_notam(idDesc, newdesc):
    sql = "UPDATE notam SET description=%s WHERE idDesc=%s;"
    param = (newdesc, idDesc)
    return bddGen.updateData(func_name(), sql, param, None)

def get_airports(exclusion):
    # Renvoie la liste de tout les aéroports sauf les id compris dans exclusion
    sql = f"SELECT idAerodrome, nomAerodrome FROM aerodrome"
    r = bddGen.selectData(func_name(), sql, None, None)
    return r if r!=None else []
