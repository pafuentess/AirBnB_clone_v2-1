#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_all_amenities():
    """ Retrieves the list of amenities """
    amenities = storage.all("Amenity")
    amenities = [i.to_dict() for i in amenities.values()
                 if i.state_id == state_id]
    return (jsonify(amenities))


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenity(amenity_id=None):
    """ Retrieves a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ delete amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    amenity.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """ create amenity """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    instance = Amenity(**request.get_json())
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ update state """
    keys = ['id', 'created_at', 'updated_at']
    amenity = storage.get('Amenity', amenity_id)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(state, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
