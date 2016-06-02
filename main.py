# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
import json, os, psycopg2, urlparse
from db import Db # voyez db.py

app = Flask(__name__)
app.debug = True

##################################################################

@app.route('/debug/db/reset')
def route_dbinit():
  """Cette route sert à initialiser (ou nettoyer) la base de données."""
  db = Db()
  db.executeFile("database_reset.sql")
  db.close()
  return "Done."

#-----------------------------------------------------------------

@app.route('/', methods=['GET'])
def home():
  return "Voir le sujet sur e-learning pour plus d'informations."
  
#-----------------------------------------------------------------

@app.route('/prets', methods=['GET'])
def prets_fetchall():
  db = Db()
  result = db.select("SELECT * FROM prets")
  db.close()
  
  resp = make_response(json.dumps(result))
  resp.mimetype = 'application/json'
  return resp

#-----------------------------------------------------------------

@app.route('/prets', methods=['POST'])
def prets_add():
  data = request.get_json()

  if (data["statut"] == "prete") or (data["statut"] == "rendu") or (data["statut"] == "annule"):
    db = Db()
    db.execute("INSERT INTO prets (quoi, qui, statut) VALUES (%(quoi)s, %(qui)s, %(statut)s)", {
      'quoi': data["quoi"],
      'qui': data["qui"],
      'statut': data["statut"]
    })
	
    last_id =  db.lastrowid()

    db.close()
  
    resp = make_response("OK", 201)
    resp.headers['Location'] = '/prets/%d' % last_id
  else:
    resp = make_response("Le prêt n'a pas pu être créé.", 400)

  return resp

#-----------------------------------------------------------------

@app.route('/prets/<int:id>')
def prets_fetchone(id):
  db = Db()
  result = db.select("SELECT * FROM prets WHERE id = %(id)s", {
    'id': id
  })
  db.close()
  
  if len(result) < 1:
    return make_response("Not found", 404)
  
  resp = make_response(json.dumps(result))
  resp.mimetype = 'application/json'
  return resp

#-----------------------------------------------------------------

@app.route('/prets/<int:id>', methods=['PUT'])
def prets_updateone(id):
  data = request.get_json()
  
  if (data["statut"] == "prete") or (data["statut"] == "rendu") or (data["statut"] == "annule"):
    db = Db()
    result = db.execute("UPDATE prets SET quoi = %(quoi)s, qui = %(qui)s, statut = %(statut)s WHERE id = %(id)s", {
      'quoi': data["quoi"],
      'qui': data["qui"],
      'statut': data["statut"],
      'id': id
    })
    db.close()
  
    if len(result) < 1:
      return make_response("Not found", 404)
  
    resp = make_response("", 204)
    resp.mimetype = 'application/json'
  else:
    resp = make_response("Le prêt n'a pas pu être modifié.", 400)

  return resp

#-----------------------------------------------------------------

if __name__ == "__main__":
  app.run()
