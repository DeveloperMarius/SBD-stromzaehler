from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from api_routes import api_routes_blueprint

#load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_routes_blueprint, url_prefix='/api')

# JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
print(JWT_SECRET_KEY)


@app.route("/api")
def hello_world():
    return "Hello, World!"


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
