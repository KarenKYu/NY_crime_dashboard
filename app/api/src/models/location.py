from app.api.src.db import db
import app.api.src.models as models
class Location:
    __table__='locations'
    columns = ['id','borough','latitude','longitude','setting','precinct']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_id(self, id, cursor): 
        location_query = """SELECT * FROM locations WHERE id = %s"""
        cursor.execute(location_query, (id,))
        record =  cursor.fetchone()
        return db.build_from_record(Location, record)
# >>> location = Location.find_by_id('5',cursor)
# >>> location.__dict__
# {'id': 5, 'borough': 'MANHATTAN', 'latitude': Decimal('40.75469651000003'), 'longitude': Decimal('-73.99535613299997'), 'setting': 'STREET', 'precinct': 14}

    @classmethod
    def find_by_lat_long(self, latitude, longitude, cursor):
        query_str = "SELECT * FROM locations WHERE (latitude, longitude) = (%s,%s)"
        cursor.execute(query_str, (latitude,longitude))
        records = cursor.fetchall()
        return db.build_from_records(Location, records)
# >>> location = Location.find_by_lat_long('40.82413968200007','-73.94097291399999',cursor)
# >>> len(location)
# 1
# >>> location[0].__dict__
# {'id': 2, 'borough': 'MANHATTAN', 'latitude': Decimal('40.82413968200007'), 'longitude': Decimal('-73.94097291399999'), 'setting': 'STREET', 'precinct': 32} 
    # @classmethod
    # def find_lat_long_by_ borough(self, borough, cursor):
    #     query_str = “SELECT latitude,longitude FROM locations WHERE borough = '%s';”
    #     cursor.execute(query_str, (borough,))
    #     records = cursor.fetchall()
    #     pd.DataFrame(data = records, columns =, [‘lat’,’lon’])
    