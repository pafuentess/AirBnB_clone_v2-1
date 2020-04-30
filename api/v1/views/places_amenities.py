#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def retrieve_place_amenities(place_id):
    """ Retrieves the list of all amenities of place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_places = place.amenities
    else:
        amenity_places = place.amenity_ids
    for f_amenities in amenity_places:
        amenity.append(f_amenities.to_dict())
    return jsonify(amenity), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ delete amenity of Place """
    place = storage.get("Place", review_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_places = place.amenities
    else:
        amenity_places = place.amenity_ids
    if amenity not in amenity_places:
        abort(404)
    amenity_places.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenities_of_place_id(place_id=None):
    """ create reviews of place_id """
    place = storage.get("Place", review_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_places = place.amenities
    else:
        amenity_places = place.amenity_ids
    if amenity in amenity_places:
        return jsonify(amenity.to_dict()), 200
    amenity_places.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
