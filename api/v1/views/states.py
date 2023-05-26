#!/usr/bin/python3
"""A script that runs a flask application"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    states = storage.all("State").values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """Retrieves the list of State objects"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """ Deletes a state object if the state_id is not linked
        to any State object.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    del state
    storage.save()
    return jsonify({}, 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Transform HTTP body request to dictionary"""
    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')

    if "name" not in state_json:
        abort(400, 'Missing name')
    new_state = State(**state_json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """Update a state resource"""
    state_json = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not state_json:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict())
