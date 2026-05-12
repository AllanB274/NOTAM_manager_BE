from flask import Flask, flash, render_template, request, redirect, session, send_file
from .model import bdd as bdd
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
        session["mail"] = user["mail"]
        session['login'] = user['login']
        session["statut"] = user["statut"]
        session["avatar"] = user["avatar"]
        flash("Authentification réussie", "success")
        return redirect("/vols")
    except TypeError as err:
        #Refus
        flash("Authentification refusée", "danger")
        return redirect("/login")

#la déconnexion
@app.route("/deco")
def deco():
    session.clear()
    flash("Casse-toi et reviens plus jamais fdp", "primary")
    return redirect("/compte")