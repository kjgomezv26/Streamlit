import pandas as pd

# Leer dataset
df = pd.read_csv("../data/tracks.csv")

print("Primeras filas")
print(df.head())

print("\nInformación")
print(df.info())

print("\nValores nulos")
print(df.isnull().sum())

print("\nEstadísticas")
print(df.describe())

print("\nColumnas")
print(df.columns)