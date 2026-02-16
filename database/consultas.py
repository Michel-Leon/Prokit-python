"""
Funciones para consultar la base de datos.
Estas funciones se usan desde el editor de glosas.
"""

import json
from .conexion import conectar, ejecutar_consulta


def obtener_contenido_por_selecciones(selecciones: dict) -> list:
    """
    Obtiene el contenido que coincide con las selecciones del usuario.
    
    Parámetros:
        selecciones: Diccionario con las selecciones del usuario
                     Ejemplo: {"Familia de la celda": "AIS", "Celda": "SM6"}
    
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
        # Convertir las condiciones de JSON a diccionario
        condiciones = json.loads(row['condiciones'])
        
        # Verificar si las selecciones cumplen TODAS las condiciones
        cumple = True
        for campo, valor_requerido in condiciones.items():
            valor_usuario = selecciones.get(campo, "")
            if valor_usuario != valor_requerido:
                cumple = False
                break
        
        # Si cumple todas las condiciones, agregar a resultados
        if cumple:
            resultados.append({
                'id': row['id'],
                'titulo': row['titulo'],
                'texto': row['texto'],
                'tipo': row['tipo'],
                'seccion_nombre': row['seccion_nombre'],
                'seccion_numero': row['seccion_numero'],
            })
    
    conn.close()
    return resultados


def obtener_imagenes_contenido(contenido_id: int) -> list:
    """
    Obtiene las imágenes asociadas a un contenido.
    
    Retorna:
        Lista de diccionarios con información de las imágenes
    """
    sql = '''
        SELECT nombre_archivo, ruta, pie_de_imagen, ancho, alto
        FROM imagen
        WHERE contenido_id = ?
    '''
    
    resultados = ejecutar_consulta(sql, (contenido_id,))
    
    imagenes = []
    for row in resultados:
        imagenes.append({
            'nombre': row['nombre_archivo'],
            'ruta': row['ruta'],
            'pie': row['pie_de_imagen'],
            'ancho': row['ancho'],
            'alto': row['alto']
        })
    
    return imagenes


def obtener_tabla_contenido(contenido_id: int) -> dict:
    """
    Obtiene una tabla asociada a un contenido.
    
    Retorna:
        Diccionario con la estructura de la tabla y sus filas
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener la tabla
    cursor.execute('''
        SELECT id, nombre, columnas
        FROM tabla_datos
        WHERE contenido_id = ?
    ''', (contenido_id,))
    
    tabla_row = cursor.fetchone()
    
    if not tabla_row:
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
        filas.append(json.loads(row['datos']))
    
    conn.close()
    
    return {
        'nombre': tabla_row['nombre'],
        'columnas': json.loads(tabla_row['columnas']),
        'filas': filas
    }


def obtener_todas_las_secciones() -> list:
    """
    Obtiene todas las secciones disponibles.
    
    Retorna:
        Lista de secciones ordenadas
    """
    sql = '''
        SELECT id, nombre, numero, orden
        FROM seccion
        ORDER BY orden
    '''
    
    resultados = ejecutar_consulta(sql)
    
    secciones = []
    for row in resultados:
        secciones.append({
            'id': row['id'],
            'nombre': row['nombre'],
            'numero': row['numero'],
            'orden': row['orden']
        })
    
    return secciones