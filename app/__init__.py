from flask import Flask
from flask_cors import CORS

from app.database import init_db

app = Flask(__name__)
CORS(app)
init_db()

from app import routes
