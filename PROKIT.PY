import sys
from typing import Self
import qtawesome as qta

from PyQt6.QtWidgets import(
   QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame,QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
) 

from PyQt6.QtCore import Qt


class VentanaPrincipal(QMainWindow):
    def __init__(self): # contructor donde configuramos la ventana
        super().__init__() # llama al contructor de la clase base QMainWindow
        
        #Estado del menu ( Expandido o colapsado)
        self.menu_expandido = True
        
        
        #Configuracion basica de la ventana
        self.setWindowTitle("PROKIT - Licitación de Proyectos")
        self.setGeometry(100,100,1000,1080) # x, y, width, height
        
        # windget central (contenedor prinicipal)
        widget_central = QWidget()
        self.setCentralWidget(widget_central)  
        
        # Layout horizontal para dividir: menu || contenido
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0,0,0,0) # eliminar margenes del layout principal
        layout_principal.setSpacing(0) # eliminar espacios entre widgets del layout principal
       
        
        #Pnel Izquierdo (menulateral)
        self.menu_lateral = QWidget()
        self.menu_lateral.setFixedWidth(250) # ancho fijo del menu lateral
        self.menu_lateral.setStyleSheet("background-color: #F5F6FA;") # color de fondo del menu lateral
         
        # Layout vertical para el menu lateral
        layout_menu = QVBoxLayout(self.menu_lateral)
        layout_menu.setContentsMargins(15,15,15,15) # margenes del layout del menu lateral
        layout_menu.setSpacing(5) # espacio entre widgets del menu lateral
        
        #1. Logo
        self.logo = QLabel()
        self.logo.setText("""
            <div style="font-size: 30px; font-family: 'Conthrax Bold'; font-weight: bold; color: #0065bb;">PROKIT</div>
            <div style="font-size: 15px; font-family: 'titillium web'; font-weight: semibold; color: #646464;">Industrias CTS</div>
        """)
        self.logo.setStyleSheet("padding: 20px 0;")
        layout_menu.addWidget(self.logo)

        # 2. Boton inicio
        self.btn_inicio = QPushButton("Inicio")
        self.btn_inicio.setIcon(qta.icon('fa5s.home', color='#0065bb'))
        self.btn_inicio.setStyleSheet("""
                                 
                                 QPushButton {
                                        font-family: 'titillium web';
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
        
        layout_menu.addWidget(self.btn_inicio)
        
        # 3. Botón Base de datos
        self.btn_base_datos = QPushButton("Base de datos")
        self.btn_base_datos.setIcon(qta.icon('fa5s.database', color='#666'))
        self.btn_base_datos.setStyleSheet("""
            QPushButton {
                font-family: 'titillium web';
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
        layout_menu.addWidget(self.btn_base_datos)
        
        # 4. Sección Soporte
        self.lbl_soporte = QLabel("Soporte")
        self.lbl_soporte.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #999;
            padding: 20px 0 10px 0;
        """)
        layout_menu.addWidget(self.lbl_soporte)
        
        self.btn_soporte = QPushButton("Solicitudes y soporte")
        self.btn_soporte.setIcon(qta.icon('fa6s.headset', color='#666'))
        self.btn_soporte.setStyleSheet("""
            QPushButton {
                font-family: 'titillium web';
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
        layout_menu.addWidget(self.btn_soporte)
        
        # Espacio flexible (empuja el perfil hacia abajo)
        layout_menu.addStretch()
        
        # 5. Perfil de usuario (abajo)
        self.perfil = QPushButton(" Admin")
        self.perfil.setIcon(qta.icon('fa5s.user-circle', color='white'))
        self.perfil.setStyleSheet("""
            font-family: 'titillium web';
            font-weight: semibold;
            background-color: #1976D2;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 15px;
        """)
        layout_menu.addWidget(self.perfil)
        
        # === PANEL CONTENIDO =================================================================================================================================
        self.contenido = QWidget()
        self.contenido.setStyleSheet("background-color: #FAFBFC;")
        
        # Layout vertical para organizar el contenido
        layout_contenido = QVBoxLayout(self.contenido)
        layout_contenido.setContentsMargins(0,0,0,0) # margenes del layout del contenido
        layout_contenido.setSpacing(0) # espacio entre widgets del contenido
        
        # ---- 1.BARRA SUPERIOR ----
        barra_superior = QWidget()
        barra_superior.setFixedHeight(60)
        barra_superior.setStyleSheet("background-color: #FFFFFF")
        
        layout_barra = QHBoxLayout(barra_superior)
        layout_barra.setContentsMargins(20, 10, 20, 10)
        
        #Boton menu Haburguesa
        btn_menu = QPushButton("☰")
        btn_menu.setFixedSize(40,40)
        btn_menu.setStyleSheet("""
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
        btn_menu.clicked.connect(self.toggle_menu)  # Conectar al método toggle_menu
        layout_barra.addWidget(btn_menu)
        
        # espacio flexible (empuja los iconos a la derecha)
        
        layout_barra.addStretch()
        
        # Icono de la derecha
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
        
        layout_barra.addWidget(btn_tema)
        layout_barra.addWidget(btn_notificacion)
        layout_barra.addWidget(btn_perfil)
        
        layout_contenido.addWidget(barra_superior)
        
        
        #--------------2. Area principal (con scroll) -----------------
        area_scroll = QScrollArea()
        area_scroll.setWidgetResizable(True)
        area_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #FAFBFC;
                border: none;
            }
        """)
        
        # Widget dentro del scroll
        contenido_principal = QWidget()
        layout_contenido_scroll = QVBoxLayout(contenido_principal)  # Nombre diferente
        layout_contenido_scroll.setContentsMargins(30, 20, 30, 20)
        layout_contenido_scroll.setSpacing(15)
        
        # Breadcrumb (ícono + texto)
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
        
        layout_contenido_scroll.addWidget(contenedor_breadcrumb)
        
        # Título en el contenido principal
        titulo = QLabel("Gestión de proyectos")
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1a1a2e;
            padding: 10px 0;
        """)
        
        # Agregar títulos
        layout_contenido_scroll.addWidget(titulo)
        
        # --------------- 3. Tarjetas
        contenedor_tarjetas = QWidget()
        layout_tarjetas = QHBoxLayout(contenedor_tarjetas)
        layout_tarjetas.setContentsMargins(0, 0, 0, 0)
        layout_tarjetas.setSpacing(20)
        
        # TARJETA 1: LICITACIONES PUBLICAS
        tarjeta1 = QFrame()
        tarjeta1.setFixedSize(280,120)
        tarjeta1.setStyleSheet("""
                               QFrame {
                                      background-color: #FFFFFF;
                                      border: 1px solid #E0E0E0;
                                    border-radius: 10px;
                                 }
                                 QLabel { border: none; }
                               """)
        layout_tarjeta1 = QHBoxLayout(tarjeta1) # layout interno de la tarjeta 1
        layout_tarjeta1.setContentsMargins(25, 10, 20, 15) # margenes del layout_tarjeta1
        
        # primero el texto (izquierda)
        info_tarjeta1 = QVBoxLayout()
        info_tarjeta1.setSpacing(5) # espacio entre titulo y numero
        info_tarjeta1.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Centrar verticalmente
        
        lbl_titulo1 = QLabel("Licitaciones públicas")
        lbl_titulo1.setStyleSheet("font-size: 16px; font-family: titillium web; font-weight: semibold; color: #333; border: none;")
        lbl_numero1 = QLabel("7")
        lbl_numero1.setStyleSheet("font-size: 28px; font-family: 'Conthrax Bold'; font-weight: bold; color: #0065bb; border: none;")
        info_tarjeta1.addWidget(lbl_titulo1)
        info_tarjeta1.addWidget(lbl_numero1)
        
        icono_tarjeta1 = QLabel()
        icono_tarjeta1.setPixmap(qta.icon('fa6s.people-roof', color='#0065bb').pixmap(60, 60))
        icono_tarjeta1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
         #Orden: texto izquierda, espacio, ícono derecha
        layout_tarjeta1.addLayout(info_tarjeta1)
        layout_tarjeta1.addWidget(icono_tarjeta1)
        
        # TARJETA 2: Licitaciones privadas
        tarjeta2 = QFrame()
        tarjeta2.setFixedSize(280,120)
        tarjeta2.setStyleSheet("""
                               QFrame {
                                        background-color: #FFFFFF;
                                        border: 1px solid #E0E0E0;
                                        border-radius: 10px;
                               }
                               QLabel { border: none; }
                               
                               """)
        layout_tarjeta2 = QHBoxLayout(tarjeta2) # layout interno de la tarjeta 2
        layout_tarjeta2.setContentsMargins(25, 10, 20, 15) # margenes del layout_tarjeta2
        info_tarjeta2 = QVBoxLayout()
        info_tarjeta2.setSpacing(5) # espacio entre titulo y numero
        info_tarjeta2.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Centrar verticalmente
        lbl_titulo2 = QLabel("Licitaciones privadas")
        lbl_titulo2.setStyleSheet("font-size: 16px; font-family: titillium web; font-weight: semibold; color: #333; border: none;")
        lbl_numero2 = QLabel("3")
        lbl_numero2.setStyleSheet("font-size: 28px; font-family: 'Conthrax Bold'; font-weight: bold; color: #00B622; border: none;")
        info_tarjeta2.addWidget(lbl_titulo2)
        info_tarjeta2.addWidget(lbl_numero2)
        
        icono_tarjeta2 = QLabel()
        icono_tarjeta2.setPixmap(qta.icon('ri.git-repository-private-fill', font_size=40, color='#00B622').pixmap(60, 60))
        icono_tarjeta2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        #Orden: ícono izquierda, texto derecha
        layout_tarjeta2.addLayout(info_tarjeta2)
        layout_tarjeta2.addWidget(icono_tarjeta2)
        
        
        # Agregar espacio flexible al inicio
        
        layout_tarjetas.addWidget(tarjeta1)
        layout_tarjetas.addWidget(tarjeta2)
        layout_tarjetas.addStretch()
        
        # Agregar tarjetas al scroll (ANTES del addStretch)
        layout_contenido_scroll.addWidget(contenedor_tarjetas)
        
        #-------------- 4. SECCION TABLA -------------
        seccion_tabla = QFrame()
        seccion_tabla.setStyleSheet("""
                                QFrame {
                                    background-color: #FFFFFF;
                                    border: 1px solid #E0E0E0;
                                    border-radius: 10px;
                                    }
                                    """)
        
        layout_seccion_tabla = QVBoxLayout(seccion_tabla)
        layout_seccion_tabla.setContentsMargins(20, 20, 20, 20)
        layout_seccion_tabla.setSpacing(15)
        
        #--------------Encabezado: Titulo + boton para crear proyectos
        encabezado_tabla = QWidget()
        encabezado_tabla.setStyleSheet("background-color: transparent;")
        layout_encabezado = QHBoxLayout(encabezado_tabla)
        layout_encabezado.setContentsMargins(0, 0, 0, 0)
        
        titulo_tabla = QLabel("Proyectos creados")
        titulo_tabla.setStyleSheet("""
                                  font-size: 25px;
                                  font-family: titillium web;
                                  font-weight: semibold;
                                  color: #333;
                                  border: none;
                                  """)
        btn_nuevo_proyecto = QPushButton("Nuevo proyecto")
        btn_nuevo_proyecto.setIcon(qta.icon('fa5s.plus', color='white'))
        btn_nuevo_proyecto.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_nuevo_proyecto.setStyleSheet("""
            QPushButton {
                background-color: #0065bb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-family: 'titillium web';
                font-weight: bold;
                }
                QPushButton:hover {
                background-color: #0053a6;
                }
                QPushButton:pressed {
                background-color: #00438c;
                }
                """)
        
        layout_encabezado.addWidget(titulo_tabla)
        layout_encabezado.addStretch()
        layout_encabezado.addWidget(btn_nuevo_proyecto)
        
        layout_seccion_tabla.addWidget(encabezado_tabla)
        
        #--------------BARRA DE BUSQUEDA Y FILTROS -------------
        barra_busqueda = QWidget()
        barra_busqueda.setStyleSheet("background-color: transparent;")
        layout_busqueda = QHBoxLayout(barra_busqueda)
        layout_busqueda.setContentsMargins(0, 0, 0, 0)
        layout_busqueda.setSpacing(15)
        
        # Campo de Busqueda
        #from PyQt6.QtWidgets import QLineEdit, QComboBox # que es qlineedit = cuadro de texto y qcombobox = lista desplegable
        
        input_busqueda = QLineEdit()
        input_busqueda.setPlaceholderText("Buscar proyecto...")
        icono_buscar = qta.icon('fa5s.search', color='#888')
        input_busqueda.addAction(icono_buscar, QLineEdit.ActionPosition.LeadingPosition)
        input_busqueda.setFixedHeight(35)
        input_busqueda.setFixedWidth(500)
        input_busqueda.setStyleSheet("""
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
        
        # CAMPO DE FILTRO (COMBOBOX)
        Combo_proyectos = QComboBox()
        Combo_proyectos.addItems(["Todos los proyectos", "Licitaciones públicas", "Licitaciones privadas"])
        Combo_proyectos.setFixedHeight(35)
        Combo_proyectos.setFixedWidth(250)
        Combo_proyectos.setStyleSheet("""
            QComboBox {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
                font-family: 'titillium web';
                background-color: #FAFBFC;
                color: #646464;
            }
            QComboBox:focus {
                border: 1px solid #0065bb;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                subcontrol-position: right center;
                }
            QcomboBox::down-arrow {
                width: 12px;
                height: 12px;
                image:none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
            }    
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
                font-family: 'titillium web';
                background-color: white;
                color: #646464;
                selection-background-color: #F2F2F2;
                selection-color: #0065bb;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 15px;
                min-height: 30px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F2F2F2;
            }
            """)
        
        layout_busqueda.addWidget(input_busqueda) 
        layout_busqueda.addWidget(Combo_proyectos)
        layout_busqueda.addStretch()
        
        layout_seccion_tabla.addWidget(barra_busqueda)

        #---------------Tabla proyectos-----------
        #from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem,QHeaderView # que es qtablewidget = tabla y qtablewidgetitem = celda de la tabla y qheaderview = cabecera de la tabla
        
        self.tabla_proyectos = QTableWidget()
        self.tabla_proyectos.setColumnCount(5)
        self.tabla_proyectos.setHorizontalHeaderLabels([ "Nombre", "Empresa","Tipo de Licitacion / Especidicacion", "Ultimo acceso", "Acciones"])
        
        # Estilo d ela tabla
        self.tabla_proyectos.setStyleSheet("""
                QTableWidget {
                    border: none;
                    background-color: white;
                    gridline-color: #F0F0F0;
                    font-size: 14px;
                    font-family: 'titillium web';
                }
                QHeaderView::section{
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
                QScrollBar: Vertical {
                    background-color: #F5F5F5;
                    width: 12px;
                    border-radius: 6px;
                    margin: 0;
                }
                QScrollBar::handle:Vertical {
                    background-color: #C0C0C0;
                    border-radius: 6px;
                    min-height: 30px;
                    }
                QScrollBar::handle:vertical:hover {
                    background-color: #A0A0A0;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0;
                    background: none;
                }
                QScrollBar:horizontal {
                    background-color: #F5F5F5;
                    height: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal {
                    background-color: #C0C0C0;
                    border-radius: 6px;
                    min-width: 30px;
                }
                QScrollBar::handle:horizontal:hover {
                    background-color: #A0A0A0;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0;
                    background: none;
                }
                """)
        
        # CONFIGURAR COLUMNAS
        
        header = self.tabla_proyectos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.tabla_proyectos.setColumnWidth(4, 120)
        
        # Ocultar numeros de filas
        self.tabla_proyectos.verticalHeader().setVisible(False)
        
        # ALTURA DE FILAS
        self.tabla_proyectos.verticalHeader().setDefaultSectionSize(50)
        # Hacer que la tabla se expanda verticalmente
        self.tabla_proyectos.setMinimumHeight(300)
        # Alternar colores de filas para mejor lectura
        self.tabla_proyectos.setAlternatingRowColors(True)
        self.tabla_proyectos.setStyleSheet(self.tabla_proyectos.styleSheet() + """
            QTableWidget {
                alternate-background-color: #FAFBFC;
            }
        """)

        # Quitar el borde de selección azul
        self.tabla_proyectos.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Seleccionar filas completas
        self.tabla_proyectos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Datos de ejemplo
        datos = [
            ("T-power", "Hocol", "Publica/Basica", "23/01/2026"),
            ("G-Flex", "CTS", "Privada/Premiun", "23/01/2026"),
            ("BlokSeT", "EcoPetrol", "Publica/Premiun", "23/01/2026"),
        ]
        
        self.tabla_proyectos.setRowCount(len(datos))
        
        for fila, (nombre,empresa,tipo,fecha) in enumerate(datos):
            self.tabla_proyectos.setItem(fila, 0, QTableWidgetItem(nombre))
            self.tabla_proyectos.setItem(fila, 1, QTableWidgetItem(empresa))
            self.tabla_proyectos.setItem(fila, 2, QTableWidgetItem(tipo))
            self.tabla_proyectos.setItem(fila, 3, QTableWidgetItem(fecha))
            
            # BOTON DE ACCIONES
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout(widget_acciones)
            layout_acciones.setContentsMargins(0,0,0,0)
            layout_acciones.setSpacing(5)
            
            btn_ver = QPushButton()
            btn_ver.setIcon(qta.icon("ei.eye-open", color="#0065bb"))
            btn_ver.setFixedSize(30, 30)
            btn_ver.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_ver.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                """)
            
            btn_editar = QPushButton()
            btn_editar.setIcon(qta.icon("fa5.edit", color="#0065bb"))
            btn_editar.setFixedSize(30, 30)
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                """)
            btn_eliminar = QPushButton()
            btn_eliminar.setIcon(qta.icon('fa6s.trash-can', color='#FA896B'))
            btn_eliminar.setFixedSize(30, 30)
            btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_eliminar.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
           
            
            layout_acciones.addWidget(btn_ver)
            layout_acciones.addWidget(btn_editar)
            layout_acciones.addWidget(btn_eliminar)
            self.tabla_proyectos.setCellWidget(fila, 4, widget_acciones)
        
        layout_seccion_tabla.addWidget(self.tabla_proyectos)
        
        # agragar seccion tabla al scroll
        layout_contenido_scroll.addWidget(seccion_tabla,1)
            
            
            

        
        
        
        
        
        # Agregar contenido al scroll
        area_scroll.setWidget(contenido_principal)
        
        # Agregar scroll al layout del contenido
        layout_contenido.addWidget(area_scroll)
        
        
        # === AGREGAR PANELES AL LAYOUT PRINCIPAL (solo una vez) ===
        layout_principal.addWidget(self.menu_lateral)
        layout_principal.addWidget(self.contenido, 1) # El contenido ocupa el resto del espacio
      
    #Funciones del la aplicacion
    def toggle_menu(self):
        """Colapsar o expandir el menu lateral"""
        if self.menu_expandido:
            # Colapsar el menu
            self.menu_lateral.setFixedWidth(60)
            # Ocultar textos de los botones (solo iconos)
            
           
            self.btn_inicio.setText("")
            self.btn_base_datos.setText("")
            self.btn_soporte.setText("")
            self.lbl_soporte.hide()
            self.logo.hide()
            self.perfil.hide()
            
            self.menu_expandido = False
        else:
            # Expandir el menu
            self.menu_lateral.setFixedWidth(250)
            # Mostrar textos de los botones
            
            self.btn_inicio.setText("Inicio")
            self.btn_base_datos.setText("Base de datos y plantillas")
            self.btn_soporte.setText("Solicitudes y soporte técnico")
            self.lbl_soporte.show()
            self.logo.show()
            self.perfil.show()
            
            self.menu_expandido = True
      
      
      
        
# punto de entrada de la aplicacion
if __name__ == "__main__":
    app=QApplication(sys.argv) # motor y controlador de toda la aplicacion
    ventana=VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())