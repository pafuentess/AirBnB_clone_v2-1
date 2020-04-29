#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_place_review(place_id=None):
    """ Retrieves the list of all Reviews of place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    places = [i.to_dict() for i in place.reviews]
    return (jsonify(places))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_review(review_id=None):
    """ retrieve reviews """
    reviews = storage.get("Review", review_id)
    if reviews is None:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ delete review by id """
    reviews = storage.get("Review", review_id)
    if reviews is None:
        abort(404)
    storage.delete(reviews)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_reviews_of_place_id(place_id=None):
    """ create reviews of place_id """
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    if 'text' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    if not storage.get('User', request.get_json()['user_id']):
        abort(404)
    dic = request.get_json()
    instance = Review(**dic)
    instance.place_id = place_id
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews(review_id):
    """ update review """
    keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
