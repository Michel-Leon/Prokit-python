"""Componente: Barra Superior"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
import qtawesome as qta


class BarraSuperior(QWidget):
    """Barra superior con menú hamburguesa y acciones"""
    
    # Señal que se emite cuando se hace clic en el botón hamburguesa
    menu_toggle_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedHeight(60)
        self.setStyleSheet("background-color: #FFFFFF;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Botón menú hamburguesa
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-radius: 5px;
            }
        """)
        self.btn_menu.clicked.connect(self.menu_toggle_signal.emit)
        layout.addWidget(self.btn_menu)
        
        # Espacio flexible
        layout.addStretch()
        
        # Botón tema
        btn_tema = QPushButton()
        btn_tema.setIcon(qta.icon('fa5.moon', color='#c8c8c8'))
        btn_tema.setFixedSize(40, 40)
        btn_tema.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-radius: 20px;
            }
        """)
        layout.addWidget(btn_tema)
        
        # Botón notificaciones
        btn_notificacion = QPushButton()
        btn_notificacion.setIcon(qta.icon('fa5s.bell', color='#c8c8c8'))
        btn_notificacion.setFixedSize(40, 40)
        btn_notificacion.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-radius: 20px;
            }
        """)
        layout.addWidget(btn_notificacion)
        
        # Botón perfil
        btn_perfil = QPushButton("👤")
        btn_perfil.setFixedSize(40, 40)
        btn_perfil.setStyleSheet("""
            QPushButton {
                background-color: #FFB74D;
                border: none;
                font-size: 18px;
                border-radius: 20px;
            }
        """)
        layout.addWidget(btn_perfil)