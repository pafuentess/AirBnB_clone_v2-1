#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_all_users():
    """ Retrieves the list of amenities """
    user = storage.all("User")
    users = [i.to_dict() for i in user.values()]
    return (jsonify(users))


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_users_id(user_id=None):
    """ Retrieves a Amenity object """
    user = storage.get("User", amenity_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """ delete amenity """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_users():
    """ create amenity """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    instance = User(**request.get_json())
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ update state """
    keys = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
