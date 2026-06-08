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
            "ok":"Account created",
            "echec":"Account refused"
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
@f.statuts_obligatoires('admin')
def ajouterAirport():
    rform = request.form
    if request.method == "POST":
        msg= {
            "ok":"New airport created",
            "echec":"Airport addition problem"
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

@app.route("/ajouterNotam", methods=["POST", "GET"])
@f.statuts_obligatoires('admin', 'client')
def ajouterNotam():
    if request.method == "GET":
        airports = bdd.get_airports()
        objects = bdd.get_objects()
        return render_template("ajouterNotam.html", airports=airports, objects=objects)
    else:
        rform = request.form
        msg= {
            "ok":"New Notam added",
            "echec":"Error while adding the Notam"
        }
        try :
            # raise("la")
            bdd.add_notamData(rform,session,msg)
            return redirect("/notam")
        except TypeError as err:
        #Refus
            flash("Notam refused", "danger")
            flash(str(err), "danger")
            return redirect("/ajouterNotam")

# about us
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

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
            
                flash("Password modified", "success")
            else:
                flash("Wrong Password", "danger")
            return redirect("/modifMdp")
        else:
            flash("Passwords doesn't match ", "danger")
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
        flash("Authentication successful", "success")
        return redirect("/vols")
    except TypeError as err:
        #Refus
        flash("Authentication refused", "danger")
        return redirect("/compte")

#la déconnexion
@app.route("/deco")
def deco():
    session.clear()
    flash("Disconnected.", "info")
    return redirect("/compte")

@app.route("/suppNotam/<idNotam>")
@f.statuts_obligatoires('admin')
def suppNotam(idNotam):
    msg= {
        "ok":"The NOTAM has been successfully deleted.",
        "echec":"Notam deletion problem"
    }
    bdd.del_notamData(idNotam,msg)
    return redirect("/notam")

@app.route("/suppAeroport/<idAeroport>")
@f.statuts_obligatoires('admin')
def suppAeroport(idAeroport):
    msg= {
        "ok":"The airport has been successfully deleted",
        "echec":"Airport deletion problem"
    }
    bdd.del_aeroportData(idAeroport,msg)
    return redirect("/notam")

@app.route("/suppVol/<idVol>")
@f.statuts_obligatoires('admin', 'client')
def suppVol(idVol):
    msg= {
        "ok":"The flight has been successfully cancelled.",
        "echec":"Flight cancellation problem"
    }
    bdd.del_volData(idVol,msg)
    return redirect("/vols")

@app.route("/versvol", methods=["POST","GET"])
def versvol():
    departure = request.form.get('departure2')
    arrival = request.form.get('arrival2')
    deroutements = request.form.getlist("degagements[]")
    vol = bdd.verifVolExist(departure, arrival)
    try:
        #Réussite
        session["idArrivee"] = vol["idArrivee"]
        session["idDepart"] = vol["idDepart"]
        session["deroutements"] = deroutements
        session["idVol"] = vol["idVol"]
        flash("Have a nice flight", "success")
        return redirect("/volsanss")
    except TypeError as err:
        #Refus
        session["idArrivee"] = arrival
        session["idDepart"] = departure
        session["deroutements"] = deroutements
        session["idVol"] = None
        flash("Have a nice flight", "success")
        return redirect("/volsanss")

@app.route("/volsanss")
def volSansS():
    dictidaero, dictnotamsparaero = {}, {}
    lnotamvolsdep = bdd.get_notamsVol(session["idDepart"])
    lnotamvolsarr = bdd.get_notamsVol(session["idArrivee"])
    lnoms = bdd.get_noms()
    if session["idDepart"] == session["idArrivee"]:
        dictnotamsparaero = {}
        dictidaero = {}
        lnotamvolsarr = [{"idAerodrome":'null'}]
    else:
        if session["idVol"] == None :
            lnotamderoutement = []
        if session["deroutements"] :
            for i in session["deroutements"]:
                lnotamderoutement+=bdd.get_notamsVol(i)
        else:
            lnotamderoutement = bdd.get_deroutement(session["idVol"])
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

@app.route("/vols")
@f.statuts_obligatoires('admin', 'client')
def vols():
    dictidaero, dictidderoute, lidvol, dictidvol = {}, {}, [], {}
    dictderoute, dictliste, lnomspremache = {}, {}, {}
    lnoms = bdd.get_noms()
    lvolsuser = bdd.get_tousLesVols(session["idUser"])
    for i in lvolsuser:
        lidvol.append(i['idVol'])
    # dictidaero : dictionnaire de dictionnaires de listes de dictionnaires {idVol1 : {idAero1 : [notam1, notam2], idAero2 : [notam1, notam2]}, idVol2 : etc...}
    # pareil avec dictidderoute
    for i in lidvol:
        dictidaero[i] = {bdd.get_aeroVol(i)['idDepart'] : bdd.get_notamsVol(bdd.get_aeroVol(i)['idDepart']), bdd.get_aeroVol(i)['idArrivee'] : bdd.get_notamsVol(bdd.get_aeroVol(i)['idArrivee'])}
        dictderoute[i] = bdd.get_idDeroute(i)
        lnomspremache[i] = [lnoms[bdd.get_aeroVol(i)['idDepart']], lnoms[bdd.get_aeroVol(i)['idArrivee']]]
        dictidvol[i] = [bdd.get_aeroVol(i)['idDepart'], bdd.get_aeroVol(i)['idArrivee']]
    for k,v in dictderoute.items():
        if len(v) == 0:
            dictidderoute[k] = {}
        else:
            for j in v:
                dictliste[j] = bdd.get_notamsVol(j)
            dictidderoute[k] = dictliste

    return render_template("vols.html", notamsaero=dictidaero, notamsderoute=dictidderoute, noms=lnoms, idvols=lidvol, nomspm=lnomspremache, idpm=dictidvol)





@app.route("/ajoutvol", methods=["POST","GET"])
@f.statuts_obligatoires('admin', 'client')
def ajoutvol():
    rform = request.form
    if request.method == "POST":

        msg = {
          "ok": "Flight successfully added",
          "echec": "error creating flight"
        }

        try:
          # Ajout du vol
          idVol = bdd.add_volData(rform, session, None)

          # dégagements
          degagements = rform.getlist("degagements[]")
          bdd.add_volUserData(idVol, session["idUser"], None)
          bdd.add_degagementsData(idVol, degagements, None)
            

          flash("Flight successfully added", "success")
          return redirect("/vols")

        except TypeError as err:
          flash("Flight denied", "danger")
          return redirect("/vols")
    
    else:
        lairports = bdd.get_airports()
        lcodes = bdd.get_oaci()
        return render_template("ajouterVol.html",airports = lairports, codes = lcodes)

        
