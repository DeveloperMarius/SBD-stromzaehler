from flask import jsonify, Blueprint, request
from auth_middleware import token_required
from variables import Variables
from datetime import datetime

api_routes_blueprint = Blueprint('API Routes', __name__)


@api_routes_blueprint.route("/test")
@token_required
def test():
    # request.json
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": "a"
    })


@api_routes_blueprint.route('/healthcheck')
def healthcheck():
    return '', 200


@api_routes_blueprint.route('/stromzaehler/update', methods=['POST'])
@token_required
def stromzaehler_update(stromzaehler):
    data = request.data
    readings = data['readings']
    logs = data['logs']
    for log in logs:
        Variables.get_database().cursor.execute("INSERT INTO 'stromzaehler_logs' VALUES (NULL, ?, ?, ?, ?)", (
            stromzaehler
        ))
    return '', 200


@api_routes_blueprint.route('/stromzaehler/history', methods=['GET'])
@token_required
def get_stromzaehler_history(stromzaehler):
    data = request.data
    try:
        start_date = round(datetime.strptime(data['start_date'], '%Y-%m-%d').timestamp() * 1000)
        end_date = round(datetime.strptime(data['end_date'], '%Y-%m-%d').timestamp() * 1000)
    except:
        return '', 422

