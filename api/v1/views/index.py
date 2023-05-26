#!/usr/bin/python3
"""A script that runs a flask application"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return json"""
    return jsonify({'status': 'OK'})
