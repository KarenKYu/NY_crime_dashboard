class Incident():
    __table__='incidents'
    columns = ['id','incident_num','complaint_id', 'incident_date','incident_time','location_id']

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

    def complaints(self,  cursor):
        offense_query = """SELECT complaints.* FROM complaints WHERE incidents.id = %s"""
        cursor.execute(offense_query, (self.id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Complaint, record)

    def find_by_borough(self, cursor):
        borough_query = """SELECT locations.* FROM locations WHERE locations.id 
         = %s"""
        cursor.execute(categories_query, (self.id,))
        venue_records = cursor.fetchall()
        return db.build_from_records(models.Category, venue_records

    
    def to_json(self, cursor):
        venue_json = self.__dict__
        location = self.location(cursor)
        if location:
            location_dict = {'lon': location.longitude, 'lat': location.latitude, 'address': location.address}
            venue_json['location'] = location_dict
        return venue_json

