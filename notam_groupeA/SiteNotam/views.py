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
    return render_template("index.html")

# page notams
@app.route("/notam")
def notam():
    return render_template("notam.html")

# page sgbd
@app.route("/vols")
@f.statuts_obligatoires('admin', 'gestion', 'client')
def vols():
    return render_template("vols.html")

# log in
@app.route("/compte")
def compte():
    return render_template("compte.html")

# sign in
@app.route("/signin")
def signin():
    return render_template("signin.html")

# about us
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/addmdp")
def addmdp():
    rform = request.form
    msg={
        "ok": "Mot de passe valide",
        "echec" : "Mot de passe invalide"
    }
    
    #genere mdp aléatoire de 5 caractères
    caracteres = string.ascii_letters + string.digits
    mdp = ''.join(secrets.choice(caracteres) for _ in range(5))
    print("Mot de passe généré:", mdp)
    
    #Chiffrement SHA-256
    mdp_hash = hashlib.sha256(mdp.encode()).hexdigest()
    print("Mot de passe chiffré:", mdp_hash)
   
    
    #création user
    idUser = bdd.add_userData(rform, mdp_hash, msg)
    print(idUser)
    flash(mdp)
    return redirect("/modifMdp")


@app.route("/modifMdp", methods=["POST"])
def modifMdp():
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
    flash("Vous êtes bien déconnecté.", "primary")
    return redirect("/compte")
