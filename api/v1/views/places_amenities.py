#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import Place
from models.review import Amenity
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
		for db_amenities in place.amenities:
			amenity.append(db_amenities.to_dict())
	else:
		for f_amenities in place.amenity_ids:
			amenity.append(storage.get('Amenity', f_amenities).to_dict())
	return jsonify(amenity)

    
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ delete amenity of Place """
    place = storage.get("Place", review_id)
	amenity = storage.get("Amenity", amenity_id)
	if place is None:
        abort(404)
	place_amenity = []
	if getenv('HBNB_TYPE_STORAGE') == 'db':
		for db_amenities in place.amenities:
			place_amenity.append(db_amenities.to_dict())
	else:
		for f_amenities in place.amenity_ids:
			place_amenity.append(storage.get('Amenity', f_amenities).to_dict())
    if amenity is not place_amenity:
		abort(404)
	place_amenity.remove(amenity)
	storage.save()
	return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_reviews_of_place_id(place_id=None):
    """ create reviews of place_id """
    place = storage.get("Place", review_id)
	amenity = storage.get("Amenity", amenity_id)
	if place is None:
        abort(404)
	place_amenity = []
	if getenv('HBNB_TYPE_STORAGE') == 'db':
		for db_amenities in place.amenities:
			place_amenity.append(db_amenities.to_dict())
	else:
		for f_amenities in place.amenity_ids:
			place_amenity.append(storage.get('Amenity', f_amenities).to_dict())
	if amenity in place_amenity:
		return jsonify(amenity.to_dict()), 200
	place_amenity.append(amenity)
	place.save()
	return jsonify(amenity.to_dict()), 201
