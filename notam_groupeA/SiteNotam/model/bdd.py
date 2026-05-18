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



def add_userData(rform, mdp_hash, msg=None):
    sql = """ INSERT INTO User(prenom, nom, mdp, login, role)
    VALUES (%s, %s, %s, %s, %s); """
    param = ( rform['prenom'], rform['nom'], mdp_hash, rform['login'], rform['role'] )
    return bddGen.addData(func_name(), sql, param, msg)
