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
    airports = bdd.get_airports(None)
    return render_template("index.html", airports=airports)

# page notams
@app.route("/notam")
def notam():
    return render_template("notam.html")

# page sgbd
@app.route("/vols")
@f.statuts_obligatoires('admin', 'client')
def vols():
    return render_template("vols.html")

# log in
@app.route("/compte")
@f.statuts_interdits('admin', 'client')
def compte():
    return render_template("compte.html")

# sign up
@app.route("/signup", methods=["POST", "GET"])
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
        bdd.add_airportData(rform,msg)
        return redirect("/vols")
    else:
        return render_template("ajouterAirport.html")


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
    print(user)
    try:
        #Réussite
        session["idUser"] = user["idUser"]
        session["nom"] = user["nom"]
        session["prenom"] = user["prenom"]
        # session["mail"] = user["mail"]
        session['login'] = user['login']
        session["statut"] = user["role"]
        # session["avatar"] = user["avatar"]
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

@app.route("/suppMembre/<idUser>")
def suprMembre(idUser):
    msg= {
        "ok":"L'utilisateur a bien été supprimé",
        "echec":"Problème suppression utilisateur"
    }
    bdd.del_membreData(idUser,msg)
    return redirect("/notam")

@app.route("/updateNotam", methods=['POST'])
def updateNom():
    idDesc = request.form['pk']
    newdesc = request.form['value']
    bdd.update_notam(idDesc, newdesc)
    return "1"
