import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import requests
API_URL = "http://127.0.0.1:5000/incidents"

@st.cache
def get_lat_lon(API_URL):
    session = requests.Session()
    incidents = session.get(API_URL).json()
    latitude  = [incident.get('latitude','NONE') for incident in incidents]
    longitude = [incident.get('longitude','NONE') for incident in incidents]
    borough = [incident.get('borough','NONE') for incident in incidents]
    scoped_data = zip(latitude,longitude,borough)
    df = pd.DataFrame(data = scoped_data, columns = ['lat','lon', 'boro'])
    return df

lat_lon_df = get_lat_lon(API_URL)
#def find_lat_long_by_date(API_URL):

# def find_lat_long_by_borough(API_URL, option):
#     lat_lon_df = get_lat_lon(API_URL)
#     boro_df = lat_lon_df[lat_lon_df['boro']== option]
#     return boro_df

# below is 3x faster than above function per timeit. adding st.cache reduces return time to 1 second instead of about 6 seconds
@st.cache 
def find_lat_long_by_borough(lat_lon_df, option):
    df = lat_lon_df[lat_lon_df['boro']== option]
    return df
    

st.header("**NYC** Police Department incidents")

st.map(get_lat_lon(API_URL))

option = st.selectbox(
        'Select a borough:',
        ('','BRONX','BROOKLYN','MANHATTAN','STATEN ISLAND','QUEENS'))

st.map(find_lat_long_by_borough(lat_lon_df, option))

date = st.text_input("Find incidents by date. Enter date as YYYY-DD-MM")





