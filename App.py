# ---------- Importing libraries ----------
 
# Data manipulation libraries
import pandas           as pd
import numpy            as np

# Data visualization libraries
import plotly.express   as px

# Geolocation libraries
import geopandas        as gpd

# Other
import streamlit        as st
import warnings

# ---------- Settings ----------

# Ignoring warnings
warnings.filterwarnings('ignore')

# ---------- Extracting data ----------

# Geojson file
gdf = gpd.GeoDataFrame.from_file('data/processed/crcrs_delegados.geojson')

# ---------- Main ----------

# Transforming dataset
gdf = gdf[['nm_mun', 'jurisdicao', 'nm_delegado', 'geometry']]

gdf = gdf.set_index('nm_mun')

# ---------- Streamlit App Code ----------

# Set the background color of the Streamlit app
st.set_page_config(layout="wide", page_title="CRCRS", page_icon="💻", 
                   initial_sidebar_state="collapsed")

st.sidebar.markdown('# CRCRS')
st.sidebar.markdown("""---""")

st.header('CRCRS')

st.subheader('Delegados CRCRS')

fig = px.choropleth_mapbox(gdf, 
                        geojson=gdf.geometry, 
                        locations=gdf.index,
                        color='jurisdicao', 
                        hover_name='nm_delegado', 
                        hover_data=['nm_delegado'],
                        mapbox_style='carto-positron', 
                        center = {'lat': -30.033333, 'lon': -51.15},
                        zoom=5.5, 
                        title='CRCRS Delegados - RS'
)

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig)
