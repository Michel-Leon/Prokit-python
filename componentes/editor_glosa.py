""" Componentes: editor de glosa -Redaccion de proyecto"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,QFrame,QLabel, QPushButton,
    QScrollArea, QSplitter, QGraphicsDropShadowEffect, QSizePolicy
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor,QFont
import qtawesome as qta

# ============================================================
# DATOS DE PRUEBA - Estructura jerárquica del sistema eléctrico
# ============================================================
DATOS_SISTEMA = {
    "Sección de Media Tensión": {
        "tipo_celda": {
            "titulo": "Tipo de celda",
            "opciones": ["Primaria", "Secundaria"]
        },
        "nivel_tension": {
            "titulo": "Nivel de tensión",
            "opciones": ["24 Kv", "36 Kv"]
        },
        "familia_celda": {
            "titulo": "Familia de la celda",
            "opciones": ["AIS", "2SIS"],
            "nota": "Nota: celda cambia según la selección de familia"
        },
        "celda": {
            "dependencias": {
                "AIS": ["SM6", "SM AIRSET"],
                "2SIS": ["MCSet", "PIX"]
            },
            "titulo": "Celda"
        },
        "condiciones_generales": {
            "titulo": "Condiciones Generales",
            "opciones": ["Aplica", "No aplica"]
        },
        "caracteristicas_generales": {
            "titulo": "Características generales",
            "opciones": ["Aplica", "No aplica"]
        },
        "clases_celdas": {
            "titulo": "Clases de Celdas",
            "opciones": [
                "IM", "QM", "GBC", "DM1-A", "GAM-0", "GAM-2",
                "NSM-0", "NSM-1", "NSM-2", "NSM-3", "GAM-3"
            ],
            "tipo": "multiple"
        },
        "killin_products": {
            "titulo": "Killin products",
            "opciones": ["H-Guard", "Sistema de Testigos"]
        },
        "documentos": {
            "titulo": "Documentos",
            "opciones": ["Aplica", "No aplica"]
        },
        "pruebas_fat": {
            "titulo": "Pruebas FAT",
            "opciones": ["Aplica", "No aplica"]
        }
    }
}

class BotonOpcion(QPushButton):
    """ Boton de opcion estilizado (toggle)"""
    
    def __init__(self, texto: str,grupo:str=""):
        super().__init__(texto)
        self.seleccionado = False
        self.grupo = grupo
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.actualizar_estilo()
        
    def actualizar_estilo(self):
            