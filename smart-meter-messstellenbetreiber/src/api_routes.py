from flask import jsonify, Blueprint, request
from auth_middleware import token_required
from utils import Variables, get_public_rsa_key, signing_response
from datetime import datetime
from models import StromzaehlerLog, StromzaehlerReading, Stromzaehler, Person, Address
from sqlalchemy import select
from sqlalchemy.orm import Session

api_routes_blueprint = Blueprint('API Routes', __name__)


@api_routes_blueprint.route('/healthcheck')
def healthcheck():
    return jsonify({
        'success': True
    }), 200


@api_routes_blueprint.route('/stromzaehler/update', methods=['POST'])
@token_required('stromzaehler')
def stromzaehler_update(stromzaehler):
    data = request.json

    with Session(Variables.get_database().get_engin()) as session:
        statement = select(StromzaehlerReading).where(StromzaehlerReading.stromzaehler == stromzaehler).order_by(StromzaehlerReading.timestamp.desc()).limit(1)
        last_reading = session.scalar(statement)
        readings = []
        for reading in data['readings']:
            if last_reading is not None and reading['id'] <= last_reading.source_id:
                continue
            readings.append(StromzaehlerReading(
                stromzaehler=stromzaehler,
                source_id=reading['id'],
                timestamp=reading['timestamp'],
                value=reading['value']
            ))
        session.add_all(readings)

        statement = select(StromzaehlerLog).where(StromzaehlerLog.stromzaehler == stromzaehler).order_by(StromzaehlerLog.timestamp.desc()).limit(1)
        last_log = session.scalar(statement)
        logs = []
        for log in data['logs']:
            if last_log is not None and log['id'] <= last_log.source_id:
                continue
            logs.append(StromzaehlerLog(
                stromzaehler=stromzaehler,
                source_id=log['id'],
                timestamp=log['timestamp'],
                message=log['message']
            ))
        session.add_all(logs)

        session.commit()
    return jsonify({
        'success': True
    }), 200


@api_routes_blueprint.route('/stromzaehler/history', methods=['GET'])
@token_required('kundenportal')
def get_stromzaehler_history(stromzaehler):
    data = request.json
    try:
        start_date = round(datetime.strptime(data['start_date'], '%Y-%m-%d').timestamp() * 1000)
        end_date = round(datetime.strptime(data['end_date'], '%Y-%m-%d').timestamp() * 1000)
        stromzaehler_id = data['stromzaehler_id']
    except Exception as e:
        print(f"Unprocessable Entity: {e}")
        return '', 422

    with Session(Variables.get_database().get_engin()) as session:
        statement = select(StromzaehlerReading).where(
            (StromzaehlerReading.stromzaehler == stromzaehler_id) &
            (start_date <= StromzaehlerReading.timestamp) &
            (StromzaehlerReading.timestamp <= end_date)
        ).order_by(StromzaehlerReading.timestamp.desc())
        response = session.scalars(statement)
        raw_readings = response.fetchall()

    readings = []
    for i in raw_readings:
        reading = {
            "stromzaehler_id": i.stromzaehler,
            "timestamp": i.timestamp,
            "value": i.value
        }
        readings.append(reading)

    Variables.get_logger().log(request, f'Provided stromzaehler readings in period: {start_date} - {end_date}.')  # todo get jwt

    body = {
        "readings": readings
    }
    return signing_response(body)


@api_routes_blueprint.route('/stromzaehler/register', methods=['POST'])
@token_required('kundenportal')
def register_stromzaehler(stromzaehler):
    data = request.json
    try:
        stromzaehler_id = data['id']
        first_name = data['person']['first_name']
        last_name = data['person']['last_name']
        gender = data['person']['gender'] if 'gender' in data['person'] else 0
        phone = data['person']['phone'] if 'phone' in data['person'] else None
        email = data['person']['email'] if 'email' in data['person'] else None
        street = data['address']['street']
        plz = data['address']['plz']
        city = data['address']['city']
        state = data['address']['state']
        country = data['address']['country']
    except Exception as e:
        print(f"Unprocessable Entity: {e}")
        return '', 422

    # Check if stromzaehler exists
    with Session(Variables.get_database().get_engin()) as session:
        statement = select(Stromzaehler).where(Stromzaehler.id == stromzaehler_id)
        response = session.scalars(statement)
        stromzaehler = response.fetchall()
        if len(stromzaehler) == 0:
            return 'Stromzaehler does not exist.', 404

        # Check if address exists
        statement = select(Address).where(
            (Address.street == street) &
            (Address.plz == plz) &
            (Address.city == city) &
            (Address.state == state) &
            (Address.country == country)
        ).limit(1)
        response = session.scalars(statement)
        add = response.fetchall()
        if len(add) == 0:
            new_add = Address(
                street=street,
                plz=plz,
                city=city,
                state=state,
                country=country
            )
            session.add(new_add)
            session.commit()
            add_id = new_add.id
        else:
            add_id = add[0].id

        # Check if owner exists
        statement = select(Person).where(
            (Person.firstname == first_name) &
            (Person.lastname == last_name) &
            (Person.gender == gender) &
            (Person.email == email)
        ).limit(1)
        response = session.scalars(statement)
        own = response.fetchall()
        if len(own) == 0:
            new_own = Person(
                firstname=first_name,
                lastname=last_name,
                gender=gender,
                phone=phone,
                email=email
            )
            session.add(new_own)
            session.commit()
            own_id = new_own.id
        else:
            own_id = own[0].id

        stromzaehler[0].address = add_id
        stromzaehler[0].owner = own_id
        session.commit()

        body = {
            'success': True,
            'stromzaehler_id': stromzaehler[0].id,
            'owner_id': own_id,
            'address_id': add_id
        }
    return signing_response(body)


@api_routes_blueprint.route('/public_key', methods=['GET'])
def get_public_key():
    return jsonify({
        'public_key': get_public_rsa_key()
    })
