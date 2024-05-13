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

# Pandas settings
pd.set_option('display.width', None)

# ---------- Extracting data ----------

# Geojson file
gdf = gpd.GeoDataFrame.from_file('data/processed/crcrs_delegados.geojson')

# ---------- Main ----------

# DataFrame
df = pd.DataFrame(gdf[['nm_mun', 'jurisdicao', 'nm_delegado']])

# GeoDataFrame
# Selecting columns
gdf = gdf[['nm_mun', 'jurisdicao', 'nm_delegado', 'geometry']]
# Add number of reference
gdf['id_jurisdicao'] = pd.factorize(gdf['jurisdicao'])[0] + 1
# Set index
gdf.set_index('nm_mun', inplace=True)

# ---------- Streamlit App Code ----------

st.set_page_config(
                page_title="CRCRS | Delegacias", 
                page_icon="images/crcrs_logo_miniatura.png", 
                layout="centered", 
                initial_sidebar_state="expanded"
)

# Sidebar
sidebar_container = st.sidebar.container()

with sidebar_container:
    st.image('images/crcrs_logo.png')
    
    st.sidebar.write(
        """
        Este aplicativo permite que você pesquise por **delegados** e **delegacias** do **Conselho Regional de Contabilidade do Rio Grande do Sul** e seus municípios de atividade.

        O aplicativo é composto por duas seções: **Pesquisa** e **Mapa RS**. 
        
        Selecionando a seção **Pesquisa**, você pode pesquisar por município, delegacia ou delegado e isso retornará as informações correspondentes.  
        
        Ao selecionar a seção **Mapa RS**, será exibido o mapa do estado do Rio Grande do Sul colorido conforme as 103 delegacias registradas. 
        
        No mapa, ao passar o cursor do *mouse* sobre cada município, serão exibidas as informações de cada um.
        
        """
    )
    st.markdown("---")
    st.sidebar.markdown("Mais informações em [CRCRS](https://www.crcrs.org.br/).", unsafe_allow_html=True)
    st.sidebar.write("<font color='gray'>Desenvolvido por [Caio Casagrande](https://www.linkedin.com/in/caiopc/).</font>", unsafe_allow_html=True)

# Main
st.header('Delegados e Delegacias do CRCRS')

tab1, tab2 = st.tabs(['Pesquisa', 'Mapa RS'])

with tab1:
        # ---------- Pesquisa por município ----------
        st.markdown('### Pesquisa por município')
        selected_municipality = st.selectbox('**Selecionar:**', df['nm_mun'])

        # Filter the DataFrame 
        filtered_by_municipality = df[df['nm_mun'] == selected_municipality]

        # Return 
        if not filtered_by_municipality.empty:
                # Filters
                delegacy    = filtered_by_municipality['jurisdicao'].iloc[0]
                delegate    = filtered_by_municipality['nm_delegado'].iloc[0]

                # Display
                st.write(f"Delegacia: {delegacy}.")
                st.write(f"Delegado:  {delegate}.")
        else:
                st.write("Não consta.")

        st.write("---")

        # ---------- Pesquisa por Delegacia ----------
        st.markdown('### Pesquisa por delegacia')
        selected_delegacy = st.selectbox('**Selecionar:**', df['jurisdicao'].unique())

        # Filter the DataFrame 
        filtered_by_delegacy = df[df['jurisdicao'] == selected_delegacy]

        # Return
        if not filtered_by_delegacy.empty:
                # Filters
                municipalities     = filtered_by_delegacy['nm_mun'].to_list()
                municipalities_str = ", ".join(municipalities)

                delegate = filtered_by_delegacy['nm_delegado'].iloc[0]

                # Display
                st.write(f"Municípios: {municipalities_str}.")
                st.write(f"Delegado:   {delegate}.")
        else:
                st.write("Não consta.")

        st.write("---")

        # ---------- Pesquisa por Delegado ----------
        st.markdown('### Pesquisa por delegado')
        selected_responsible = st.selectbox('**Selecionar:**', df['nm_delegado'].unique())

        # Filter the DataFrame 
        filtered_by_delegate = df[df['nm_delegado'] == selected_responsible]

        # Return
        if not filtered_by_delegate.empty:
                # Filters
                municipalities     = filtered_by_delegate['nm_mun'].to_list()
                municipalities_str = ", ".join(municipalities)

                delegacy = filtered_by_delegate['jurisdicao'].iloc[0]

                # Display
                st.write(f"Municípios: {municipalities_str}.")
                st.write(f"Delegacia:  {delegacy}.")
        else:
                st.write("Não consta.")

        st.markdown("---")

with tab2:
        # Map
        st.markdown('### Mapa de delegados por delegacia e município')

        # Create the map
        fig = px.choropleth_mapbox(gdf, 
                                geojson=gdf.geometry, 
                                locations=gdf.index,
                                color='id_jurisdicao', 
                                color_continuous_scale='Portland',
                                hover_name='jurisdicao', 
                                hover_data=['jurisdicao', 'nm_delegado'],
                                mapbox_style='carto-positron', 
                                center = {'lat': -31, 'lon': -53.5},
                                zoom=5,
                                labels={'nm_mun': 'Município', 
                                        'jurisdicao': 'Delegacia', 
                                        'nm_delegado': 'Delegado', 
                                        'id_jurisdicao': 'ID'}
        )

        # Map layout
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Display the map
        st.plotly_chart(fig, use_container_width=True)
