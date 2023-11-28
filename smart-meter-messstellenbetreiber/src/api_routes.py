from flask import jsonify, Blueprint, request
from auth_middleware import token_required


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
def stromzaehler_update():
    return '', 200
