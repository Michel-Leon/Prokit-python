"""Componente: Tarjeta expandible del proyecto"""

from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QAction
import qtawesome as qta


class TarjetaProyecto(QDialog):
    """Tarjeta expandible que muestra los detalles de un proyecto"""
    
    # Señales
    nuevo_documento_signal = pyqtSignal(dict)
    descargar_documento_signal = pyqtSignal(int)
    editar_documento_signal = pyqtSignal(int)
    
    def __init__(self, datos_proyecto: dict, parent=None):
        super().__init__(parent)
        self.datos = datos_proyecto
        self.documentos = list(self.datos.get('documentos', []))
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Tarjeta del proyecto")
        self.setFixedSize(720, 520)
        
        # Eliminar barra de título del sistema
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        
        # Hacer el fondo transparente para que se vea la sombra
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Layout principal del diálogo
        layout_dialogo = QVBoxLayout(self)
        layout_dialogo.setContentsMargins(15, 15, 15, 15)
        
        # Contenedor principal con sombra
        contenedor_principal = QFrame()
        contenedor_principal.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
        """)
        
        # Aplicar sombra al contenedor
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setColor(QColor(0, 0, 0, 80))
        sombra.setOffset(0, 5)
        contenedor_principal.setGraphicsEffect(sombra)
        
        layout_principal = QVBoxLayout(contenedor_principal)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # ====== ENCABEZADO AZUL ======
        encabezado = QFrame()
        encabezado.setFixedHeight(50)
        encabezado.setStyleSheet("""
            QFrame {
                background-color: #0065bb;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        
        layout_encabezado = QHBoxLayout(encabezado)
        layout_encabezado.setContentsMargins(20, 0, 20, 0)
        
        titulo = QLabel("Tarjeta del proyecto")
        titulo.setStyleSheet("""
            font-size: 16px;
            font-family: 'Titillium Web';
            font-weight: bold;
            color: white;
        """)
        
        btn_cerrar = QPushButton("✕")
        btn_cerrar.setFixedSize(30, 30)
        btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        
        layout_encabezado.addWidget(titulo)
        layout_encabezado.addStretch()
        layout_encabezado.addWidget(btn_cerrar)
        
        layout_principal.addWidget(encabezado)
        
        # ====== CONTENIDO ======
        contenido = QWidget()
        contenido.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        """)
        layout_contenido = QVBoxLayout(contenido)
        layout_contenido.setContentsMargins(25, 25, 25, 25)
        layout_contenido.setSpacing(15)
        
        # ====== INFORMACIÓN DEL PROYECTO (2 columnas) ======
        info_widget = QWidget()
        layout_info = QHBoxLayout(info_widget)
        layout_info.setContentsMargins(0, 0, 0, 0)
        layout_info.setSpacing(40)
        
        # Columna izquierda
        col_izq = QVBoxLayout()
        col_izq.setSpacing(10)
        col_izq.addLayout(self._crear_campo("Nombre del proyecto:", self.datos.get('nombre', '')))
        col_izq.addLayout(self._crear_campo("Nombre de la empresa:", self.datos.get('empresa', '')))
        col_izq.addLayout(self._crear_campo("Tipo de licitación:", self.datos.get('tipo_licitacion', '')))
        col_izq.addLayout(self._crear_campo("Tipo de especificación:", self.datos.get('tipo_especificacion', '')))
        
        # Columna derecha
        col_der = QVBoxLayout()
        col_der.setSpacing(10)
        col_der.addLayout(self._crear_campo("Nombre del comercial:", self.datos.get('comercial', '')))
        col_der.addLayout(self._crear_campo("Número de CRM:", self.datos.get('crm', '')))
        col_der.addLayout(self._crear_campo("Fecha de inicio:", self.datos.get('fecha', '')))
        col_der.addStretch()
        
        layout_info.addLayout(col_izq)
        layout_info.addLayout(col_der)
        layout_info.addStretch()
        
        layout_contenido.addWidget(info_widget)
        
        # ====== BOTÓN NUEVO DOCUMENTO CON MENÚ ======
        contenedor_btn = QWidget()
        layout_btn = QHBoxLayout(contenedor_btn)
        layout_btn.setContentsMargins(0, 0, 0, 0)
        layout_btn.addStretch()
        
        self.btn_nuevo_doc = QPushButton("  Nuevo documento")
        self.btn_nuevo_doc.setIcon(qta.icon('fa5s.plus-circle', color='#0065bb'))
        self.btn_nuevo_doc.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nuevo_doc.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #0065bb;
                border: none;
                font-size: 13px;
                font-family: 'Titillium Web';
                padding: 5px 10px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.btn_nuevo_doc.clicked.connect(self._mostrar_menu_documento)
        
        layout_btn.addWidget(self.btn_nuevo_doc)
        layout_contenido.addWidget(contenedor_btn)
        
        # ====== TABLA DE DOCUMENTOS ======
        self.tabla_documentos = self._crear_tabla_documentos()
        layout_contenido.addWidget(self.tabla_documentos)
        
        layout_contenido.addStretch()
        
        layout_principal.addWidget(contenido)
        
        # Agregar contenedor al diálogo
        layout_dialogo.addWidget(contenedor_principal)
    
    # ====== MENÚ DESPLEGABLE NUEVO DOCUMENTO ======
    def _mostrar_menu_documento(self):
        """Muestra el menú desplegable para seleccionar tipo de documento"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
                font-family: 'Titillium Web';
                font-size: 13px;
            }
            QMenu::item {
                padding: 10px 30px;
                color: #333;
            }
            QMenu::item:hover {
                background-color: #E3F2FD;
                color: #0065bb;
            }
            QMenu::separator {
                height: 1px;
                background-color: #E0E0E0;
                margin: 3px 10px;
            }
        """)
        
        # Opción Glosa
        accion_glosa = QAction("Glosa", self)
        accion_glosa.triggered.connect(lambda: self._crear_nuevo_documento("Glosa", ".docx"))
        menu.addAction(accion_glosa)
        
        # Separador
        menu.addSeparator()
        
        # Opción RPP
        accion_rpp = QAction("RPP", self)
        accion_rpp.triggered.connect(lambda: self._crear_nuevo_documento("RPP", ".xls"))
        menu.addAction(accion_rpp)
        
        # Mostrar el menú debajo del botón
        pos = self.btn_nuevo_doc.mapToGlobal(self.btn_nuevo_doc.rect().bottomLeft())
        menu.exec(pos)
    
    def _obtener_siguiente_version(self, tipo: str) -> int:
        """Calcula la siguiente versión para un tipo de documento"""
        version_max = 0
        
        for doc in self.documentos:
            if doc.get('tipo', '').lower() == tipo.lower():
                version_actual = int(doc.get('version', 0))
                if version_actual > version_max:
                    version_max = version_actual
        
        return version_max + 1
    
    def _crear_nuevo_documento(self, tipo: str, formato: str):
        """Crea un nuevo documento con versionamiento automático"""
        # Obtener la siguiente versión
        nueva_version = self._obtener_siguiente_version(tipo)
        
        # Crear el documento
        nuevo_doc = {
            "tipo": tipo,
            "formato": formato,
            "version": str(nueva_version)
        }
        
        # Agregar a la lista interna
        self.documentos.append(nuevo_doc)
        
        # Agregar a la tabla visual
        fila = self.tabla_documentos.rowCount()
        self.tabla_documentos.insertRow(fila)
        
        self.tabla_documentos.setItem(fila, 0, QTableWidgetItem(tipo))
        self.tabla_documentos.setItem(fila, 1, QTableWidgetItem(formato))
        
        item_version = QTableWidgetItem(str(nueva_version))
        item_version.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabla_documentos.setItem(fila, 2, item_version)
        
        self.tabla_documentos.setCellWidget(fila, 3, self._crear_botones_acciones(fila))
        
        # Emitir señal con los datos del nuevo documento
        self.nuevo_documento_signal.emit(nuevo_doc)
        
        print(f"Documento creado: {tipo} - Versión {nueva_version}")
    
    # ====== MÉTODOS DE UI ======
    def _crear_campo(self, etiqueta: str, valor: str) -> QHBoxLayout:
        """Crea un campo con etiqueta y valor"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        lbl_etiqueta = QLabel(etiqueta)
        lbl_etiqueta.setStyleSheet("""
            color: #666;
            font-size: 13px;
            font-family: 'Titillium Web';
        """)
        lbl_etiqueta.setFixedWidth(160)
        
        lbl_valor = QLabel(valor if valor else "—")
        lbl_valor.setStyleSheet("""
            color: #333;
            font-size: 13px;
            font-family: 'Titillium Web';
            font-weight: bold;
        """)
        
        layout.addWidget(lbl_etiqueta)
        layout.addWidget(lbl_valor)
        layout.addStretch()
        
        return layout
    
    def _crear_tabla_documentos(self) -> QTableWidget:
        """Crea la tabla de documentos"""
        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels([
            "Tipo de documento", "Formato del documento", "Versión", "Acciones"
        ])
        
        tabla.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #F0F0F0;
                font-size: 13px;
                font-family: 'Titillium Web';
            }
            QHeaderView::section {
                background-color: transparent;
                color: #0065bb;
                font-weight: bold;
                font-size: 13px;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                text-decoration: underline;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
                color: #333;
            }
            QTableWidget::item:selected {
                background-color: #F2F2F2;
                color: #333;
            }
        """)
        
        # Configurar columnas
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        tabla.setColumnWidth(3, 100)
        
        # Ocultar números de fila
        tabla.verticalHeader().setVisible(False)
        tabla.verticalHeader().setDefaultSectionSize(45)
        
        # Configuraciones
        tabla.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabla.setMaximumHeight(200)
        
        # Cargar documentos existentes
        self._cargar_documentos(tabla)
        
        return tabla
    
    def _cargar_documentos(self, tabla: QTableWidget):
        """Carga los documentos del proyecto en la tabla"""
        if not self.documentos:
            tabla.setRowCount(0)
            return
        
        tabla.setRowCount(len(self.documentos))
        
        for fila, doc in enumerate(self.documentos):
            tabla.setItem(fila, 0, QTableWidgetItem(doc.get('tipo', '')))
            tabla.setItem(fila, 1, QTableWidgetItem(doc.get('formato', '')))
            
            # Versión centrada
            item_version = QTableWidgetItem(str(doc.get('version', '1')))
            item_version.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila, 2, item_version)
            
            # Botones de acciones
            tabla.setCellWidget(fila, 3, self._crear_botones_acciones(fila))
    
    def _crear_botones_acciones(self, fila: int) -> QWidget:
        """Crea los botones de acciones para un documento"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        estilo_btn = """
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-radius: 5px;
            }
        """
        
        # Botón descargar
        btn_descargar = QPushButton()
        btn_descargar.setIcon(qta.icon('fa5s.download', color='#666'))
        btn_descargar.setFixedSize(30, 30)
        btn_descargar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_descargar.setStyleSheet(estilo_btn)
        btn_descargar.setToolTip("Descargar documento")
        btn_descargar.clicked.connect(lambda: self.descargar_documento_signal.emit(fila))
        
        # Botón editar
        btn_editar = QPushButton()
        btn_editar.setIcon(qta.icon('fa5s.edit', color='#0065bb'))
        btn_editar.setFixedSize(30, 30)
        btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_editar.setStyleSheet(estilo_btn)
        btn_editar.setToolTip("Editar documento")
        btn_editar.clicked.connect(lambda: self.editar_documento_signal.emit(fila))
        
        layout.addWidget(btn_descargar)
        layout.addWidget(btn_editar)
        
        return widget