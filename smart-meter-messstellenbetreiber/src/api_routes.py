from flask import jsonify, Blueprint
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