class Incident():
    __table__='incidents'
    columns = ['id','incident_num','complaint_id', 'incident_date','incident_time','location_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)


