from flask import Flask
import simplejson as json
from flask import request

import api.src.models as models
import api.src.db as db

def create_app(database='nypd_complaints', testing = False, debug = True):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=database,
        DEBUG = debug,
        TESTING = testing
    )

    @app.route('/')
    def root_url():
        return 'Welcome to the NYPD Complaints api'

    @app.route('/incidents')
    def incidents():
        conn = db.get_db()
        cursor = conn.cursor()

        incidents = db.find_all(models.Incident, cursor)
        incident_dicts = [incident.__dict__ for incident in incidents]
        return json.dumps(incident_dicts, default = str)

    @app.route('/incidents/search')
    def search_incidents():
        conn = db.get_db()
        cursor = conn.cursor()

        params = dict(request.args)
        incidents = models.Incident.search(params, cursor)
        incident_dicts = [incident.to_json(cursor) for incident in incidents]
        return json.dumps(incident_dicts, default = str)

    @app.route('/incidents/<id>')
    def incident(id):
        conn = db.get_db()
        cursor = conn.cursor()
        venue = db.find(models.Incident, id, cursor)

        return json.dumps(incident.__dict__, default = str)


    return app