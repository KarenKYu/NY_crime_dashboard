from api.src.db import db
import api.src.models as models
class Incident():
    __table__='incidents'
    columns = ['id','incident_num', 'complaint_id', 'incident_date','incident_time', 'location_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_incident_num(self, incident_num, cursor):
        incident_query = """SELECT * FROM incidents WHERE incident_num = %s"""
        cursor.execute(incident_query, (incident_num,))
        record =  cursor.fetchone()
        return db.build_from_record(Incident, record)

    @classmethod
    def find_incidents_by_date(self, date, cursor):
        date_query = """SELECT * FROM incidents WHERE incident_date = %s"""
        cursor.execute(date_query, (date,))
        record = cursor.fetchall()
        return db.build_from_records(Incident, record)

    @classmethod
    def find_incidents_by_complaint_type(self, complaint_type, cursor):
        incident_query = """SELECT * FROM incidents JOIN complaints ON incidents.complaint_id = complaints.id 
        WHERE desc_offense = %s"""
        cursor.execute(incident_query, (complaint_type,))
        record =  cursor.fetchall()
        return db.build_from_records(Incident, record) # returns a list of incident objects which match the complaint type

    @classmethod
    def find_incidents_by_borough(self, borough, cursor):
        query_str = """SELECT * FROM incidents JOIN locations ON incidents.location_id = locations.id WHERE borough = %s"""
        cursor.execute(query_str, (borough,))
        records = cursor.fetchall()
        return db.build_from_records(Incident, records)

    def loc_to_json(self, cursor):
        location_json = self.__dict__
        location = self.location(cursor)
        if location:
            location_json['location'] = location.__dict__
        return location_json

    def complaint_to_json(self, cursor):
        complaint_json = self.__dict__
        complaint = self.complaint_type(cursor)
        if complaint:
            complaint_json['complaint'] = complaint.__dict__
        return complaint_json

