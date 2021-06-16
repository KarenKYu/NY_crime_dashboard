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

@st.cache 
def find_lat_long_by_borough(lat_lon_df, option):
    df = lat_lon_df[lat_lon_df['boro']== option]
    return df
    

st.header("**NYC** Police Department incidents")

st.map(get_lat_lon(API_URL))
'''User selects a boroough and display incidents'''

option = st.selectbox(
        'Select a borough:',
        ('','BRONX','BROOKLYN','MANHATTAN','STATEN ISLAND','QUEENS'))

st.map(find_lat_long_by_borough(lat_lon_df, option))

sites_df= pd.read_csv('tourist_lat_long.csv').drop(columns="Unnamed: 3")

letter,site,start,end = st.beta_columns(4)

first_letter = str(letter.text_input("Enter first letter of site.")).lower()

site_names = sites_df[[site[0] == first_letter for site in sites_df.loc_name]].loc_name.values
#returns numpy.ndarray

site_choice = site.selectbox("Pick a site", (site_names))
# site_choice = 'brooklyn_bridge'
#returns numpy.str_

start_date = start.date_input("Select a start date")
end_date = end.date_input("Select an end date")

st.map(sites_df[sites_df.loc_name==site_choice])
