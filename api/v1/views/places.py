#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_all_places(city_id):
    """ Retrieves the list of amenities """
    if states is None:
        abort(404)
    place = storage.all("Place")
    places_of_cities = [i.to_dict() for i in place.values()
                        if i.city_id == city_id]
    return (jsonify(places_of_state))


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_places_id(place_id=None):
    """ Retrieves a Amenity object """
    place = storage.get("Place", place_id)
    if user is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """ delete amenity """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ create amenity """
    cities = storage.all("City"
    if "city.{}".format(city_id) not in cities:
        abort (404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    dic = request.get_json()
    dic.update({'city_id': city_id})
    instance = Place(**dic)
    instance.save()
    return jsonify(instance.to_dict()), 201



@app_views.route('/place/<place_id>',
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
