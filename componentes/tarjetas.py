"""Componente: Tarjetas de Licitaciones"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
import qtawesome as qta


class ContenedorTarjetas(QWidget):
    """Contenedor con tarjetas de licitaciones públicas y privadas"""
    
    def __init__(self):
        super().__init__()
        self.contador_publicas = 0
        self.contador_privadas = 0
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Tarjeta 1: Licitaciones Públicas
        self.tarjeta_publicas, self.lbl_numero_publicas = self.crear_tarjeta(
            titulo="Licitaciones públicas",
            numero="0",
            color="#0065bb",
            icono='fa6s.landmark-flag'
        )
        layout.addWidget(self.tarjeta_publicas)
        
        # Tarjeta 2: Licitaciones Privadas
        self.tarjeta_privadas, self.lbl_numero_privadas = self.crear_tarjeta(
            titulo="Licitaciones privadas",
            numero="3",
            color="#00B622",
            icono='fa6s.building-columns'
        )
        layout.addWidget(self.tarjeta_privadas)
        
        layout.addStretch()
    
    def crear_tarjeta(self, titulo: str, numero: str, color: str, icono: str) -> tuple:
        """Crea una tarjeta con título, número e ícono. retorna (tarjeta, lbl_numero)"""
        tarjeta = QFrame()
        tarjeta.setFixedSize(280, 120)
        tarjeta.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
            QLabel { 
                border: none; 
            }
        """)
        
        layout = QHBoxLayout(tarjeta)
        layout.setContentsMargins(25, 10, 20, 15)
        
        # Información (título y número)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(f"""
            font-size: 16px; 
            font-family: 'Titillium Web'; 
            font-weight: semibold; 
            color: #333;
        """)
        
        lbl_numero = QLabel(numero)
        lbl_numero.setStyleSheet(f"""
            font-size: 28px; 
            font-family: 'Conthrax Bold'; 
            font-weight: bold; 
            color: {color};
        """)
        
        info_layout.addWidget(lbl_titulo)
        info_layout.addWidget(lbl_numero)
        
        # Ícono
        lbl_icono = QLabel() 
        lbl_icono.setPixmap(qta.icon(icono, color=color).pixmap(60, 60))
        lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(info_layout)
        layout.addWidget(lbl_icono)
        
        return tarjeta, lbl_numero
    
    def actualizar_contadores(self, publicas: int, privadas: int):
        self.contador_publicas = publicas
        self.contador_privadas = privadas
        self.lbl_numero_publicas.setText(str(self.contador_publicas))
        self.lbl_numero_privadas.setText(str(self.contador_privadas))
        
    def incrementar_publicas(self):
        """Incrementa el contador de licitaciones públicas"""
        self.contador_publicas += 1
        self.lbl_numero_publicas.setText(str(self.contador_publicas))
    
    def incrementar_privadas(self):
        """Incrementa el contador de licitaciones privadas"""
        self.contador_privadas += 1
        self.lbl_numero_privadas.setText(str(self.contador_privadas))     