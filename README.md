# Spotify Tracks Visualization

Proyecto de visualización de datos utilizando Python, Pandas y Streamlit sobre un conjunto de datos de canciones de Spotify.

## Estructura del proyecto

```text
Streamlit/
│
├── data/
│   └── tracks.csv
│
├── src/
│   ├── eda.py
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Descripción de carpetas

* **data/**: contiene el dataset utilizado para el análisis.
* **src/eda.py**: script para el análisis exploratorio de datos (EDA).
* **src/app.py**: aplicación web desarrollada con Streamlit.
* **requirements.txt**: dependencias necesarias para ejecutar el proyecto.

## Configuración del entorno

Clonar el repositorio:

```bash
git clone https://github.com/kjgomezv26/Streamlit.git
cd Streamlit
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual:

### Windows (Git Bash)

```bash
source venv/Scripts/activate
```

### Windows (CMD)

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Análisis Exploratorio de Datos (EDA)

Ejecutar:

```bash
python src/eda.py
```

## Ejecutar la aplicación Streamlit

```bash
streamlit run src/app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

## Dataset

El dataset utilizado corresponde a información de más de 500.000 canciones de Spotify, incluyendo variables como:

*Danceability (Bailabilidad): Mide qué tan adecuada es una pista para bailar basándose en el tempo, la estabilidad del ritmo, la fuerza del compás y la regularidad general. Un valor de 1.0 significa que es extremadamente bailable.

*Energy (Energía): Representa una medida perceptual de intensidad y actividad. Las pistas enérgicas se sienten rápidas, fuertes y ruidosas (ej. el Death Metal tendría un valor cercano a 1.0, mientras que un preludio de Bach estaría cerca de 0.0).

*Valence (Valencia): Describe la positividad musical que transmite una pista. Las pistas con alta valencia (cercanas a 1.0) suenan felices, alegres o eufóricas, mientras que las pistas con baja valencia suenan tristes, deprimidas o enojadas.

*Acousticness (Acusticidad): Es una medida de confianza de si la pista es acústica o no. Un valor alto indica una alta probabilidad de que la canción no utilice instrumentos electrónicos o sintetizadores.

*Instrumentalness (Instrumentalidad): Predice si una pista no contiene voces humanas. Cuanto más se acerque a 1.0, mayor es la probabilidad de que la pista sea instrumental (sin letra).

*Liveness (Vivacidad): Detecta la presencia de una audiencia en la grabación. Valores altos indican que es muy probable que la canción se haya grabado en vivo durante un concierto y no en un estudio aislado.

*Loudness (Sonoridad): Es el volumen general promedio de una pista medido en decibelios (dB).

*Tempo: Es la velocidad o el ritmo general estimado de una pista, medido en pulsaciones por minuto (BPM).

*Duration_min: Esta es la variable que calculamos en la aplicación; es simplemente la duración total del archivo de audio en minutos.
