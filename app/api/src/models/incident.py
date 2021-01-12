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

    def complaint_type(self,  cursor):
        complaint_query = """SELECT * FROM complaints WHERE id = %s"""
        cursor.execute(complaint_query, (self.complaint_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Complaint, record)

    def location(self, cursor):
        location_query = """SELECT * FROM locations WHERE id = %s"""
        cursor.execute(location_query, (self.location_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Location, record)

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

