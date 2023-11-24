from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb+srv://longvo210404:ILovePython2003@clusterlol.niegrk3.mongodb.net/'
    mongo.init_app(app)

    return app