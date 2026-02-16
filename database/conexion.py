"""Conexion ala base de datos SQLite"""

import sqlite3
import os

def obtener_ruta_db():
    """Obtener la ruta completa al archivo de base de datos"""
    #obtener la carpeta raiz del proyecto
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # a base de datos estara en la carpeta 'datos'
    ruta_db = os.path.join(ruta_base, 'datos', 'prokit.db')
    return ruta_db

def conectar():
    """Crea y devuelve una conexión a la base de datos"""
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    # Esto permite acceder a las columnas por nombre
    conexion.row_factory = sqlite3.Row
    return conexion

