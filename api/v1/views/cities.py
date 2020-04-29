#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_cites_of_state_id(state_id=None):
    """ Retrieves the list of all City objects of a State """
    states = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = storage.all("City")
    cities_of_state = [i.to_dict() for i in cities.values()
                       if i.state_id == state_id]
    return (jsonify(cities_of_state))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id=None):
    """ retrieve cities """
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """ retrieve cities """
    cities = storage.get("City", city_id)
    cities.delete()
    cities.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_cites_of_state_id(state_id=None):
    """ create cities """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    dic = request.get_json()
    dic.update({'state_id': state_id})
    instance = City(**dic)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/cities/<cities_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    """ update state """
    keys = ['id', 'created_at', 'updated_at']
    city = storage.get('City', state_id)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(state, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
