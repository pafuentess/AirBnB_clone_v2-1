#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    """ Retrieves the list of all State """
    all_states = []
    for value in storage.all("State").values():
        all_states.append(value.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_id(state_id):
    """ Retrieves a State object """
    state = (storage.get('State', state_id)).to_dict()
    if state is None:
        abort(404)
    else:
        return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_state(state_id):
    """Deletes a State object"""
    try:
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def Post_state():
    """ Create a State object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    instance = State(**request.get_json())
    storage.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update state """
    keys = ['id', 'created_at', 'updated_at']
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get('State', state_id)
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(state, key, value)
    return jsonify(state.to_dict())
