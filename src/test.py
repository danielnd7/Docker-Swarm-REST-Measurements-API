from flask import Flask, request
from redis import Redis, RedisError
import os
import socket # Para obtener el ID/Hostname
from datetime import datetime # Para convertir timestamps
import tensorflow as tf  # Para cargar el modelo de detección de anomalías
import json  # Para cargar el threshold desde un archivo
import numpy as np  # Para manipulación de arrays


try:
    # Cargamos el modelo para deteccion de anomalías
    model = tf.keras.models.load_model('lstm-model.keras')
    # Cargamos el threshold desde un archivo para deteccion de anomalías
    with open('config-lstm-model.json', 'r') as config_file:
        config = json.load(config_file)
        threshold = config.get('threshold')
        window_size = config.get('window_size', 10)  # Tamaño de ventana por defecto 10
    print(f"Modelo y threshold cargados correctamente. Threshold: {threshold}")
except Exception as e:
    print(f"Error al cargar el modelo y threshold: {str(e)}")


last_window = [69.88083514, 71.22022706, 70.87780496, 68.95939994, 69.28355102, 70.06096581, 69.27976479, 69.36960846, 69.16671394, 68.98608257] # Lista para almacenar los ultimos valores

x_input = np.array(last_window)  # Convertir a array de numpy
x_input = x_input.reshape((1, window_size, 1))  # Reshape para el modelo LSTM (n_features=1, )
print(x_input)
print(x_input.shape)

# Hacer la predicción
prediction = model.predict(x_input)

print(f"Predicción del siguiente valor de temperatura: {prediction}")




error = abs(prediction[0][0] - dato)

if error > threshold:
    print(f"Temperatura recibida: <b>{dato}°C</b> <br><b style='color:red;'>Anomalía detectada! Error: {error} Prediccion : {prediction}</b>")
else:
    print(f"Temperatura recibida: <b>{dato}°C</b> <br>No se detectaron anomalías. Error: {error}")
