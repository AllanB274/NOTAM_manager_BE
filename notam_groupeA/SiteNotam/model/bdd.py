from . import bddGen
import inspect

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
    sql = "SELECT * FROM user where login=%s and mdp=%s"
    param = (login, mdp)
    return bddGen.selectOneData(func_name(), sql, param)