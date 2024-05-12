# ---------- Importing libraries ----------
 
# Data manipulation libraries
import pandas       as pd

# Geolocation libraries
import geopandas    as gpd

# Other libraries
import warnings

# ---------- Settings ----------

# Ignoring warnings
warnings.filterwarnings('ignore')

# ---------- Extracting data ----------

# Geojson file
gdf = gpd.read_file('../../data/interim/municipios_rs.geojson')

# Delegados information
df = pd.read_excel('../../data/raw/crcrs_delegados.xlsx')

# ---------- Transforming data ----------

# Split municipios column into a list
df['municipios'] = df['municipios'].str.split(',')
# Explode 'municipios' column to separate rows for each municipality
df_exploded = df.explode('municipios')
# Remove leading and trailing spaces from 'municipios' column
df_exploded['nm_mun'] = df_exploded['municipios'].str.strip()

# Merging gdf and df_exploded into new geodataframe
gdf_delegados = gdf.merge(df_exploded[['nm_mun', 'jurisdicao', 'nm_delegado']], 
                                        on='nm_mun', how='left')

# Reordering columns
gdf_delegados = gdf_delegados[['id_mun', 'nm_mun', 'nm_delegado', 'jurisdicao', 'geometry']]

# ---------- Loading data ----------
gdf_delegados.to_file('../../data/processed/crcrs_delegados.geojson', driver='GeoJSON')
