#!/usr/bin/python3
"""A script that runs a flask application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
# Register the blueprint
app.register_blueprint(app_views)

# Initialize CORS
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown_app_context(exception):
    """It removes the current SQLAlchemy sessions after each requests"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ get host and port from environmental variables, or
        use the default
    """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
