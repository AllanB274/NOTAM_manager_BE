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