# Vérifie que l'utilisateur est connecté et possède un rôle autorisé
from functools import wraps
from flask import Flask, flash, render_template, request, redirect, session, send_file

def statuts_obligatoires(*statuts_autorises):
    def decorateur(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Vérifie que l'utilisateur est connecté
            if 'idUser' not in session or 'statut' not in session:
                flash("Vous devez être connecté pour accéder à cette page.", "danger")
                return redirect("/connecter")
            # Vérifie que le rôle est autorisé
            if session['statut'] not in statuts_autorises:
                flash("Vous n'avez pas les droits pour accéder à cette page.", "danger")
                # Redirection selon le rôle
                routes = {
                    "administrateur": "/vols",
                    "pilote": "/vols"
                }
                route_suivante = routes.get(session['statut'], "/")
                return redirect(route_suivante)
            return f(*args, **kwargs) # Exécute la route si tout est valide
        return wrapper
    return decorateur
