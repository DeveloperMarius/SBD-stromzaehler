import json
from flask import jsonify, Blueprint, request
from auth_middleware import token_required
from variables import Variables
from models import StromzaehlerLog, StromzaehlerReading
from sqlalchemy import select


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
    return jsonify({
        'success': True
    }), 200


@api_routes_blueprint.route('/stromzaehler/update', methods=['POST'])
@token_required
def stromzaehler_update(stromzaehler):
    data = request.data

    statement = select(StromzaehlerReading).where(StromzaehlerReading.stromzaehler == stromzaehler).order_by(StromzaehlerReading.timestamp.desc()).limit(1)
    last_reading = Variables.get_database().session.scalar(statement)
    readings = []
    for reading in data['readings']:
        if last_reading is not None and reading['id'] <= last_reading['source_id']:
            continue
        readings.append(StromzaehlerReading(
            stromzaehler=stromzaehler,
            source_id=reading['id'],
            timestamp=reading['timestamp'],
            value=reading['value']
        ))
    Variables.get_database().session.add_all(readings)

    statement = select(StromzaehlerLog).where(StromzaehlerLog.stromzaehler == stromzaehler).order_by(StromzaehlerLog.timestamp.desc()).limit(1)
    last_log = Variables.get_database().session.scalar(statement)
    logs = []
    for log in data['logs']:
        if last_log is not None and log['id'] <= last_log['source_id']:
            continue
        logs.append(StromzaehlerLog(
            stromzaehler=stromzaehler,
            source_id=log['id'],
            timestamp=log['timestamp'],
            message=log['message']
        ))
    Variables.get_database().session.add_all(logs)

    Variables.get_database().session.commit()
    return jsonify({
        'success': True
    }), 200
