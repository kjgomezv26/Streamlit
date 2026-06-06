import ast
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Spotify Tracks Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("../data/tracks.csv")

    # Limpieza básica
    df = df.dropna(subset=["id"])
    df["name"] = df["name"].fillna("Sin nombre")

    # Fecha
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

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
# Sidebar - filtros
# =========================

st.sidebar.header("Filtros")

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.sidebar.slider(
    "Rango de años",
    min_year,
    max_year,
    (2000, max_year)
)

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

df_filtered = df[
    (df["release_year"] >= year_range[0]) &
    (df["release_year"] <= year_range[1]) &
    (df["popularity"] >= popularity_range[0]) &
    (df["popularity"] <= popularity_range[1]) &
    (df["explicit_label"].isin(explicit_filter))
]

# =========================
# KPIs
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracks", f"{df_filtered.shape[0]:,}")
col2.metric("Artistas", f"{df_filtered['main_artist'].nunique():,}")
col3.metric("Popularidad promedio", round(df_filtered["popularity"].mean(), 2))
col4.metric("Duración promedio", f"{round(df_filtered['duration_min'].mean(), 2)} min")

st.divider()

# =========================
# Dataset
# =========================

with st.expander("Ver datos filtrados"):
    st.dataframe(df_filtered.head(1000), use_container_width=True)

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

st.subheader("Relación entre características musicales")

feature_x = st.selectbox(
    "Variable eje X",
    [
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "loudness",
        "duration_min"
    ]
)

feature_y = st.selectbox(
    "Variable eje Y",
    [
        "popularity",
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "valence",
        "tempo"
    ]
)

sample_df = df_filtered.sample(
    min(5000, len(df_filtered)),
    random_state=42
)

fig_scatter = px.scatter(
    sample_df,
    x=feature_x,
    y=feature_y,
    color="explicit_label",
    hover_data=["name", "main_artist", "release_year"],
    title=f"Relación entre {feature_x} y {feature_y}"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# Top canciones
# =========================

st.subheader("Top canciones por popularidad")

top_tracks = (
    df_filtered
    .sort_values("popularity", ascending=False)
    [["name", "main_artist", "release_year", "popularity", "duration_min", "explicit_label"]]
    .head(20)
)

st.dataframe(top_tracks, use_container_width=True)

# =========================
# Top artistas
# =========================

st.subheader("Top artistas por cantidad de tracks")

top_artists = (
    df_filtered
    .groupby("main_artist")
    .size()
    .reset_index(name="cantidad_tracks")
    .sort_values("cantidad_tracks", ascending=False)
    .head(20)
)

fig_artists = px.bar(
    top_artists,
    x="cantidad_tracks",
    y="main_artist",
    orientation="h",
    title="Top 20 artistas con más tracks"
)

st.plotly_chart(fig_artists, use_container_width=True)