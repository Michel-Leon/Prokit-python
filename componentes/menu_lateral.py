"""Componente: Menú Lateral"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal
import qtawesome as qta


class MenuLateral(QWidget):
    """Menú lateral con navegación principal"""
    
    def __init__(self):
        super().__init__()
        self.expandido = True
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #F5F6FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Logo
        self.logo = QLabel()
        self.logo.setText("""
            <div style="font-size: 30px; font-family: 'Conthrax Bold'; font-weight: bold; color: #0065bb;">PROKIT</div>
            <div style="font-size: 15px; font-family: 'Titillium Web'; font-weight: semibold; color: #646464;">Industrias CTS</div>
        """)
        self.logo.setStyleSheet("padding: 20px 0;")
        layout.addWidget(self.logo)
        
        # Botón Inicio
        self.btn_inicio = QPushButton("Inicio")
        self.btn_inicio.setIcon(qta.icon('fa5s.home', color='#0065bb'))
        self.btn_inicio.setStyleSheet("""
            QPushButton {
                font-family: 'Titillium Web';
                background-color: #E3F2FD;
                border: none;
                border-radius: 5px;
                padding: 12px 15px;
                text-align: left;
                font-size: 18px;
                color: #0065bb;
            }
            QPushButton:hover {
                background-color: #BBDEFB;
            }
        """)
        layout.addWidget(self.btn_inicio)
        
        # Botón Base de datos
        self.btn_base_datos = QPushButton("Base de datos")
        self.btn_base_datos.setIcon(qta.icon('fa5s.database', color='#666'))
        self.btn_base_datos.setStyleSheet("""
            QPushButton {
                font-family: 'Titillium Web';
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 12px 15px;
                text-align: left;
                font-size: 18px;
                color: #666;
            }
            QPushButton:hover {
                background-color: #E8E8E8;
            }
        """)
        layout.addWidget(self.btn_base_datos)
        
        # Sección Soporte
        self.lbl_soporte = QLabel("Soporte")
        self.lbl_soporte.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #999;
            padding: 20px 0 10px 0;
        """)
        layout.addWidget(self.lbl_soporte)
        
        self.btn_soporte = QPushButton("Solicitudes y soporte")
        self.btn_soporte.setIcon(qta.icon('fa6s.headset', color='#666'))
        self.btn_soporte.setStyleSheet("""
            QPushButton {
                font-family: 'Titillium Web';
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 12px 15px;
                text-align: left;
                font-size: 18px;
                color: #666;
            }
            QPushButton:hover {
                background-color: #E8E8E8;
            }
        """)
        layout.addWidget(self.btn_soporte)
        
        # Espacio flexible
        layout.addStretch()
        
        # Perfil de usuario
        self.perfil = QPushButton(" Admin")
        self.perfil.setIcon(qta.icon('fa5s.user-circle', color='white'))
        self.perfil.setStyleSheet("""
            QPushButton {
                font-family: 'Titillium Web';
                font-weight: bold;
                background-color: #1976D2;
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        layout.addWidget(self.perfil)
    
    def colapsar(self):
        """Colapsa el menú mostrando solo íconos"""
        self.setFixedWidth(60)
        self.btn_inicio.setText("")
        self.btn_base_datos.setText("")
        self.btn_soporte.setText("")
        self.lbl_soporte.hide()
        self.logo.hide()
        self.perfil.hide()
        self.expandido = False
    
    def expandir(self):
        """Expande el menú mostrando texto completo"""
        self.setFixedWidth(250)
        self.btn_inicio.setText("Inicio")
        self.btn_base_datos.setText("Base de datos")
        self.btn_soporte.setText("Solicitudes y soporte")
        self.lbl_soporte.show()
        self.logo.show()
        self.perfil.show()
        self.expandido = True
    
    def toggle(self):
        """Alterna entre colapsar y expandir"""
        if self.expandido:
            self.colapsar()
        else:
            self.expandir()