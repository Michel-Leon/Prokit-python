"""Ventana Principal de PROKIT"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QScrollArea, QLabel
)
import qtawesome as qta

from componentes import (
    MenuLateral, BarraSuperior, ContenedorTarjetas, 
    SeccionTabla, DialogoNuevoProyecto, TarjetaProyecto
)


class VentanaPrincipal(QMainWindow):
    """Ventana principal que une todos los componentes"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.conectar_senales()
        self.actualizar_contadores()
    
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
        self.contenido_scroll = QWidget()
        self.layout_scroll = QVBoxLayout(self.contenido_scroll)
        self.layout_scroll.setContentsMargins(30, 20, 30, 20)
        self.layout_scroll.setSpacing(15)
        
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
        
        self.layout_scroll.addWidget(contenedor_breadcrumb)
        
        # Título
        titulo = QLabel("Gestión de proyectos")
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1a1a2e;
            padding: 10px 0;
        """)
        self.layout_scroll.addWidget(titulo)
        
        # Contenedor para la tarjeta del proyecto (inicialmente vacío)
        #self.contenedor_tarjeta = QWidget()
        #self.layout_tarjeta = QVBoxLayout(self.contenedor_tarjeta)
        #self.layout_tarjeta.setContentsMargins(0, 0, 0, 0)
        #self.layout_scroll.addWidget(self.contenedor_tarjeta)
        
        # Tarjetas de estadísticas
        self.layout_scroll.addWidget(self.tarjetas)
        
        # Tabla
        self.layout_scroll.addWidget(self.seccion_tabla, 1)
        
        area_scroll.setWidget(self.contenido_scroll)
        layout_contenido.addWidget(area_scroll)
        
        # Agregar al layout principal
        layout_principal.addWidget(self.menu_lateral)
        layout_principal.addWidget(panel_contenido, 1)
    
    def conectar_senales(self):
        """Conecta las señales entre componentes"""
        # Botón hamburguesa toggle menú
        self.barra_superior.menu_toggle_signal.connect(self.menu_lateral.toggle)
        
        # Señales de la tabla
        self.seccion_tabla.nuevo_proyecto_signal.connect(self.abrir_dialogo_nuevo_proyecto)
        self.seccion_tabla.ver_proyecto_signal.connect(self.mostrar_tarjeta_proyecto)
        self.seccion_tabla.eliminar_proyecto_signal.connect(self.eliminar_proyecto)
    
    def actualizar_contadores(self):
        """Actualiza los contadores de las tarjetas"""
        publicas, privadas = self.seccion_tabla.contar_por_tipo()
        self.tarjetas.actualizar_contadores(publicas, privadas)
    
    def abrir_dialogo_nuevo_proyecto(self):
        """Abre el diálogo para crear nuevo proyecto"""
        from componentes import DialogoNuevoProyecto
        
        dialogo = DialogoNuevoProyecto(self)
        dialogo.proyecto_creado.connect(self.agregar_nuevo_proyecto)
        dialogo.exec()
    
    def agregar_nuevo_proyecto(self, datos: dict):
        """Agrega el nuevo proyecto a la tabla y actualiza contadores"""
        self.seccion_tabla.agregar_proyecto(datos)
        self.actualizar_contadores()
        print(f"Proyecto creado: {datos['nombre']}")
    
    def mostrar_tarjeta_proyecto(self, fila: int):
        """Muestra la tarjeta del proyecto como diálogo"""
        # Obtener datos del proyecto
        datos = self.seccion_tabla.obtener_proyecto(fila)
    
        if datos:
            # Crear y mostrar diálogo
            dialogo = TarjetaProyecto(datos, self)
            
            # Conectar señales
            dialogo.nuevo_documento_signal.connect(
                lambda: self.nuevo_documento(fila)
            )
            dialogo.editar_documento_signal.connect(
                lambda doc_fila: self.editar_documento(fila, doc_fila)
            )
            dialogo.descargar_documento_signal.connect(
                lambda doc_fila: self.descargar_documento(fila, doc_fila)
            )
            
            # Mostrar diálogo
            dialogo.exec()
    
    def nuevo_documento(self, fila_proyecto: int):
        """Abre diálogo para crear nuevo documento"""
        print(f"Crear nuevo documento para proyecto en fila {fila_proyecto}")
        # Aquí puedes abrir un diálogo para crear documento
    
    def editar_documento(self, fila_proyecto: int, fila_documento: int):
        """Abre el editor según el tipo de documento"""
        datos = self.seccion_tabla.obtener_proyecto(fila_proyecto)
        
        if datos:
            from ventanas.ventana_editor_glosa import VentanaEditorGlosa
            self.ventana_editor = VentanaEditorGlosa(datos, self)
            self.ventana_editor.show()
    
    def descargar_documento(self, fila_proyecto: int, fila_documento: int):
        """Descarga el documento"""
        print(f"Descargar documento {fila_documento} del proyecto {fila_proyecto}")
        # Aquí puedes implementar la descarga
    
    def eliminar_proyecto(self, fila: int):
        """Acción para eliminar proyecto"""
        # Cerrar tarjeta si está abierta
        self.cerrar_tarjeta_proyecto()
        
        # Eliminar de la lista y tabla
        if 0 <= fila < len(self.seccion_tabla.proyectos):
            self.seccion_tabla.proyectos.pop(fila)
        self.seccion_tabla.tabla.removeRow(fila)
        
        self.actualizar_contadores()
        print(f"Proyecto eliminado de fila {fila}")