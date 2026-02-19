from database.consultas import obtener_contenido_por_selecciones

selecciones = {
    "Tipo de celda": "Secundaria",
    "Nivel de tensión": "24 Kv",
    "Familia de la celda": "AIS",
    "Celda": "SM6",
    "Características generales": "Aplica"
}

contenidos = obtener_contenido_por_selecciones(selecciones)

print(f"Total contenidos: {len(contenidos)}\n")

for c in contenidos:
    print(f"ID: {c['id']} | Tipo: {c['tipo']} | Orden: {c.get('orden', '?')}")
    if c['tipo'] == 'tabla':
        print(f"  TABLA: {c.get('tabla', 'NO HAY DATOS')}")
    print("-" * 50)