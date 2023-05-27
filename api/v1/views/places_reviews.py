#!/usr/bin/python3
"""A  view for Review object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    if not storage(Place, place_id):
        abort(404)

    review_json = request.get_json()
    if not review_json:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_json:
        abort(400, 'Missing user_id')

    user_id = review_json['user_id']
    if not storage(User, user_id):
        abort(404)

    if 'text' not in review_json:
        abort(400, 'Missing text')

    new_review = Review(**review_json)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review_json = request.get_json()
    if not review_json:
        abort(400, 'Not a JSON')

    for k, v in review_json.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
