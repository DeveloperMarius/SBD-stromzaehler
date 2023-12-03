import json
import jwt
from flask import jsonify, Blueprint, request
from auth_middleware import token_required
from utils import Variables, get_public_rsa_key, get_private_rsa_key
from datetime import datetime
from models import StromzaehlerLog, StromzaehlerReading, Stromzaehler, Person, Address
from sqlalchemy import select
import hashlib
from cryptography.hazmat.primitives import serialization

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


@api_routes_blueprint.route('/stromzaehler/history', methods=['GET'])
@token_required
def get_stromzaehler_history(stromzaehler):
    data = request.json
    try:
        start_date = round(datetime.strptime(data['start_date'], '%Y-%m-%d').timestamp() * 1000)
        end_date = round(datetime.strptime(data['end_date'], '%Y-%m-%d').timestamp() * 1000)
        stromzaehler_id = data['stromzaehler_id']
    except Exception as e:
        print(e)
        return '', 422

    statement = select(StromzaehlerReading).where(
        (StromzaehlerReading.stromzaehler == stromzaehler_id) &
        (start_date <= StromzaehlerReading.timestamp) &
        (StromzaehlerReading.timestamp <= end_date)
    ).order_by(StromzaehlerReading.timestamp.desc())
    response = Variables.get_database().session.scalars(statement)
    raw_readings = response.fetchall()

    readings = []
    for i in raw_readings:
        reading = {
            "stromzaehler": i.stromzaehler,
            "timestamp": i.timestamp,
            "value": i.value
        }
        readings.append(reading)

    Variables.get_logger().log(request, f'Provided stromzaehler readings in period: {start_date} - {end_date}.')  # todo get jwt

    body = {
        "readings": readings
    }
    response = jsonify(body)

    jwt_data = {
        'mode': "SHA256",
        'signature': hashlib.sha256(json.dumps(body).encode('utf-8')).hexdigest()
    }

    jwt_token = 'Bearer ' + jwt.encode(jwt_data, get_private_rsa_key(), "RS256")

    response.headers['Authorization'] = jwt_token

    return response


@api_routes_blueprint.route('/public_key', methods=['GET'])
def get_public_key():
    return jsonify({
        'public_key': get_public_rsa_key()
    })
