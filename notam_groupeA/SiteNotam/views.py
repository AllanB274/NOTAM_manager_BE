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

# voir son compte
@app.route("/compte")
def compte():
    return render_template("compte.html")