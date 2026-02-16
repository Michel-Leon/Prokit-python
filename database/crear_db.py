"""
Script para crear la base de datos de PROKIT.
Ejecutar UNA SOLA VEZ para crear las tablas.
"""

import sqlite3
import os


def crear_base_de_datos():
    """Crea todas las tablas de la base de datos"""
    
    # Obtener ruta
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(ruta_base, "datos", "prokit.db")
    
    print(f"Creando base de datos en: {ruta_db}")
    
    # Conectar (si no existe el archivo, lo crea)
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    # =========================================
    # TABLA 1: seccion
    # Define las secciones del documento
    # Ejemplo: "1.1 Descripción", "1.2 Características"
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            numero TEXT,
            orden INTEGER DEFAULT 0,
            padre_id INTEGER DEFAULT NULL,
            FOREIGN KEY (padre_id) REFERENCES seccion(id)
        )
    ''')
    print("✓ Tabla 'seccion' creada")
    
    # =========================================
    # TABLA 2: contenido
    # Guarda los textos, títulos y referencias
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seccion_id INTEGER NOT NULL,
            tipo TEXT DEFAULT 'texto',
            titulo TEXT,
            texto TEXT,
            orden INTEGER DEFAULT 0,
            FOREIGN KEY (seccion_id) REFERENCES seccion(id)
        )
    ''')
    print("✓ Tabla 'contenido' creada")
    
    # =========================================
    # TABLA 3: imagen
    # Guarda información de las imágenes
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido_id INTEGER NOT NULL,
            nombre_archivo TEXT NOT NULL,
            ruta TEXT,
            pie_de_imagen TEXT,
            ancho INTEGER DEFAULT 400,
            alto INTEGER DEFAULT 300,
            FOREIGN KEY (contenido_id) REFERENCES contenido(id)
        )
    ''')
    print("✓ Tabla 'imagen' creada")
    
    # =========================================
    # TABLA 4: tabla_datos
    # Guarda la estructura de las tablas
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido_id INTEGER NOT NULL,
            nombre TEXT,
            columnas TEXT,
            FOREIGN KEY (contenido_id) REFERENCES contenido(id)
        )
    ''')
    print("✓ Tabla 'tabla_datos' creada")
    
    # =========================================
    # TABLA 5: tabla_fila
    # Guarda las filas de cada tabla
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_fila (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabla_id INTEGER NOT NULL,
            fila_numero INTEGER DEFAULT 0,
            datos TEXT,
            FOREIGN KEY (tabla_id) REFERENCES tabla_datos(id)
        )
    ''')
    print("✓ Tabla 'tabla_fila' creada")
    
    # =========================================
    # TABLA 6: regla_contenido
    # Define CUÁNDO mostrar cada contenido
    # según las selecciones del usuario
    # =========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regla_contenido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido_id INTEGER NOT NULL,
            condiciones TEXT NOT NULL,
            FOREIGN KEY (contenido_id) REFERENCES contenido(id)
        )
    ''')
    print("✓ Tabla 'regla_contenido' creada")
    
    # Guardar cambios
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("¡Base de datos creada exitosamente!")
    print("="*50)


def insertar_datos_ejemplo():
    """Inserta datos de ejemplo para probar"""
    
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(ruta_base, "datos", "prokit.db")
    
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    print("\nInsertando datos de ejemplo...")
    
    # =========================================
    # SECCIONES
    # =========================================
    secciones = [
        ("Descripción", "1.1", 1, None),
        ("Condiciones Generales", "1.2", 2, None),
        ("Características Técnicas", "1.3", 3, None),
    ]
    
    cursor.executemany('''
        INSERT INTO seccion (nombre, numero, orden, padre_id)
        VALUES (?, ?, ?, ?)
    ''', secciones)
    print("✓ Secciones insertadas")
    
    # =========================================
    # CONTENIDO PARA SM6 (AIS + 24Kv)
    # =========================================
    
    # Contenido 1: Descripción para SM6
    cursor.execute('''
        INSERT INTO contenido (seccion_id, tipo, titulo, texto, orden)
        VALUES (1, 'texto', 'Descripción General', 
                'Las celdas SM6 son equipos de media tensión tipo modular, aisladas en aire (AIS), diseñadas para distribución secundaria hasta 24kV. Estas celdas garantizan la seguridad del operador mediante compartimentos separados y enclavamientos mecánicos.

Características principales:
- Diseño compacto y modular
- Fácil instalación y mantenimiento
- Alta seguridad operativa
- Tecnología probada mundialmente', 1)
    ''')
    contenido_sm6_desc = cursor.lastrowid
    
    # Regla: mostrar cuando familia=AIS, celda=SM6
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "AIS", "Celda": "SM6"}')
    ''', (contenido_sm6_desc,))
    
    # Contenido 2: Condiciones para SM6
    cursor.execute('''
        INSERT INTO contenido (seccion_id, tipo, titulo, texto, orden)
        VALUES (2, 'texto', 'Condiciones de Operación',
                'Las condiciones generales de operación son:

- Tensión nominal: 24 kV
- Tensión de aislamiento: 28 kV
- Frecuencia: 50/60 Hz
- Temperatura ambiente: -5°C a +40°C
- Altitud máxima: 1000 m.s.n.m.
- Humedad relativa: hasta 95%

Los equipos SM6 cumplen con las normas IEC 62271-200 e IEC 62271-1.', 1)
    ''')
    contenido_sm6_cond = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "AIS", "Celda": "SM6", "Condiciones Generales": "Aplica"}')
    ''', (contenido_sm6_cond,))
    
    # =========================================
    # CONTENIDO PARA PIX (AIS + 24Kv + Primaria)
    # =========================================
    
    cursor.execute('''
        INSERT INTO contenido (seccion_id, tipo, titulo, texto, orden)
        VALUES (1, 'texto', 'Descripción General',
                'Las celdas PIX son equipos de media tensión diseñadas para aplicaciones de distribución primaria. Ofrecen una solución robusta y confiable para subestaciones de hasta 24kV.

Características principales:
- Diseño robusto para distribución primaria
- Interruptores extraíbles
- Sistema de enclavamientos completo
- Preparadas para automatización', 1)
    ''')
    contenido_pix_desc = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "AIS", "Celda": "PIX"}')
    ''', (contenido_pix_desc,))
    
    # =========================================
    # CONTENIDO PARA GIS (GBGS-0)
    # =========================================
    
    cursor.execute('''
        INSERT INTO contenido (seccion_id, tipo, titulo, texto, orden)
        VALUES (1, 'texto', 'Descripción General',
                'Las celdas GBGS son equipos de media tensión con aislamiento en gas SF6 (GIS), diseñadas para instalaciones donde el espacio es limitado o se requiere máxima confiabilidad.

Características principales:
- Aislamiento en SF6 (gas hexafluoruro de azufre)
- Diseño ultra compacto
- Libre de mantenimiento
- Ideal para ambientes agresivos
- Mayor vida útil', 1)
    ''')
    contenido_gis_desc = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "GIS", "Celda": "GBGS-0"}')
    ''', (contenido_gis_desc,))
    
    # También para GBGS-2
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "GIS", "Celda": "GBGS-2"}')
    ''', (contenido_gis_desc,))
    
    # =========================================
    # CONTENIDO PARA 2SIS (Premset)
    # =========================================
    
    cursor.execute('''
        INSERT INTO contenido (seccion_id, tipo, titulo, texto, orden)
        VALUES (1, 'texto', 'Descripción General',
                'Las celdas Premset utilizan tecnología 2SIS (Shielded Solid Insulation System), una innovación que combina aislamiento sólido con protección blindada, eliminando el uso de SF6.

Características principales:
- Tecnología libre de SF6
- Aislamiento sólido blindado
- Amigable con el medio ambiente
- Bajo mantenimiento
- Diseño compacto y seguro', 1)
    ''')
    contenido_premset_desc = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO regla_contenido (contenido_id, condiciones)
        VALUES (?, '{"Familia de la celda": "2SIS", "Celda": "Premset"}')
    ''', (contenido_premset_desc,))
    
    # Guardar cambios
    conn.commit()
    conn.close()
    
    print("✓ Contenidos de ejemplo insertados")
    print("\n" + "="*50)
    print("¡Datos de ejemplo insertados!")
    print("="*50)


# =========================================
# EJECUTAR EL SCRIPT
# =========================================
if __name__ == "__main__":
    print("="*50)
    print("   CREACIÓN DE BASE DE DATOS PROKIT")
    print("="*50 + "\n")
    
    # Crear las tablas
    crear_base_de_datos()
    
    # Preguntar si insertar datos de ejemplo
    respuesta = input("\n¿Desea insertar datos de ejemplo? (s/n): ")
    if respuesta.lower() == 's':
        insertar_datos_ejemplo()
    
    print("\n¡Proceso completado!")