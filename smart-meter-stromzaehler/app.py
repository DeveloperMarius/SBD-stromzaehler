from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
print(JWT_SECRET_KEY)
app.config['SECRET_KEY'] = JWT_SECRET_KEY

@app.route("/api")
def hello_world():
    return "Hello, World!"