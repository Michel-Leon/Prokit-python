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
        if self.seleccionado:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0065bb;
                    color: white;
                    border: none;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 12px;
                    font-family: 'Titillium Web';
                    font-weight: bold;
                }      
        """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    color: #333;
                    border: 1px solid #E0E0E0;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 12px;
                    font-family: 'Titillium Web';
                    font-weight: bold;
                }
                QPushButton:hover {
                    border-color: #0065bb;
                    color: #0065bb;
                }
                               """)    
    def set_seleccionado(self,estado:bool):
        self.seleccionado = estado
        self.actualizar_estilo()

class  CheckBoxOpcion(QWidget):
    """Checkox estilizado para seleccion multiple""" 
    
    seleccion_cambio = pyqtSignal(str, bool)
    
    def __init__(self,texto:str):
        super().__init__()
        self.texto = texto
        self.seleccionado = False
        
        layout= QHBoxLayout(self)
        layout.setContentsMargins(0,2,10,2)
        layout.setSpacing(5)
        
        self.check = QLabel("☐")
        self.check.setFixedHeight(18)
        self.check.setStyleSheet("font-size: 14px; color: #666;") 
        
        self.label = QLabel(texto)
        self.label.setStyleSheet("""font-size: 12px;
                                 color: #333;
                                 font-family: 'Titillium Web';
        """)
        
        layout.addwidget(self.check)
        layout.addWidget(self.label)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def mousePressEvent(self, event):
        self.seleccionado = not self.seleccionado
        if self.seleccionado:
            self.check.setText("☑")
            self.check.setStyleSheet("font-size: 14px; color: #0065bb; font-weight: bold;") 
        else:
            self.check.setText("☐")
            self.check.setStyleSheet("font-size: 14px; color: #666;") 
        self.seleccion_cambio.emit(self.texto, self.seleccionado)
        
class SeccionCaracteristicas(QWidget):
    """Una seccin dentro del panel de contenido (EJ: Tipo de celda)""" 
    
    seleccion_hecha = pyqtSignal(str,str,str) #seccion campo valor
    
    def __init__(self, titulo:str,opciones:list, tipo:str="simple"): 
        super().__init__()
        self.titulo = titulo
        self.opciones = opciones
        self.tipo = tipo
        self.botones = []
        self.checks = []
        self.valor_seleccionado = ""
        self.valores_multiples = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,5,0,5)  
        layout.setSpacing(5)
        
        # TITULO CON ICONO +          
     
            
            