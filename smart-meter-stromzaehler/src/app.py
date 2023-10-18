from flask import Flask, jsonify, request
import os
from dotenv.main import load_dotenv
from auth_middleware import token_required

load_dotenv()

app = Flask(__name__)

# JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
print(JWT_SECRET_KEY)
app.config['SECRET_KEY'] = JWT_SECRET_KEY


@app.route("/api")
def hello_world():
    return "Hello, World!"


@app.route("/protected", methods=["GET"])
@token_required
def get_current_user():
    # request.json
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": "a"
    })

@app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403

@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404


if __name__ == "__main__":
    app.run(debug=True)