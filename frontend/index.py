import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import requests
API_URL = "http://127.0.0.1:5000/incidents"

def get_lat_lon(API_URL):
    session = requests.Session()
    incidents = session.get(API_URL).json()
    latitude  = [incident.get('latitude','NONE') for incident in incidents]
    longitude = [incident.get('longitude','NONE') for incident in incidents]
    borough = [incident.get('borough','NONE') for incident in incidents]
    scoped_data = zip(latitude,longitude,borough)
    df = pd.DataFrame(data = scoped_data, columns = ['lat','lon', 'boro'])
    return df

#def find_lat_long_by_borough(borough,cursor):


st.header("**NYC** Police Department incidents")

option = st.selectbox(
        'Select a borough:',
        ('BRONX','BROOKLYN','MANHATTAN','STATEN ISLAND','QUEENS'))

st.map(get_lat_lon(API_URL))



