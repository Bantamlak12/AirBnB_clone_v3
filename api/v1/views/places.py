#!/usr/bin/python3
"""A view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    place.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_json = request.get_json()
    if not place_json:
        abort(400, 'Not a JSON')
    if 'user_id' not in place_json:
        abort(400, 'Missing user_id')
    user_id = place_json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in place_json:
        abort(400, 'Missing name')
    new_place = Place(**place_json)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_json = request.get_json()
    if not place_json:
        abort(400, 'Not a JSON')
    for k, v in place_json.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
