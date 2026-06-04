import secrets
import string
import hashlib
from flask import flash
import hashlib


from flask import Flask, flash, render_template, request, redirect, session, send_file, jsonify
from .model import bdd as bdd
from .controller import function as f
app = Flask(__name__)

app.template_folder = "template"
app.static_folder = "static"
app.config.from_object('SiteNotam.config')

# page accueil
@app.route("/")
def index():
    airports = bdd.get_airports()
    return render_template("index.html", airports=airports)

# page notams
@app.route("/notam")
def notam():
    lnotam = bdd.get_notams()
    lairports = bdd.get_airports()
    lcodes = bdd.get_oaci()
    print(type(lcodes[lnotam[1]['idAerodrome']]))
    return render_template("notam.html", notams=lnotam, airports=lairports, codes=lcodes)

# page sgbd
@app.route("/vols")
@f.statuts_obligatoires('admin', 'client')
def vols():
    lvols = bdd.get_vols()
    return render_template("vols.html", vols=lvols)

# log in
@app.route("/compte")
@f.statuts_interdits('admin', 'client')
def compte():
    return render_template("compte.html")

# sign up
@app.route("/signup", methods=["POST", "GET"])
@f.statuts_interdits('admin', 'client')
def signup():
    rform = request.form
    if request.method == "POST":
        msg= {
            "ok":"Nouveau membre inséré",
            "echec":"Problème ajout utilisateur"
        }
        try :
            bdd.add_membreData(rform,msg)
            return redirect("/compte")
        except TypeError as err:
        #Refus
            flash("Account refused", "danger")
            return redirect("/signup")
    else:
        return render_template("signup.html")


# ajouterAirport

@app.route("/ajouterAirport", methods=["POST", "GET"])
def ajouterAirport():
    rform = request.form
    if request.method == "POST":
        msg= {
            "ok":"Nouvel Aeroport inséré",
            "echec":"Problème ajout Aeroport"
        }
        try :
            bdd.add_airportData(rform,msg)
            return redirect("/vols")
        except TypeError as err:
        #Refus
            flash("Airport refused", "danger")
            return redirect("/ajouterAirport")
    else:
        return render_template("ajouterAirport.html")

@app.route("/ajouterNotam")
def ajouterNotam():
    airports = bdd.get_airports()
    return render_template("ajouterNotam.html", airports=airports)

# about us
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

# @app.route("/addmdp")
# def addmdp():
#     rform = request.form
#     msg={
#         "ok": "Mot de passe valide",
#         "echec" : "Mot de passe invalide"
#     }
    
#     #genere mdp aléatoire de 5 caractères
#     caracteres = string.ascii_letters + string.digits
#     mdp = ''.join(secrets.choice(caracteres) for _ in range(5))
#     print("Mot de passe généré:", mdp)
    
#     #Chiffrement SHA-256
#     mdp_hash = hashlib.sha256(mdp.encode()).hexdigest()
#     print("Mot de passe chiffré:", mdp_hash)
   
    
#     #création user
#     idUser = bdd.add_userData(rform, mdp_hash, msg)
#     print(idUser)
#     flash(mdp)
#     return redirect("/modifMdp")


@app.route("/modifMdp", methods=["POST", "GET"])
@f.statuts_obligatoires('admin', 'client')
def modifMdp():
    rform = request.form
    if request.method == "POST":
        ancien = rform.get("oldmdp")
        nouveau = rform.get("newmdp")
        confirmation = rform.get("confirmMdp")
        if nouveau == confirmation:
            new_mdp_hash = hashlib.sha256(nouveau.encode()).hexdigest()
            if bdd.verifAuthData(session['login'], ancien):
                bdd.update_userMdpData(new_mdp_hash, session["idUser"])
            
                flash("BRAVO MDP modified", "success")
            else:
                flash("Mot de passe erroné!", "danger")
            return redirect("/modifMdp")
        else:
            flash("Les deux mots de passe ne correspondent pas!", "danger")
            return redirect("/modifMdp")
    return render_template("modifMdp.html")

def verifAuth(login, mdp):
    mdp = hashlib.sha256(mdp.encode())
    mdpC = mdp.hexdigest() #mot de passe chiffré
#la connexion
@app.route("/connexion", methods=["POST"])
def connect():
    login = request.form['login']
    mdp = request.form['mdp']
    user = bdd.verifAuthData(login, mdp)
    try:
        #Réussite
        session["idUser"] = user["idUser"]
        session["nom"] = user["nom"]
        session["prenom"] = user["prenom"]
        # session["mail"] = user["mail"]
        session['login'] = user['login']
        session["statut"] = user["role"]
        session["avatar"] = user["avatar"]
        flash("Authentification réussie", "success")
        return redirect("/vols")
    except TypeError as err:
        #Refus
        flash("Authentification refusée", "danger")
        return redirect("/compte")

#la déconnexion
@app.route("/deco")
def deco():
    session.clear()
    flash("Vous êtes bien déconnecté.", "info")
    return redirect("/compte")

@app.route("/suppNotam/<idNotam>")
def suppNotam(idNotam):
    msg= {
        "ok":"Le notam a bien été supprimé",
        "echec":"Problème suppression notam"
    }
    bdd.del_notamData(idNotam,msg)
    return redirect("/notam")

@app.route("/suppAeroport/<idAeroport>")
def suppAeroport(idAeroport):
    msg= {
        "ok":"L'aéroport' a bien été supprimé",
        "echec":"Problème suppression aéroport"
    }
    bdd.del_aeroportData(idAeroport,msg)
    return redirect("/notam")

@app.route("/suppVol/<idVol>")
def suppVol(idVol):
    msg= {
        "ok":"Le vol a bien été supprimé",
        "echec":"Problème suppression vol"
    }
    bdd.del_volData(idVol,msg)
    return redirect("/vols")

@app.route("/versvol", methods=["POST","GET"])
def versvol():
    departure = request.form.get('departure2')
    arrival = request.form.get('arrival2')
    print(arrival, len(arrival), "arr")
    print(departure, len(departure), "dep")
    vol = bdd.verifVolExist(departure, arrival)
    try:
        #Réussite
        session["idArrivee"] = vol["idArrivee"]
        session["idDepart"] = vol["idDepart"]
        session["idVol"] = vol["idVol"]
        flash("Bon voyage", "success")
        return redirect("/volsanss")
    except TypeError as err:
        #Refus
        flash("Le vol n'existe pas", "danger")
        return redirect("/")

@app.route("/volsanss")
def volSansS():
    dictidaero, dictnotamsparaero = {}, {}
    lnotamvolsdep = bdd.get_notamsVol(session["idDepart"])
    lnotamvolsarr = bdd.get_notamsVol(session["idArrivee"])
    lnotamderoutement = bdd.get_deroutement(session["idVol"])
    lnoms = bdd.get_noms()
    for i,v in enumerate(lnotamderoutement):
        if v["idAerodrome"] in dictidaero.keys():
            dictidaero[v["idAerodrome"]] += 1
        else:
            dictidaero[v["idAerodrome"]] = 1
    for i in lnotamderoutement:
        if i["idAerodrome"] in dictnotamsparaero.keys():
            dictnotamsparaero[i["idAerodrome"]].append(i)
        else:
            dictnotamsparaero[i["idAerodrome"]] = [i]
    return render_template("volsanss.html", notamsdep=lnotamvolsdep, notamsarr=lnotamvolsarr, notamsderoute=dictnotamsparaero, dictid=dictidaero, noms=lnoms)

@app.route("/editNotam", methods=["POST"])
@f.statuts_obligatoires('admin')
def editNotam():
    notam = request.form['edit']
    linfos = []
    temp = ''
    for i in notam :
        if i != '$':
            temp += i
        else:
            linfos.append(temp)
            temp = ''
    return render_template('editNotam.html', notam=linfos)

@app.route("/updateId", methods=['POST'])
def updateId():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_idData(idNotam, newvalue)
    return "1"

@app.route("/updateType", methods=['POST'])
def updateType():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_typeData(idNotam, newvalue)
    return "1"

@app.route("/updateWindow", methods=['POST'])
def updateWindow():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_windowData(idNotam, newvalue)
    return "1"

@app.route("/updateDesc", methods=['POST'])
def updateDesc():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_descData(idNotam, newvalue)
    return "1"

@app.route("/updateFloor", methods=['POST'])
def updateFloor():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_floorData(idNotam, newvalue)
    return "1"

@app.route("/updateCeiling", methods=['POST'])
def updateCeiling():
    # réception des données du formulaire
    idNotam = request.form['pk']
    newvalue = request.form['value']
    bdd.update_ceilingData(idNotam, newvalue)
    return "1"