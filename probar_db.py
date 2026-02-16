from database.consultas import obtener_contenido_por_selecciones

selecciones = {
    "Familia de la celda": "AIS",
    "Celda": "SM6"
}

contenidos = obtener_contenido_por_selecciones(selecciones)

print(f"Total: {len(contenidos)} contenidos\n")

for c in contenidos:
    print(f"Tipo: {c['tipo']}")
    if c['tipo'] == 'imagen':
        print(f"  Imagen: {c.get('imagen', 'NO HAY DATOS DE IMAGEN')}")
    else:
        print(f"  Texto: {c.get('texto', '')[:50]}...")
    print("-" * 50)