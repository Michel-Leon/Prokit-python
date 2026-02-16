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
    """
    Crea y devuelve una conexión a la base de datos.
    
    Uso:
        conn = conectar()
        cursor = conn.cursor()
        # ... hacer consultas ...
        conn.close()
    """
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    # Esto permite acceder a las columnas por nombre
    conexion.row_factory = sqlite3.Row
    return conexion

def ejecutar_consulta(sql, parametros=None):
    """
    Ejecuta una consulta SQL con parámetros opcionales.
    
    Args:
        sql (str): La consulta SQL a ejecutar.
        parametros (tuple, optional): Los parámetros para la consulta. Por defecto es None.
    
    Returns:
        list: Una lista de filas resultantes de la consulta.
    """
    conn = conectar()
    cursor = conn.cursor()
    if parametros:
        cursor.execute(sql, parametros)
    else:
        cursor.execute(sql)
        
    resultados = cursor.fetchall()
    conn.close()
    return resultados   

def ejecutar_insert(sql, parametros=None):
    """
        Ejecuta in INSET Y devuelve el ID del registro insertado.
        
        retorna:
            el ID del nuevo registro insertado.
    """
    conn = conectar()
    cursor = conn.cursor()
    if parametros:
        cursor.execute(sql, parametros)
    else:
        cursor.execute(sql)
        
    nuevo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return nuevo_id