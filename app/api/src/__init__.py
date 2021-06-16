from flask import Flask
import simplejson as json
from flask import request

import app.api.src.models as models
import app.api.src.db as db

def create_app(database='nypd_complaints', testing = False, debug = True):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=database,
        DEBUG = debug,
        TESTING = testing)

    @app.route('/')
    def root_url():
        return 'Welcome to the NYPD Complaints api'

    @app.route('/incidents')
    def incidents():
        conn = db.get_db()
        cursor = conn.cursor()
        incidents = db.find_all(models.Incident, cursor)
        incident_dicts = [incident.to_json(cursor) for incident in incidents]
        return json.dumps(incident_dicts, default = str)

    @app.route('/incidents/search')
    def search_incidents():
        conn = db.get_db()
        cursor = conn.cursor()

        params = dict(request.args) # from frontend/index.py streamlit requests.get(API_URL + "complaint":complaint)
        incidents = models.Incident.find_by_complaint_type(params, cursor)
        incident_dicts = [incident.to_json(cursor) for incident in incidents]
        return json.dumps(incident_dicts, default = str)

    @app.route('/incidents/<incident_num>')
    def incident(incident_num):
        conn = db.get_db()
        cursor = conn.cursor()
        incident = db.find_incident(models.Incident, incident_num, cursor)

        return json.dumps(incident.__dict__, default = str)


    return app

    