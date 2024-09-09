# app/__init__.py

from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
from flask_cors import CORS
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes and origins
CORS(app)

# CORS(app, resources={r"/parcels/*": {"origins": "http://localhost:3000"}})


# MySQL connection
mysql = MySQL(app)

# SocketIO setup
socketio = SocketIO(app)



from app import routes,auth,user
