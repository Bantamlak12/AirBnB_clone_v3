#!/usr/bin/python3
""" A view for the link between Place objects and Amenity objects
    that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_of_place(place_id):
    """Retrieves the list of all Amenity objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_to_place(place_id, amenity_id):
    """Deletes Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Links Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    storage.save()
    return jsonify(amenity.to_dict()), 201
