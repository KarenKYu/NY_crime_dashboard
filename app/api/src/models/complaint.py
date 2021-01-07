class Complaint():
    __table__='complaints'
    columns = ['id','desc_offense', 'level_offense', 'dept_juris']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

# select all columns from incidents table where complaint_id== a type of complaint aka incidents by type of complaint
    def incidents(self, cursor):
        query_str = "SELECT * FROM incidents WHERE incident_id = %s"
        cursor.execute(query_str, (self.incident_id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Complaint, records)

