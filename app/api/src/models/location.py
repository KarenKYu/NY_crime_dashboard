class Location:
    __table__='locations'
    columns = ['id','latitude','longitude','borough','precinct','setting']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

# select all columns from incidents table where location_id== a location aka incidents associated with location
    def incidents(self, cursor):
        query_str = "SELECT * FROM incidents WHERE incident_id = %s"
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Location, records)