# ---------- Importing libraries ----------
 
# Data manipulation libraries
import pandas       as pd
import numpy        as np

# Geolocation libraries
import geopandas    as gpd

# Other libraries
import requests     as req
import sys
import warnings
import inflection

# ---------- Settings ----------

# Ignoring warnings
warnings.filterwarnings('ignore')

# ---------- Functions ----------
def columns_to_snake_case(dataframe):
    """
    Summary:    This function transforms the column names to snake_case style.
    Args:       Dataframe with incorrect column names.
    Returns:    None.
    """
    
    # List of columns
    old_columns = dataframe.columns.tolist()
    # Lambda function
    snake_case = lambda x: inflection.underscore(x)
    # Assigning new column names to DataFrame
    dataframe.columns = list(map(snake_case, old_columns))

    return None

# ---------- Extracting data ----------

# Path to the shapefile
shapefile_path = '../../RS_Municipios_2022/RS_Municipios_2022.shp'

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# ---------- Transforming data ----------

# Transforming column names
columns_to_snake_case(gdf)
# Transforming ID column
gdf['id_mun'] = gdf['cd_mun'].apply(lambda x: int(str(x)[:-1]))
# Selecting only necessary columns
gdf = gdf[['id_mun', 'nm_mun', 'geometry']]
# Dropping unnecessary rows (Lagoa dos Patos, Lagoa Mirim)
gdf = gdf[gdf['id_mun'] != 430000]

# ---------- Loading data ----------
gdf.to_file('../../data/interim/municipios_rs.geojson', driver='GeoJSON')