"""Ventana: Editor de Glosa - Integra el editor con la barra superior"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal

from componentes.barra_superior import BarraSuperior
from componentes.editor_glosa import EditorGlosa


class VentanaEditorGlosa(QMainWindow):
    """Ventana para editar documentos de tipo Glosa"""
    
    cerrar_signal = pyqtSignal()
    
    def __init__(self, datos_proyecto: dict = None, parent=None):
        super().__init__(parent)
        self.datos_proyecto = datos_proyecto or {}
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("PROKIT - Redacción de Proyecto")
        self.setGeometry(50, 50, 1400, 850)
        
        # Widget central con fondo claro
        widget_central = QWidget()
        widget_central.setStyleSheet("background-color: #FAFBFC;")
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # Barra superior
        self.barra_superior = BarraSuperior()
        layout_principal.addWidget(self.barra_superior)
        
        # Editor de Glosa (ocupa todo el espacio)
        self.editor = EditorGlosa(self.datos_proyecto)
        layout_principal.addWidget(self.editor, 1)
    
    def closeEvent(self, event):
        self.cerrar_signal.emit()
        super().closeEvent(event)