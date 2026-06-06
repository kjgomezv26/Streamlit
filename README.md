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

* Popularidad
* Duración
* Artista
* Fecha de lanzamiento
* Danceability
* Energy
* Acousticness
* Valence
* Tempo
* Entre otras características musicales
