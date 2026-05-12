import mysql.connector
from mysql.connector import pooling
from flask import flash
from ..config import DB_SERVER, COLOR

# ------------------------------
# Pool de connexions
# ------------------------------
cnx_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
    **DB_SERVER
)

# ------------------------------
# Récupère une connexion du pool
# ------------------------------
def connexion():
    try:
        return cnx_pool.get_connection()
    except mysql.connector.Error as err:
        msg = f"{err} <br /> Veuillez vérifier les paramètres dans config.py"
        flash(msg, "danger")
        print(f"{COLOR['red']}{msg}{COLOR['end']}")
        return None


# ------------------------------
# Execution d'une requête sql
# ------------------------------
def queryData(type, sql, param, funct_name, message=None):
    cnx = connexion()
    if cnx is None:
        return None
    try:
        cursor = cnx.cursor(dictionary=True)
        
        if type=="addMany":
            cursor.executemany(sql, param)
            res= cursor.lastrowid
        else:
            cursor.execute(sql, param)
            if type=="select":
                res = cursor.fetchall()
            elif type=="selectOne":
                res = cursor.fetchone()
            elif type=="add":
                res= cursor.lastrowid
            elif type=="delete" or type=="update":
                res = True
            else:
                res = False
            
        cnx.commit()
        cursor.close()
        if message:
            flash(message['ok'], "success")
        print(f"{COLOR['green']}{funct_name}{COLOR['end']}")
        return res
        
    except mysql.connector.Error as err:
        msg = f"{message['echec']}: {err}" if message else str(err)
        flash(msg, "danger")
        print(f"{COLOR['red']}{sql}\n{funct_name}\n{err}{COLOR['end']}")
        return None
    finally:
        cnx.close()  # retourne la connexion au pool


# Select avec fetchall
def selectData(funct_name, sql, param=None,  message=None):
    return queryData("select", sql, param, funct_name, message)

# Select avec fetchOne
def selectOneData(funct_name, sql, param=None, message=None):
    return queryData("selectOne", sql, param, funct_name, message)

# insert
def addData(funct_name, sql, param=None, message=None):
    return queryData("add", sql, param, funct_name, message)

# insert
def addManyData(funct_name, sql, param=None, message=None):
    return queryData("addMany", sql, param, funct_name, message)

# delete
def deleteData(funct_name, sql, param=None, message=None):
    return queryData("delete", sql, param, funct_name, message)

# update
def updateData(funct_name, sql, param=None, message=None):
    return queryData("update", sql, param, funct_name, message)