import os
from flask_pymongo import PyMongo
from flask import Flask, render_template
import json
from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self,o)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.json_encoder = JSONEncoder

    with app.app_context():
        from . import db
        mongo = db.get_db()
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import plan
    app.register_blueprint(plan.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/hello')
    def hello():
        return render_template("hello.html")
        '''
        online_users = mongo.db.users.find({"online":True})
        for x in online_users: print(x)
        if online_users is None:
            mongo.db.users.insert_one({"name":"Ryan","online":True})
        return render_template("index.html", online_users=online_users)
        '''
    return app

