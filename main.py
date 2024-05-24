import pydeck as pdk
import streamlit as st
import pandas as pd
import altair as alt
import streamlit_echarts as echarts
from streamlit_echarts import st_echarts
# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord de la Migration en Tunisie",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Fonction pour charger les données de la migration
@st.cache
def load_migration_data():
    # Le chemin vers le fichier Excel doit être accessible par votre application Streamlit
    data = pd.read_excel("migrafr.xlsx", thousands=',')
    # Assurez-vous que les noms des colonnes sont corrects après le chargement
    data.columns = [str(column).strip() for column in data.columns]
    return data

# Chargement des données
migration_data = load_migration_data()

# Titre principal
st.title("Illegal Migration Dashboard in France")

# Sélection de l'année dans la page principale
selected_year = st.selectbox("Choose a year:", [year for year in range(2010, 2024)], index=13)

if str(selected_year) in migration_data.columns:
    chart_data = migration_data[['Region', str(selected_year)]]
    chart_data = chart_data.rename(columns={str(selected_year): 'Migration'})
    chart_data = chart_data.sort_values('Migration', ascending=False)

    hover = alt.selection_single(on='mouseover', fields=['Region'], empty='none')

    # Création du graphique à barres avec interaction de survol
    bars = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Region:N', title='Region', sort='-y'),
        y=alt.Y('Migration:Q', title='Migration'),
        color=alt.condition(hover, alt.value('red'), alt.value('steelblue')),
        tooltip=['Region:N', 'Migration:Q']
    ).properties(width='container', height=400)

    # Texte sur les barres, soulevé pour éviter la superposition
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-10  # Nudge text up for better visibility
    ).encode(
        text=alt.Text('Migration:Q', format=',')
    )

    # Combine les barres et le texte avec interaction de survol
    chart = (bars + text).add_selection(hover)

    st.altair_chart(chart, use_container_width=True)
else:
    st.error(f"Data for the year {selected_year} is not available.")

with st.sidebar.expander("See raw data"):
    st.write(migration_data[['Region', str(selected_year)]])

# Le reste du CSS personnalisé reste le même


# Function to load migrant gender data from an Excel file
@st.cache(allow_output_mutation=True)
def load_gender_data(path):
    try:
        data = pd.read_excel(path)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load migrant gender data from the provided path for France
gender_data_path_fr = "GENREfr.xlsx"
gender_data_fr = load_gender_data(gender_data_path_fr)

def render_pie_chart_fr():
    # Main page for year and month selection
    selected_year_fr = st.selectbox("Choose a year", options=gender_data_fr["Année"].unique())
    selected_month_fr = st.selectbox("Choose a month", options=gender_data_fr["Mois"].unique())

    # Filter data based on selections
    filtered_data_fr = gender_data_fr[(gender_data_fr["Année"] == selected_year_fr) & (gender_data_fr["Mois"] == selected_month_fr)]

    if filtered_data_fr.empty:
        st.error("No data found for the selected year and month.")
    else:
        # Prepare data for the pie chart
        pie_values_fr = filtered_data_fr[['Enfants', 'Femmes', 'Hommes']].sum()
        pie_data_fr = [
            {"value": int(pie_values_fr['Enfants']), "name": "Enfants", "itemStyle": {"color": "white"}},
            {"value": int(pie_values_fr['Femmes']), "name": "Femmes", "itemStyle": {"color": "red"}},
            {"value": int(pie_values_fr['Hommes']), "name": "Hommes", "itemStyle": {"color": "blue"}}
        ]

        # Options for pie chart
        options_fr = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "5%", "left": "center"},
            "series": [
                {
                    "name": "Access From",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "center": ["50%", "70%"],
                    "startAngle": 180,
                    "endAngle": 360,
                    "data": pie_data_fr
                }
            ]
        }

        # Convert selected_year_fr and selected_month_fr to strings for key
        key_fr = f"{selected_year_fr}-{selected_month_fr}"

        # Render the pie chart with a dynamic key to refresh on data update
        echarts.st_echarts(options=options_fr, height="600px", key=key_fr)

# Call the function to render the pie chart for France
render_pie_chart_fr()




# Function to load the new France data
@st.cache
def load_new_france_data():
    new_data_path = "BATOU2fr.xlsx"
    data = pd.read_excel(new_data_path)
    return data


# Load the new France data
new_france_data = load_new_france_data()

# Title of the dashboard
st.title('Dashboard de Surveillance Spatiotemporelle pour la Migration en France')

# Multiselect for year filter for the new France data
selected_year_france = st.selectbox(
    'Sélectionnez l\'année pour la France',
    options=new_france_data['Année'].unique(),
    index=len(new_france_data['Année'].unique()) - 1
)

# Filter new France data by the selected year
filtered_new_france_data = new_france_data[new_france_data['Année'] == selected_year_france]

# Pie Chart
if not filtered_new_france_data.empty:
    pie_data = [
        {"value": int(filtered_new_france_data['Train'].sum()), "name": 'Train'},
        {"value": int(filtered_new_france_data['Bus'].sum()), "name": 'Bus'},
        {"value": int(filtered_new_france_data['Voitures'].sum()), "name": 'Voitures'},
        {"value": int(filtered_new_france_data['Camions'].sum()), "name": 'Camions'}
    ]

    options = {
        "tooltip": {"trigger": 'item'},
        "legend": {
            "top": '5%',
            "left": 'center'
        },
        "series": [
            {
                "name": 'Modes de Transport',
                "type": 'pie',
                "radius": ['40%', '70%'],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": '#fff',
                    "borderWidth": 2
                },
                "label": {
                    "show": False,
                    "position": 'center'
                },
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": '40',
                        "fontWeight": 'bold'
                    }
                },
                "labelLine": {
                    "show": False
                },
                "data": pie_data
            }
        ]
    }

    st_echarts(options=options, height="600px")
else:
    st.write("Aucune donnée à afficher pour l'année sélectionnée.")


# Load your dataset
@st.cache(allow_output_mutation=True)
def load_data():
    # Excel file path for French data
    return pd.read_excel("voyagefr.xlsx")

# Function to create the gauge chart data
def create_gauge_data(number_of_voyages):
    # Convert to int for JSON serialization
    return [{"value": int(number_of_voyages), "name": "Nombre de voyages"}]

# Initialize your Streamlit app and load the data
st.title("Analyse de la Migration Illégale en France")
df = load_data()

# Main page for user input instead of the sidebar
selected_year = st.selectbox("Sélectionnez l'année", df['Année'].unique())
selected_month = st.selectbox("Sélectionnez le mois", df['Mois'].unique())

# Filter the data based on user selections
monthly_data = df[(df['Année'] == selected_year) & (df['Mois'] == selected_month)]
if not monthly_data.empty:
    voyages_made = monthly_data['Voyages'].iloc[0]
else:
    voyages_made = 0
    st.error("Aucune donnée disponible pour le mois et l'année sélectionnés")

# Create the gauge data
gauge_data = create_gauge_data(voyages_made)

# ECharts gauge options with the color changed to green
options = {
    "series": [
        {
            "type": 'gauge',
            "startAngle": 90,
            "endAngle": -270,
            "pointer": {
                "show": True,
                "length": '80%',
                "width": 8,
                "itemStyle": {
                    "color": "blue"
                }
            },
            "progress": {
                "show": True,
                "overlap": False,
                "roundCap": True,
                "color": "blue"
            },
            "axisLine": {
                "lineStyle": {
                    "width": 30,
                    "color": [[1, 'red']]
                }
            },
            "axisTick": {
                "show": False
            },
            "splitLine": {
                "show": False,
                "length": 30,
            },
            "axisLabel": {
                "distance": 15,
                "color": "red",
                "fontSize": 15
            },
            "anchor": {
                "show": True,
                "showAbove": True,
                "size": 25,
                "itemStyle": {
                    "borderWidth": 10
                }
            },
            "title": {
                "show": False
            },
            "detail": {
                "valueAnimation": True,
                "formatter": '{value}',
                "color": 'auto',
                "fontSize": 40,
                "offsetCenter": [0, '70%']
            },
            "data": gauge_data,
            "max": 300  # Adjust the max value if needed based on the data range
        }
    ],
    "tooltip": {
        "formatter": '{a} <br/>{b} : {c}'
    }
}

# Render the gauge in Streamlit
st_echarts(options=options, height="400px", key="gauge_chart")

# Sidebar for displaying the raw data table
with st.sidebar:
    if st.checkbox("Afficher les données brutes"):
        st.write(df)



# Load your dataset
@st.cache(allow_output_mutation=True)
def load_data():
    # Replace with the actual path to your Excel file
    return pd.read_excel(r"jjobfr.xlsx")

df = load_data()
# Title for the data analysis
st.title("Le Niveau Académique des Migrants")


# User selections for multiple years and months
selected_years = st.multiselect("Select Years", options=sorted(df['Année'].unique()), default=sorted(df['Année'].unique()))
selected_months = st.multiselect("Select Months", options=sorted(df['Mois'].unique()), default=sorted(df['Mois'].unique()))

# Filter dataset based on selections
df_filtered = df[df['Année'].isin(selected_years) & df['Mois'].isin(selected_months)]

# Check if any data is available after filtering
if not df_filtered.empty:
    # Preparing data for stacked area chart
    area_data = [
        {
            "name": category,
            "type": "line",
            "stack": "Total",
            "areaStyle": {},
            "data": df_filtered.groupby(["Année", "Mois"])[category].sum().tolist()
        }
        for category in ["Élèves", "Étudiants", "Chômeurs", "Travailleurs"]
    ]

    # ECharts options for the stacked area chart
    options = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'cross',
                "label": {
                    "backgroundColor": '#6a7985'
                }
            }
        },
        "legend": {
            "data": ["Élèves", "Étudiants", "Chômeurs", "Travailleurs"]
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": df_filtered.groupby(["Année", "Mois"]).size().index.tolist()
        },
        "yAxis": {
            "type": 'value'
        },
        "series": area_data
    }

    # Render the chart in the Streamlit app
    st_echarts(options=options, height="400px")
else:
    st.error("No data available for the selected time period.")

# Sidebar for displaying the raw data table
with st.sidebar:
    if st.checkbox("Show Raw Data"):
        st.write(df_filtered)



# Charger le jeu de données pour la France
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_excel(path)
    # Convertir les pourcentages en flottants, en s'assurant de traiter uniquement les chaînes
    for col in data.columns[2:]:
        data[col] = data[col].apply(lambda x: str(x).rstrip('%')).astype('float') / 100
    return data

# Emplacement du fichier de données pour la France
DATA_FILE_FRANCE = "sahelfr.xlsx"
df_france = load_data(DATA_FILE_FRANCE)

# Dictionnaire avec les coordonnées pour chaque région française
coordinates_france = {
    'Île-de-France': [48.8566, 2.3522],
    'Provence-Alpes-Côte d\'Azur': [43.9352, 6.0679],
    'Nord-Pas-de-Calais': [50.4801, 2.7937],
    'Occitanie': [43.8927, 3.2828],
    'Nouvelle-Aquitaine': [44.8378, -0.5792],
    'Auvergne-Rhône-Alpes': [45.4473, 4.3859],
    'Bretagne': [48.2020, -2.9326],
    'Normandie': [49.1829, -0.3707],
    'Grand Est': [48.6998, 6.1878],
    # Ajoutez les coordonnées d'autres régions si nécessaire
}

# Sélection de l'année par l'utilisateur
selected_year_france = st.slider('Select Year for France', int(df_france['Année'].min()), int(df_france['Année'].max()), int(df_france['Année'].max()))

# Traitement des données pour obtenir l'année sélectionnée
df_yearly_france = df_france[df_france['Année'] == selected_year_france]

# Initialisation de la carte Pydeck pour la France
view_state_france = pdk.ViewState(latitude=46.2276, longitude=2.2137, zoom=5, pitch=50)

# Génération des couches pour Pydeck pour la France
layers_france = []
for region, (lat, lon) in coordinates_france.items():
    elevation = df_yearly_france[region].values[0] * 1e4  # Échelle pour visibilité
    layers_france.append(pdk.Layer(
        "ColumnLayer",
        data=pd.DataFrame([{
            "position": [lon, lat],
            "elevation": elevation,
        }]),
        get_position='position',
        get_elevation='elevation',
        elevation_scale=100,
        radius=8000,
        get_fill_color="[255, 165, 0, 180]",  # Couleur des colonnes
        pickable=True,
        auto_highlight=True,
    ))

# Création de la carte Pydeck avec les couches pour la France
r_france = pdk.Deck(
    layers=layers_france,
    initial_view_state=view_state_france,
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip={
        'html': '<b>Région:</b> {region} <br><b>Pourcentage:</b> {elevation}%'
    }
)

# Affichage de la carte PyDeck dans l'application Streamlit pour la France
st.pydeck_chart(r_france)
