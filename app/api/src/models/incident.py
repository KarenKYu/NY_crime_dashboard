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
        return db.build_from_record(models.Incident, record)

    @classmethod
    def complaint_type(self,  cursor):
        complaint_query = """SELECT * FROM incidents WHERE complaint_id = %s"""
        cursor.execute(complaint_query, (complaint_id,))
        record = cursor.fetchone()
        return db.build_from_record(Complaint, record)

    def location(self, cursor):
        location_query = """SELECT locations.* FROM locations WHERE incidents.location_id = %s"""
        cursor.execute(location_query, (self.location_id,))
        record = cursor.fetchall()
        return db.build_from_records(models.Location, record)

    def to_json(self, cursor):
        location_json = self.__dict__
        location = self.location_id(cursor)
        if location:
            location_dict = {'lon': location.longitude, 'lat': location.latitude, 'borough': location.borough}
            location_json['location'] = location_dict
        return location_json

