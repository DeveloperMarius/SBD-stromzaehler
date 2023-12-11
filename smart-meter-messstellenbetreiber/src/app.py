from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from api_routes import api_routes_blueprint
import atexit
from utils import Variables
import sys
import traceback

load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")

app = Flask(__name__)
app.register_blueprint(api_routes_blueprint, url_prefix='/api')


@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404


@app.errorhandler(Exception)
def handle_exception(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    log_id = Variables.get_logger().log(request, f"{exc_type}: {str(e)} - {traceback.format_exc()}")
    return jsonify({
        "message": "Error",
        "error": 'Error',
        "log_id": log_id,
        "data": None
    }), 500


if __name__ == "__main__":
    app.run(debug=False)
