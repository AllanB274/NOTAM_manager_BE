import secrets
import string
import hashlib
from flask import flash



from flask import Flask, render_template, request, redirect, session, jsonify
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


@app.route("/modifMdp")
def modifMdp():
    return render_template("modifMdp.html")