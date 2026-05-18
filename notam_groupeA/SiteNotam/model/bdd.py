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
    sql = "SELECT * FROM User where login=%s and mdp=%s"
    param = (login, mdpC)
    return bddGen.selectOneData(func_name(), sql, param)


def update_userMdpData(newmdp, idUser):
    sql = "UPDATE User SET mdp=%s WHERE idUser=%s;"
    param = (newmdp, idUser)
    return bddGen.updateData(func_name(), sql, param, None)

def add_membreData(rform, msg=None):
    sql = """ INSERT INTO User
    (nom, prenom, login, mdp, role, avatar)
    VALUES (%s, %s, %s, %s, %s, %s); """
    mdp=rform['mdp']
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
    # avatar = rform['avatar']
    avatar = None
    param = ( rform['lastname'], rform['firstname'], rform['username'], mdpC,
    rform.get('role'), avatar )
    return bddGen.addData(func_name(), sql, param, msg)
