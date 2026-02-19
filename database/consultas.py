"""Funciones para consultar contenido según las selecciones del usuario"""

import json
from .conexion import conectar


def obtener_contenido_por_selecciones(selecciones: dict) -> list:
    """
    Obtiene el contenido que coincide con las selecciones del usuario.
    
    Parámetros:
        selecciones: {"Familia de la celda": "AIS", "Celda": "SM6", ...}
    
    Retorna:
        Lista de diccionarios con el contenido a mostrar
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener todos los contenidos con sus reglas
    cursor.execute('''
        SELECT 
            c.id,
            c.titulo,
            c.texto,
            c.tipo,
            c.orden,
            s.nombre as seccion_nombre,
            s.numero as seccion_numero,
            s.orden as seccion_orden,
            r.condiciones
        FROM contenido c
        JOIN seccion s ON s.id = c.seccion_id
        JOIN regla_contenido r ON r.contenido_id = c.id
        ORDER BY s.orden, c.orden
    ''')
    
    resultados = []
    
    for row in cursor.fetchall():
        # Convertir condiciones de JSON a diccionario
        try:
            condiciones = json.loads(row['condiciones'])
        except:
            continue
        
        # Verificar si las selecciones cumplen TODAS las condiciones
        cumple = True
        for campo, valor_requerido in condiciones.items():
            valor_usuario = selecciones.get(campo, "")
            if valor_usuario != valor_requerido:
                cumple = False
                break
        
        # Si cumple todas las condiciones, agregar a resultados
        if cumple:
            item = {
                'id': row['id'],
                'titulo': row['titulo'],
                'texto': row['texto'],
                'tipo': row['tipo'],
                'orden': row['orden'],
                'seccion_nombre': row['seccion_nombre'],
                'seccion_numero': row['seccion_numero'],
            }
            
            # Si es tipo imagen, obtener los datos de la imagen
            if row['tipo'] == 'imagen':
                imagen_data = obtener_imagen(row['id'], cursor)
                if imagen_data:
                    item['imagen'] = imagen_data
            
            # Si es tipo tabla, obtener los datos de la tabla
            if row['tipo'] == 'tabla':
                tabla_data = obtener_tabla(row['id'], cursor)
                if tabla_data:
                    item['tabla'] = tabla_data        
            
            resultados.append(item)
    
    conn.close()
    return resultados


def obtener_imagen(contenido_id: int, cursor=None) -> dict:
    """
    Obtiene la imagen asociada a un contenido.
    
    Parámetros:
        contenido_id: ID del contenido
        cursor: Cursor de la conexión (opcional)
    
    Retorna:
        Diccionario con datos de la imagen o None
    """
    cerrar_conexion = False
    
    if cursor is None:
        conn = conectar()
        cursor = conn.cursor()
        cerrar_conexion = True
    
    cursor.execute('''
        SELECT nombre_archivo, ruta, pie_de_imagen, ancho, alto
        FROM imagen
        WHERE contenido_id = ?
    ''', (contenido_id,))
    
    row = cursor.fetchone()
    
    if cerrar_conexion:
        conn.close()
    
    if row:
        return {
            'nombre': row['nombre_archivo'],
            'ruta': row['ruta'],
            'pie': row['pie_de_imagen'],
            'ancho': row['ancho'] if row['ancho'] else 400,
            'alto': row['alto'] if row['alto'] else 300
        }
    
    return None


def obtener_todas_las_secciones() -> list:
    """
    Obtiene todas las secciones disponibles.
    
    Retorna:
        Lista de secciones ordenadas
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nombre, numero, orden
        FROM seccion
        ORDER BY orden
    ''')
    
    resultados = cursor.fetchall()
    conn.close()
    
    secciones = []
    for row in resultados:
        secciones.append({
            'id': row['id'],
            'nombre': row['nombre'],
            'numero': row['numero'],
            'orden': row['orden']
        })
    
    return secciones
def obtener_tabla(contenido_id: int, cursor=None) -> dict:
    """
    Obtiene una tabla asociada a un contenido.
    
    Retorna:
        Diccionario con estructura: {nombre, columnas, filas}
    """
    cerrar_conexion = False
    
    if cursor is None:
        conn = conectar()
        cursor = conn.cursor()
        cerrar_conexion = True
    
    # Obtener metadata de la tabla
    cursor.execute('''
        SELECT id, nombre, columnas
        FROM tabla_datos
        WHERE contenido_id = ?
    ''', (contenido_id,))
    
    tabla_row = cursor.fetchone()
    
    if not tabla_row:
        if cerrar_conexion:
            conn.close()
        return None
    
    # Obtener las filas
    cursor.execute('''
        SELECT datos
        FROM tabla_fila
        WHERE tabla_id = ?
        ORDER BY fila_numero
    ''', (tabla_row['id'],))
    
    filas = []
    for row in cursor.fetchall():
        try:
            fila_datos = json.loads(row['datos'])
            filas.append(fila_datos)
        except:
            continue
    
    if cerrar_conexion:
        conn.close()
    
    # Parsear columnas
    try:
        columnas = json.loads(tabla_row['columnas'])
    except:
        columnas = []
    
    return {
        'nombre': tabla_row['nombre'],
        'columnas': columnas,
        'filas': filas
    }