import ast
import pandas as pd
import streamlit as st
import plotly.express as px
import kagglehub
import os

st.set_page_config(
    page_title="Spotify Tracks Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    # 1. Descarga el dataset a la caché local usando kagglehub
    path = kagglehub.dataset_download("yamaerenay/spotify-dataset-19212020-600k-tracks")
    
    # 2. Apunta específicamente al archivo tracks.csv
    csv_path = os.path.join(path, "tracks.csv")
    
    # 3. Leer el CSV con Pandas
    df = pd.read_csv(csv_path)

    # Limpieza básica
    df = df.dropna(subset=["id"])
    df["name"] = df["name"].fillna("Sin nombre")

    # Fecha
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year
    
    # Forzamos a que el año sea entero antes de calcular la década
    # Llenamos los nulos temporalmente con 0 para que no falle la conversión
    df["release_year"] = df["release_year"].fillna(0).astype(int)
    
    # Derivación de datos: Década limpia (ej. 1980s)
    df["decade"] = (df["release_year"] // 10) * 10
    df["decade"] = df["decade"].astype(str) + "s"
    
    # Quitamos los que quedaron como "0s" por los nulos
    df = df[df["decade"] != "0s"]
    # Duración en minutos
    df["duration_min"] = df["duration_ms"] / 60000

    # Convertir explicit a etiqueta
    df["explicit_label"] = df["explicit"].map({
        0: "No explícita",
        1: "Explícita"
    })

    # Extraer artista principal
    def get_main_artist(value):
        try:
            artists = ast.literal_eval(value)
            if isinstance(artists, list) and len(artists) > 0:
                return artists[0]
        except:
            return value
        return "Desconocido"

    df["main_artist"] = df["artists"].apply(get_main_artist)

    return df

df = load_data()

st.title("Dashboard de Tracks de Spotify")

st.markdown(
    """
    Exploración de canciones de Spotify usando variables como popularidad,
    duración, año de lanzamiento y características musicales.
    """
)

# =========================
# Sidebar - filtros interactivos
# =========================

st.sidebar.header("Filtros")

# Filtro por Artista (Buscador de texto)
artist_search = st.sidebar.text_input("Buscar Artista (ej. Bad Bunny)", "")

st.sidebar.markdown("---")

# =========================
# Lógica de Interacción Bidireccional
# =========================
min_year_global = int(df["release_year"].min())
max_year_global = int(df["release_year"].max())

# Inicializar estados si no existen
if "year_slider" not in st.session_state:
    st.session_state.year_slider = (min_year_global, max_year_global)

if "decade_selector" not in st.session_state:
    st.session_state.decade_selector = "Todas"

# Callbacks
def update_slider_from_decade():
    chosen_decade = st.session_state.decade_selector
    if chosen_decade == "Todas":
        st.session_state.year_slider = (min_year_global, max_year_global)
    else:
        anio_inicio = int(chosen_decade[:4])
        anio_fin = anio_inicio + 9
        st.session_state.year_slider = (max(min_year_global, anio_inicio), min(max_year_global, anio_fin))

def reset_decade_from_slider():
    st.session_state.decade_selector = "Todas"

decades = sorted(df["decade"].dropna().unique())
opciones_decadas = ["Todas"] + decades

# Widgets enlazados a los callbacks
decade_filter = st.sidebar.selectbox(
    "Seleccione una Década",
    options=opciones_decadas,
    key="decade_selector",
    on_change=update_slider_from_decade
)

year_range = st.sidebar.slider(
    "Rango de años específico",
    min_value=min_year_global,
    max_value=max_year_global,
    key="year_slider",
    on_change=reset_decade_from_slider
)

st.sidebar.markdown("---")

popularity_range = st.sidebar.slider(
    "Popularidad",
    int(df["popularity"].min()),
    int(df["popularity"].max()),
    (0, 100)
)

explicit_filter = st.sidebar.multiselect(
    "Contenido explícito",
    options=df["explicit_label"].dropna().unique(),
    default=df["explicit_label"].dropna().unique()
)

# Aplicar los filtros al dataframe
df_filtered = df[
    (df["release_year"] >= year_range[0]) &
    (df["release_year"] <= year_range[1]) &
    (df["popularity"] >= popularity_range[0]) &
    (df["popularity"] <= popularity_range[1]) &
    (df["explicit_label"].isin(explicit_filter))
]

# El filtro de década ya está implícito en el rango del slider, 
# pero lo dejamos como seguro adicional si no es "Todas".
if decade_filter != "Todas":
    df_filtered = df_filtered[df_filtered["decade"] == decade_filter]

# Aplicar filtro de artista si el usuario escribió algo
if artist_search:
    df_filtered = df_filtered[df_filtered["main_artist"].str.contains(artist_search, case=False, na=False)]

# =========================
# KPIs
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracks Filtrados", f"{df_filtered.shape[0]:,}")
col2.metric("Artistas Diferentes", f"{df_filtered['main_artist'].nunique():,}")
col3.metric("Popularidad Promedio", round(df_filtered["popularity"].mean(), 2))
col4.metric("Duración Promedio", f"{round(df_filtered['duration_min'].mean(), 2)} min")

st.divider()

# =========================
# Dataset
# =========================

with st.expander("Ver datos filtrados"):
    # Hacemos un drop temporal solo para la vista, así no rompemos los datos originales
    df_vista = df_filtered.drop(columns=["id", "id_artists"], errors="ignore")
    st.dataframe(df_vista.head(1000), use_container_width=True)
    
# =========================
# Gráficas
# =========================

st.subheader("Distribución de popularidad")

fig_pop = px.histogram(
    df_filtered,
    x="popularity",
    nbins=50,
    title="Distribución de la popularidad"
)
st.plotly_chart(fig_pop, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Tracks por año")

    tracks_by_year = (
        df_filtered
        .groupby("release_year")
        .size()
        .reset_index(name="cantidad_tracks")
        .sort_values("release_year")
    )

    fig_year = px.line(
        tracks_by_year,
        x="release_year",
        y="cantidad_tracks",
        title="Cantidad de tracks por año"
    )
    st.plotly_chart(fig_year, use_container_width=True)

with col_b:
    st.subheader("Popularidad promedio por año")

    popularity_by_year = (
        df_filtered
        .groupby("release_year")["popularity"]
        .mean()
        .reset_index()
    )

    fig_pop_year = px.line(
        popularity_by_year,
        x="release_year",
        y="popularity",
        title="Popularidad promedio por año"
    )
    st.plotly_chart(fig_pop_year, use_container_width=True)

st.divider()

# =========================
# Mapa de Calor de Correlaciones
# =========================
st.subheader("Mapa de Calor de Correlaciones (Heatmap)")

# Seleccionamos solo las variables cuantitativas para correlacionar
corr_cols = ["popularity", "danceability", "energy", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "loudness", "duration_min"]

# Calculamos la matriz de correlación
corr_matrix = df_filtered[corr_cols].corr()

fig_heatmap = px.imshow(
    corr_matrix, 
    text_auto=".2f", 
    aspect="auto",
    color_continuous_scale="RdBu_r",
    title="Correlación entre características musicales"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# =========================
# Scatter Plot mejorado (Añadido canal de tamaño)
# =========================
st.subheader("Relación entre características musicales")

col_x, col_y = st.columns(2)
with col_x:
    feature_x = st.selectbox(
        "Variable eje X",
        ["danceability", "energy", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "loudness", "duration_min"]
    )
with col_y:
    feature_y = st.selectbox(
        "Variable eje Y",
        ["energy", "popularity", "danceability", "acousticness", "instrumentalness", "valence", "tempo"]
    )

# Muestreo para que el navegador no colapse con cientos de miles de puntos
sample_df = df_filtered.sample(
    min(3000, len(df_filtered)),
    random_state=42
)

fig_scatter = px.scatter(
    sample_df,
    x=feature_x,
    y=feature_y,
    color="explicit_label",
    size="popularity",         # <- Añadido canal visual de tamaño
    size_max=15,               # <- Limita el tamaño máximo de la burbuja
    hover_data=["name", "main_artist", "release_year"],
    title=f"Relación entre {feature_x} y {feature_y} (Tamaño = Popularidad)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# Top canciones y artistas
# =========================

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Top canciones por popularidad")
    top_tracks = (
        df_filtered
        .sort_values("popularity", ascending=False)
        [["name", "main_artist", "release_year", "popularity", "duration_min", "explicit_label"]]
        .head(20)
    )
    st.dataframe(top_tracks, use_container_width=True)

with col_d:
    st.subheader("Top artistas por cantidad de tracks")
    top_artists = (
        df_filtered
        .groupby("main_artist")
        .size()
        .reset_index(name="cantidad_tracks")
        .sort_values("cantidad_tracks", ascending=False)
        .head(10)
    )
    fig_artists = px.bar(
        top_artists,
        x="cantidad_tracks",
        y="main_artist",
        orientation="h",
        title="Top 10 artistas con más tracks"
    )
    # Reordenar para que el más grande salga arriba
    fig_artists.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_artists, use_container_width=True)