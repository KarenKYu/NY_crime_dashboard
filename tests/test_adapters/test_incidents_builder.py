import psycopg2
import pytest
import api.src.db.db as db
import api.src.models as models
import api.src.adapters as adapters

def test_incident_builder():
    class IncidentBuilder:
    attributes = ['incident_num', 'complaint_id', 'incident_date','incident_time', 'location_id']

    def select_attributes(self, incident_details):
        complaint_id = complaint.id
        incident_num = incident_details['cmplnt_num']
        incident_date = incident_details['cmplnt_fr_dt']
        incident_time = incident_details['cmplnt_fr_tm']
        location_id = location.id
        return dict(zip(self.attributes, [incident_num,complaint_id,incident_date,incident_time,location_id]))

    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        incident_num = selected['incident_num']
        incident = models.Incident.find_by_incident_num(incident_num, cursor)
        if incident:
            incident.exists = True
            return incident
        else:
            incident = db.save(models.Incident(**selected), conn, cursor)
            incident.exists = False
            return incident