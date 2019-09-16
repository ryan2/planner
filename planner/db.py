from flask_pymongo import PyMongo

from flask import current_app, g

def get_db():
    if 'mongo' not in g:
        current_app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
        g.mongo = PyMongo(current_app)
    return g.mongo

@current_app.teardown_appcontext
def teardown_db(e=None):
    mongo = g.pop('mongo',None)
    if mongo is not None:
        mongo.cx.close()
