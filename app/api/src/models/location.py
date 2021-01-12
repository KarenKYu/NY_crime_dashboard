class Location:
    __table__='locations'
    columns = ['id','borough','latitude','longitude','setting','precinct']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

# select all columns from incidents table where location_id== a location aka incidents associated with location
    @classmethod
    def incidents(self, cursor):
        query_str = "SELECT * FROM incidents WHERE location_id = %s"
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Location, records)

    @classmethod
    def boroughs(self, cursor):
        query_str = "SELECT * FROM incidents WHERE location_id = %s"
        cursor.execute(query_str, (self.borough,))
        records = cursor.fetchall()
        return db.build_from_records(models.Location, records)

        (5, 'MANHATTAN', Decimal('40.75469651000003'), Decimal('-73.99535613299997'), 'STREET', 14)