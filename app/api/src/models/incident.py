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
        return db.build_from_record(Incident, record) # returns one Incident object
# >>> incident4=Incident.find_by_incident_num('949043828',cursor)
# >>> incident4.__dict__
# {'id': 4, 'incident_num': 949043828, 'complaint_id': 4, 'incident_date': datetime.date(2020, 7, 26), 'incident_time': datetime.time(1, 8), 'location_id': 4}

    @classmethod
    def find_by_date(self, date, cursor):
        date_query = """SELECT * FROM incidents WHERE incident_date = %s"""
        cursor.execute(date_query, (date,))
        record = cursor.fetchall()
        return db.build_from_records(Incident, record) # returns a list of Incident objects
# returns list of objects:
# >>> incident1 = Incident.find_incidents_by_date('2020-06-24', cursor)
# >>> incident1[0]
# <api.src.models.incident.Incident object at 0x000001DBA29438E0>
# >>> incident1[0].__dict__
# {'id': 2, 'incident_num': 664557183, 'complaint_id': 2, 'incident_date': datetime.date(2020, 6, 24), 'incident_time': datetime.time(21, 20), 'location_id': 2}

    @classmethod
    def find_incident_by_complaint(self, complaint, cursor):
        incident_query = """SELECT * FROM incidents JOIN complaints ON incidents.complaint_id = complaints.id 
        WHERE desc_offense = %s"""
        cursor.execute(incident_query, (complaint,))
        record =  cursor.fetchall()
        return db.build_from_records(Incident, record) # returns a list of incident objects which match the complaint type
# >>> incident2 = Incident.find_incidents_by_complaint_type('ROBBERY',cursor)
# >>> incident2[0].__dict__
# {'id': 3, 'incident_num': 453437883, 'complaint_id': 3, 'incident_date': datetime.date(2020, 9, 28), 'i
# ncident_time': datetime.time(20, 0), 'location_id': 3}

    @classmethod
    def find_by_borough(self, borough, cursor):
        query_str = """SELECT * FROM incidents JOIN locations ON incidents.location_id = locations.id WHERE borough = %s"""
        cursor.execute(query_str, (borough,))
        records = cursor.fetchall()
        return db.build_from_records(Incident, records)
# >>> incident3 = Incident.find_incidents_by_borough('BRONX',cursor)
# >>> incident3[0].__dict__
# {'id': 3, 'incident_num': 453437883, 'complaint_id': 3, 'incident_date': datetime.date(2020, 9, 28), 'incident_time': datetime.time(20, 0), 'location_id': 3}
    
    def location(self, cursor):
        location_query = """SELECT * FROM locations JOIN incidents ON incidents.location_id = locations.id WHERE incident_num = %s"""
        cursor.execute(location_query, (self.incident_num,))
        record =  cursor.fetchone()
        return db.build_from_record(models.Location, record)
# >>> incid = Incident.return_location('453437883',cursor)
# >>> incid.__dict__
# {'id': 3, 'borough': 'BRONX', 'latitude': Decimal('40.88144124600007'), 'longitude': Decimal('-73.83235353999999'), 'setting': 'OTHER', 'precinct': 47}

    def to_json(self,cursor):
        incident_attr = self.__dict__
        location = self.location(cursor)
        if location:
            incident_attr.update(location.__dict__)
        return incident_attr
# >>> incident = Incident().loc_to_json('453437883',cursor) 
# >>> incident
# {'location': {'id': 3, 'borough': 'BRONX', 'latitude': Decimal('40.88144124600007'), 'longitude': Decimal('-73.83235353999999'), 'setting': 'OTHER', 'precinct': 47}}

    def complaint(self, cursor):
        incident_attr = self.__dict__
        complaints = self.find_incident_by_complaint(complaint_type, cursor)
        if len(complaints)>0:
            incident_attr['complaint'] = [complaint.__dict__ for complaint in complaints]
        return incident_attr
# >>> incid = Incident().complaint_to_json('ROBBERY',cursor)            
# >>> incid 
# {'complaint': [{'id': 3, 'incident_num': 453437883, 'complaint_id': 3, 'incident_date': datetime.date(2020, 9, 28), 'incident_time': datetime.time(20, 0), 'location_id': 3}]}
