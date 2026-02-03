"""Componente: Sección de Tabla de Proyectos"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
    QPushButton, QLineEdit, QComboBox, QTableWidget, 
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta


class SeccionTabla(QFrame):
    """Sección completa con tabla de proyectos, búsqueda y filtros"""
    
    # Señales para comunicar acciones
    nuevo_proyecto_signal = pyqtSignal()
    ver_proyecto_signal = pyqtSignal(int)
    editar_proyecto_signal = pyqtSignal(int)
    eliminar_proyecto_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.proyectos = []
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Encabezado
        layout.addWidget(self.crear_encabezado())
        
        # Barra de búsqueda
        layout.addWidget(self.crear_barra_busqueda())
        
        # Tabla
        self.tabla = self.crear_tabla()
        layout.addWidget(self.tabla)
        
        # Cargar datos de ejemplo
        self.cargar_datos_ejemplo()
    
    def crear_encabezado(self) -> QWidget:
        """Crea el encabezado con título y botón nuevo proyecto"""
        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        titulo = QLabel("Proyectos creados")
        titulo.setStyleSheet("""
            font-size: 25px;
            font-family: 'Titillium Web';
            font-weight: semibold;
            color: #333;
            border: none;
        """)
        
        btn_nuevo = QPushButton("Nuevo proyecto")
        btn_nuevo.setIcon(qta.icon('fa5s.plus', color='white'))
        btn_nuevo.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_nuevo.setStyleSheet("""
            QPushButton {
                background-color: #0065bb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-family: 'Titillium Web';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0053a6;
            }
            QPushButton:pressed {
                background-color: #00438c;
            }
        """)
        btn_nuevo.clicked.connect(self.nuevo_proyecto_signal.emit)
        
        layout.addWidget(titulo)
        layout.addStretch()
        layout.addWidget(btn_nuevo)
        
        return widget
    
    def crear_barra_busqueda(self) -> QWidget:
        """Crea la barra de búsqueda y filtros"""
        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Input de búsqueda
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar proyecto...")
        self.input_busqueda.addAction(
            qta.icon('fa5s.search', color='#888'), 
            QLineEdit.ActionPosition.LeadingPosition
        )
        self.input_busqueda.setFixedHeight(35)
        self.input_busqueda.setFixedWidth(500)
        self.input_busqueda.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding-left: 30px;
                padding-right: 10px;
                color: #333;
                font-size: 14px;
                font-family: 'Titillium Web';
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QLineEdit:focus {
                border: 1px solid #0065bb;
            }
        """)
        
        # ComboBox de filtro
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems([
            "Todos los proyectos", 
            "Licitaciones públicas", 
            "Licitaciones privadas"
        ])
        self.combo_filtro.setFixedHeight(35)
        self.combo_filtro.setFixedWidth(250)
        self.combo_filtro.setStyleSheet("""
            QComboBox {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
                font-family: 'Titillium Web';
                background-color: #FAFBFC;
                color: #333;
            }
            QComboBox:focus {
                border: 1px solid #0065bb;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                subcontrol-position: right center;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #666;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: #333;
                selection-background-color: #E3F2FD;
                selection-color: #0065bb;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 15px;
                min-height: 30px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F5F5F5;
            }
        """)
        
        layout.addWidget(self.input_busqueda)
        layout.addWidget(self.combo_filtro)
        layout.addStretch()
        
        return widget
    
    def crear_tabla(self) -> QTableWidget:
        """Crea y configura la tabla de proyectos"""
        tabla = QTableWidget()
        tabla.setColumnCount(5)
        tabla.setHorizontalHeaderLabels([
            "Nombre", "Empresa", "Tipo de Licitación / Especificación", 
            "Último acceso", "Acciones"
        ])
        
        tabla.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #F0F0F0;
                font-size: 14px;
                font-family: 'Titillium Web';
                alternate-background-color: #FAFBFC;
            }
            QHeaderView::section {
                background-color: #FAFBFC;
                color: #666;
                font-weight: bold;
                font-size: 13px;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
                color: #333;
            }
            QTableWidget::item:selected {
                background-color: #F2F2F2;
                color: #333;
            }
            QScrollBar:vertical {
                background-color: #F5F5F5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        
        # Configurar columnas
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        tabla.setColumnWidth(4, 120)
        
        # Configuración adicional
        tabla.verticalHeader().setVisible(False)
        tabla.verticalHeader().setDefaultSectionSize(50)
        tabla.setMinimumHeight(300)
        tabla.setAlternatingRowColors(True)
        tabla.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        return tabla
    
    def crear_botones_acciones(self, fila: int) -> QWidget:
        """Crea los botones de acciones para una fila"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        estilo_boton = """
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """
        
        btn_ver = QPushButton()
        btn_ver.setIcon(qta.icon("ei.eye-open", color="#0065bb"))
        btn_ver.setFixedSize(30, 30)
        btn_ver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ver.setStyleSheet(estilo_boton)
        btn_ver.clicked.connect(lambda: self.ver_proyecto_signal.emit(fila))
        
        #btn_editar = QPushButton()
        #btn_editar.setIcon(qta.icon("fa5.edit", color="#0065bb"))
        #btn_editar.setFixedSize(30, 30)
        #btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
        #btn_editar.setStyleSheet(estilo_boton)
        #btn_editar.clicked.connect(lambda: self.editar_proyecto_signal.emit(fila))
        
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(qta.icon('fa6s.trash-can', color='#FA896B'))
        btn_eliminar.setFixedSize(30, 30)
        btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eliminar.setStyleSheet(estilo_boton)
        btn_eliminar.clicked.connect(lambda: self.eliminar_proyecto_signal.emit(fila))
        
        layout.addWidget(btn_ver)
        #layout.addWidget(btn_editar)
        layout.addWidget(btn_eliminar)
        
        return widget
    
    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo en la tabla"""
        datos_ejemplo = [
            {
                "nombre": "T-power",
                "empresa": "Hocol",
                "comercial": "Juan Pérez",
                "crm": "0021",
                "tipo_licitacion": "Pública",
                "tipo_especificacion": "Básica",
                "tipo_completo": "Pública/Básica",
                "fecha": "23/01/2026",
                "documentos": [
                    {"tipo": "Glosa", "formato": ".docx", "version": "1"},
                ]
            },
            {
                "nombre": "G-Flex",
                "empresa": "CTS",
                "comercial": "María García",
                "crm": "0022",
                "tipo_licitacion": "Privada",
                "tipo_especificacion": "Premium",
                "tipo_completo": "Privada/Premium",
                "fecha": "23/01/2026",
                "documentos": []
            },
            {
                "nombre": "BlokSeT",
                "empresa": "EcoPetrol",
                "comercial": "Carlos López",
                "crm": "0023",
                "tipo_licitacion": "Pública",
                "tipo_especificacion": "Premium",
                "tipo_completo": "Pública/Premium",
                "fecha": "23/01/2026",
                "documentos": [
                    {"tipo": "RPP", "formato": ".xls", "version": "1"},
                ]
            },
        ]
        
        for datos in datos_ejemplo:
            self.agregar_proyecto(datos)
        
    def agregar_proyecto(self, datos:dict):
        """Agregar un nuevo proyecto a la tabla""" 
        # Guardar datos completos
        self.proyectos.append(datos)
        
        fila = self.tabla.rowCount()
        self.tabla.insertRow(fila)
        
        self.tabla.setItem(fila, 0, QTableWidgetItem(datos["nombre"]))
        self.tabla.setItem(fila, 1, QTableWidgetItem(datos["empresa"]))
        self.tabla.setItem(fila, 2, QTableWidgetItem(datos["tipo_completo"]))
        self.tabla.setItem(fila, 3, QTableWidgetItem(datos["fecha"]))
        self.tabla.setCellWidget(fila, 4, self.crear_botones_acciones(fila))
    
    def obtener_proyecto(self, fila: int) -> dict:
        """Obtiene los datos completos de un proyecto por su fila"""
        if 0 <= fila < len(self.proyectos):
            return self.proyectos[fila]
        return {}
    
    def contar_por_tipo(self) -> tuple:
        """Cuenta proyectos publicos y privados. Retorna (publicas, Privadas)"""   
        publicas = 0
        privadas = 0
        
        for fila in range(self.tabla.rowCount()):
            item = self.tabla.item(fila, 2)
            if item:
                tipo = item.text().lower()
                if "pública" in tipo:
                    publicas += 1
                elif "privada" in tipo:
                    privadas += 1
        return publicas, privadas        