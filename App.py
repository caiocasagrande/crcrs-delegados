# ---------- Importing libraries ----------
 
# Data manipulation libraries
import pandas           as pd
import numpy            as np

# Data visualization libraries
import plotly.express   as px
import matplotlib       as mpl

# Geolocation libraries
import geopandas        as gpd

# Other
import streamlit        as st
import warnings

# ---------- Settings ----------

# Ignoring warnings
warnings.filterwarnings('ignore')

# Matplotlib settings
mpl.rcParams['figure.titlesize']    = 24
mpl.rcParams['figure.figsize']      = (20, 5)

# ---------- Extracting data ----------

# Geojson file
gdf = gpd.GeoDataFrame.from_file('data/processed/crcrs_delegados.geojson')

# ---------- Main ----------

# Selecting columns
gdf = gdf[['nm_mun', 'jurisdicao', 'nm_delegado', 'geometry']]

# Add number of reference
gdf['id_jurisdicao'] = pd.factorize(gdf['jurisdicao'])[0] + 1

# Set index
gdf.set_index('nm_mun', inplace=True)

# ---------- Streamlit App Code ----------

# Set the background color of the Streamlit app
st.set_page_config(layout="wide", page_title="Mapa CRCRS", page_icon="📈", 
                   initial_sidebar_state="collapsed")

st.sidebar.markdown('# Delegacias e delegados | CRCRS')
st.sidebar.markdown("[www.crcrs.org.br](https://www.crcrs.org.br/)")
st.sidebar.markdown("""---""")

st.header('Conselho Regional de Contabilidade do RS')

st.subheader('Mapa de delegados por delegacia e municípios')

fig = px.choropleth_mapbox(gdf, 
                        geojson=gdf.geometry, 
                        locations=gdf.index,
                        color='id_jurisdicao', 
                        color_continuous_scale='Portland',
                        hover_name=gdf.index, 
                        hover_data=['jurisdicao', 'nm_delegado'],
                        mapbox_style='carto-positron', 
                        center = {'lat': -31, 'lon': -53.5},
                        zoom=5,
                        labels={'nm_mun': 'Município', 
                                'jurisdicao': 'Delegacia', 
                                'nm_delegado': 'Delegado', 
                                'id_jurisdicao': 'ID'}
)

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig, use_container_width=True)
