"""Ventana Principal de PROKIT"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QScrollArea, QLabel
)
import qtawesome as qta

from componentes import MenuLateral, BarraSuperior, ContenedorTarjetas, SeccionTabla


class VentanaPrincipal(QMainWindow):
    """Ventana principal que une todos los componentes"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.conectar_senales()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        self.setWindowTitle("PROKIT - Licitación de Proyectos")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # Crear componentes
        self.menu_lateral = MenuLateral()
        self.barra_superior = BarraSuperior()
        self.tarjetas = ContenedorTarjetas()
        self.seccion_tabla = SeccionTabla()
        
        # Panel de contenido
        panel_contenido = QWidget()
        panel_contenido.setStyleSheet("background-color: #FAFBFC;")
        layout_contenido = QVBoxLayout(panel_contenido)
        layout_contenido.setContentsMargins(0, 0, 0, 0)
        layout_contenido.setSpacing(0)
        
        # Agregar barra superior
        layout_contenido.addWidget(self.barra_superior)
        
        # Área con scroll
        area_scroll = QScrollArea()
        area_scroll.setWidgetResizable(True)
        area_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #FAFBFC;
                border: none;
            }
        """)
        
        # Contenido dentro del scroll
        contenido_scroll = QWidget()
        layout_scroll = QVBoxLayout(contenido_scroll)
        layout_scroll.setContentsMargins(30, 20, 30, 20)
        layout_scroll.setSpacing(15)
        
        # Breadcrumb
        contenedor_breadcrumb = QWidget()
        layout_breadcrumb = QHBoxLayout(contenedor_breadcrumb)
        layout_breadcrumb.setContentsMargins(0, 0, 0, 0)
        layout_breadcrumb.setSpacing(5)
        
        icono_bread = QLabel()
        icono_bread.setPixmap(qta.icon('fa5s.home', color='#888').pixmap(14, 14))
        texto_bread = QLabel("Inicio/")
        texto_bread.setStyleSheet("color: #888; font-size: 13px;")
        
        layout_breadcrumb.addWidget(icono_bread)
        layout_breadcrumb.addWidget(texto_bread)
        layout_breadcrumb.addStretch()
        
        layout_scroll.addWidget(contenedor_breadcrumb)
        
        # Título
        titulo = QLabel("Gestión de proyectos")
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1a1a2e;
            padding: 10px 0;
        """)
        layout_scroll.addWidget(titulo)
        
        # Tarjetas
        layout_scroll.addWidget(self.tarjetas)
        
        # Tabla
        layout_scroll.addWidget(self.seccion_tabla, 1)
        
        area_scroll.setWidget(contenido_scroll)
        layout_contenido.addWidget(area_scroll)
        
        # Agregar al layout principal
        layout_principal.addWidget(self.menu_lateral)
        layout_principal.addWidget(panel_contenido, 1)
    
    def conectar_senales(self):
        """Conecta las señales entre componentes"""
        # Botón hamburguesa toggle menú
        self.barra_superior.menu_toggle_signal.connect(self.menu_lateral.toggle)
        
        # Señales de la tabla (puedes agregar funcionalidad aquí)
        self.seccion_tabla.nuevo_proyecto_signal.connect(self.nuevo_proyecto)
        self.seccion_tabla.ver_proyecto_signal.connect(self.ver_proyecto)
        self.seccion_tabla.editar_proyecto_signal.connect(self.editar_proyecto)
        self.seccion_tabla.eliminar_proyecto_signal.connect(self.eliminar_proyecto)
    
    def nuevo_proyecto(self):
        """Acción para crear nuevo proyecto"""
        print("Crear nuevo proyecto")
    
    def ver_proyecto(self, fila: int):
        """Acción para ver proyecto"""
        print(f"Ver proyecto en fila {fila}")
    
    def editar_proyecto(self, fila: int):
        """Acción para editar proyecto"""
        print(f"Editar proyecto en fila {fila}")
    
    def eliminar_proyecto(self, fila: int):
        """Acción para eliminar proyecto"""
        print(f"Eliminar proyecto en fila {fila}")