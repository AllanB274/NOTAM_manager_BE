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



def add_membreData(rform, msg=None):
   sql = """ INSERT INTO user(prenom, nom, mdp, login, role)
   VALUES (%s, %s, %s, %s, %s); """
   param = ( rform['prenom'], rform['nom'], rform['mdp'], rform['login'], rform['role'] )
   return bddGen.addData(func_name(), sql, param, msg)
