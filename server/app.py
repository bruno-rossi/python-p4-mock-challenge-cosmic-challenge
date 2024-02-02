#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods=['GET', 'POST'])
def scientists():

    if request.method == 'GET':

        scientists = []

        for scientist in Scientist.query.all():
            scientist_dict = scientist.to_dict(rules=['-missions'])
            scientists.append(scientist_dict)

        response = make_response(scientists, 200)

        return response
    
    if request.method == 'POST':

        try:
            new_scientist = Scientist(
            name=request.get_json().get('name'),
            field_of_study=request.get_json().get('field_of_study')
        )
            
            db.session.add(new_scientist)
            db.session.commit()

            new_scientist_dict = new_scientist.to_dict()

            return make_response(new_scientist_dict, 201)
        
        except Exception:
            return {"errors": ["validation errors"]}, 400

@app.route('/scientists/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    
    scientist = Scientist.query.filter(Scientist.id == id).first()
    
    if not scientist:
            return {"error": "Scientist not found"}, 404
    else:
        if request.method == 'GET':

            scientist_dict = scientist.to_dict()
            return scientist_dict, 200
        
        if request.method == 'PATCH':

            try:
                for attr in request.get_json():
                    setattr(scientist, attr, request.get_json()[attr])

                db.session.add(scientist)
                db.session.commit()

                scientist_dict = scientist.to_dict()
                return make_response ( scientist_dict, 202 )
            except Exception:
                return {"errors": ["validation errors"]}, 400
            
        if request.method == 'DELETE':
            db.session.delete(scientist)
            db.session.commit()

            return {}, 204
        
@app.route('/planets')
def planets():
    planets = []

    for planet in Planet.query.all():
        planets.append(planet.to_dict(rules=['-missions']))

    return planets, 200

@app.route('/missions', methods=['GET', 'POST'])
def missions():

    if request.method == 'GET':
        missions_list = []
        for mission in Mission.query.all():
            missions.append(missions_list.to_dict())

    if request.method == 'POST':
        
        try:
            new_mission = Mission(
                name=request.get_json().get('name'),
                scientist_id=request.get_json().get('scientist_id'),
                planet_id=request.get_json().get('planet_id')
            )
            
            db.session.add(new_mission)
            db.session.commit()

            new_mission_dict = new_mission.to_dict()

            return make_response(new_mission_dict, 201)
        
        except Exception:
            return {"errors": ["validation errors"]}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)