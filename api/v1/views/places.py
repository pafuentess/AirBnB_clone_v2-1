#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_all_places(city_id):
    """ Retrieves the list of amenities """
    cities = storage.get('City', city_id)
    if cities is None:
        abort(404)
    return jsonify([i.to_dict() for i in
                   storage.get('City', city_id).places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_places_id(place_id):
    """ Retrieves a Amenity object """
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ delete amenity """
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create place """
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    info = request.get_json()
    if info is None:
        abort(400, "Not a JSON")
    if "user_id" not in info:
        abort(400, "Missing user_id")
    user = storage.get("User", info["user_id"])
    if user is None:
        abort(404)
    if "name" not in info:
        abort(400, "Missing name")
    info["city_id"] = city_id
    place = Place(**info)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update state """
    keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
