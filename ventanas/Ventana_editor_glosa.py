"""Ventana: Editor de Glosa - Integra el editor con la barra superior y menú"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal

from componentes.barra_superior import BarraSuperior
from componentes.menu_lateral import MenuLateral
from componentes.editor_glosa import EditorGlosa


class VentanaEditorGlosa(QMainWindow):
    """Ventana para editar documentos de tipo Glosa"""
    
    cerrar_signal = pyqtSignal()
    
    def __init__(self, datos_proyecto: dict = None, parent=None):
        super().__init__(parent)
        self.datos_proyecto = datos_proyecto or {}
        self.setup_ui()
        self.conectar_senales()
    
    def setup_ui(self):
        self.setWindowTitle("PROKIT - Redacción de Proyecto")
        self.setGeometry(50, 50, 1400, 850)
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # Menú lateral
        self.menu_lateral = MenuLateral()
        
        # Panel de contenido
        panel_contenido = QWidget()
        panel_contenido.setStyleSheet("background-color: #FAFBFC;")
        layout_contenido = QVBoxLayout(panel_contenido)
        layout_contenido.setContentsMargins(0, 0, 0, 0)
        layout_contenido.setSpacing(0)
        
        # Barra superior
        self.barra_superior = BarraSuperior()
        layout_contenido.addWidget(self.barra_superior)
        
        # Editor de Glosa
        self.editor = EditorGlosa(self.datos_proyecto)
        layout_contenido.addWidget(self.editor, 1)
        
        # Agregar al layout principal
        layout_principal.addWidget(self.menu_lateral)
        layout_principal.addWidget(panel_contenido, 1)
    
    def conectar_senales(self):
        self.barra_superior.menu_toggle_signal.connect(self.menu_lateral.toggle)
    
    def closeEvent(self, event):
        self.cerrar_signal.emit()
        super().closeEvent(event)