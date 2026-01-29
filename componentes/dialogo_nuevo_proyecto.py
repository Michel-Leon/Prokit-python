from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QComboBox, QCheckBox,
    QTextEdit, QFrame, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta


class DialogoNuevoProyecto(QDialog):

    # señal que emite los datos del nuevo proyecto
    proyecto_creado = pyqtSignal(dict)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Crear Nuevo Proyecto")   
        self.setFixedSize(500, 500)
        self.setStyleSheet("""
                           QDialog {
                               background-color: #FFFFFF;
                               border-radius: 10px;
                           }
                           """)
        layout= QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        #------ENCABEZADO  AZUL --------------
        encabezado = QFrame()
        encabezado.setFixedHeight(50)
        encabezado.setStyleSheet("background-color: #0065bb;")
        layout_encabezado = QHBoxLayout(encabezado)
        layout_encabezado.setContentsMargins(20,0,20,0)
        
        icono_titulo = QLabel()
        icono_titulo.setPixmap(qta.icon('fa5s.plus', color='white').pixmap(16,16))
        
        titulo = QLabel("Crear un Nuevo proyecto")
        titulo.setStyleSheet("""
                             color: white;
                             font-size: 16px;
                             font-family: 'Titillium Web';
                             font-weight: Bold;
                             """)
        
        btn_cerrar = QPushButton("X")
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
        btn_cerrar.clicked.connect(self.reject)
        
        layout_encabezado.addWidget(icono_titulo)
        layout_encabezado.addWidget(titulo)
        layout_encabezado.addStretch()
        layout_encabezado.addWidget(btn_cerrar)
        
        layout.addWidget(encabezado)
        
        # --- Contenido del formulario ---
        contenido = QFrame()
        contenido.setStyleSheet("background-color: white;")
        layout_contenido = QVBoxLayout(contenido)
        layout_contenido.setContentsMargins(25, 25, 25, 25)
        layout_contenido.setSpacing(15)
        
        #------Combobox - seleccionar plantilla --------------
        self.combo_plantilla = QComboBox()
        self.combo_plantilla.addItems([
            "Seleccione una plantilla *",
            "Plantilla Basica",
            "Plantilla Avanzada",
            "Plantilla Premium"
        ])
        
        self.combo_plantilla.setFixedHeight(40)
        self.combo_plantilla.setStyleSheet(self.estilo_combobox())
        layout_contenido.addWidget(self.combo_plantilla)
        
        # Imput - Nombre del proyecto
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del Proyecto")
        self.input_nombre.setFixedHeight(40)
        self.input_nombre.setStyleSheet(self.estilo_input())
        layout_contenido.addWidget(self.input_nombre)
        
        # Imput - Nombre de la empresa
        self.input_empresa = QLineEdit()
        self.input_empresa.setPlaceholderText("Nombre de la empresa*")
        self.input_empresa.setFixedHeight(40)
        self.input_empresa.setStyleSheet(self.estilo_input())
        layout_contenido.addWidget(self.input_empresa)
        
        #----Titulo de licitacion ----------
        lbl_tipo_licitacion = QLabel("Seleccione el tipo de licitación")
        lbl_tipo_licitacion.setStyleSheet("""
                                    color: #666;
                                    font-size: 13px;
                                    font-family: 'Titillium Web';
                                    font-weight: semibold;
                                    """)
        layout_contenido.addWidget(lbl_tipo_licitacion)
        
        # Checkboxes de licitación
        layout_licitacion = QHBoxLayout()
        layout_licitacion.setSpacing(15)
        
        self.check_publica = QCheckBox("Oferta Pública")
        self.check_privada = QCheckBox("Oferta Privada")
        self.check_otras_lic = QCheckBox("Otras")
        
        # Estilo para checkboxes
        estilo_checkbox = """
            QCheckBox {
                font-family: 'Titillium Web';
                font-size: 13px;
                color: #333;
                spacing: 8px;   
        }
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
            border: 2px solid #E0E0E0;
            border-radius: 4px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #0065bb;
            border-color: #0065bb;
        }
        """
        
        self.check_publica.setStyleSheet(estilo_checkbox)
        self.check_privada.setStyleSheet(estilo_checkbox)
        self.check_otras_lic.setStyleSheet(estilo_checkbox)
        
        # Grupo para que solo uno este seleccionado
        self.grupo_licitacion = QButtonGroup(self)
        self.grupo_licitacion.addButton(self.check_publica, 1)
        self.grupo_licitacion.addButton(self.check_privada, 2)
        self.grupo_licitacion.addButton(self.check_otras_lic, 3)
        self.grupo_licitacion.setExclusive(True)
        
        layout_licitacion.addWidget(self.check_publica)
        layout_licitacion.addWidget(self.check_privada)
        layout_licitacion.addWidget(self.check_otras_lic)
        layout_contenido.addStretch()
        
        layout_contenido.addLayout(layout_licitacion)
        
        # ------ Tipo de especificacion----
        lbl_tipo_especificacion = QLabel("Seleccione el tipo de especificación")
        lbl_tipo_especificacion.setStyleSheet("""
                                    color: #666;
                                    font-size: 13px;
                                    font-family: 'Titillium Web';
                                    font-weight: semibold;
                                    """)
        layout_contenido.addWidget(lbl_tipo_especificacion)
        
        # Checkboxes de especificación
        layout_especificacion = QHBoxLayout()
        layout_especificacion.setSpacing(15)
        
        self.check_basica = QCheckBox("Basica")
        self.check_premium = QCheckBox("Premium")
        self.check_otras_esp = QCheckBox("Otras")
        
        self.check_basica.setStyleSheet(estilo_checkbox)
        self.check_premium.setStyleSheet(estilo_checkbox)
        self.check_otras_esp.setStyleSheet(estilo_checkbox)
        
        # Grupo para que solo uno este seleccionado
        self.grupo_especificacion = QButtonGroup(self)
        self.grupo_especificacion.addButton(self.check_basica, 1)
        self.grupo_especificacion.addButton(self.check_premium, 2)
        self.grupo_especificacion.addButton(self.check_otras_esp, 3)
        self.grupo_especificacion.setExclusive(True)
        
        layout_especificacion.addWidget(self.check_basica)
        layout_especificacion.addWidget(self.check_premium)
        layout_especificacion.addWidget(self.check_otras_esp)
        layout_contenido.addStretch()
        
        layout_contenido.addLayout(layout_especificacion)
        
        #---- Comentarios----
        self.txt_comentarios = QTextEdit()
        self.txt_comentarios.setPlaceholderText("Comentarios a tener en cuenta")
        self.txt_comentarios.setFixedHeight(100)
        self.txt_comentarios.setStyleSheet("""
                            QTextEdit {
                                border: 1px solid #E0E0E0;
                                border-radius: 8px;
                                padding: 10px;
                                font-family: 'Titillium Web';
                                font-size: 14px;
                                background-color: white;
                                color: #333;
                            }
                            QTextEdit::placeholder {
                                color: #999;
                            }
                                    """)
        
        layout_contenido.addWidget(self.txt_comentarios)
        
        #ESPACIO FLEXIBLE
        layout_contenido.addStretch()
        
        # ---BOTON DE ACCION----
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFixedHeight(40)
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #666;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-family: 'Titillium Web';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
                                          
        btn_crear = QPushButton("Crear Proyecto")
        btn_crear.setFixedHeight(40)
        btn_crear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #0065bb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 30px;
                font-size: 14px;
                font-family: 'Titillium Web';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0053a6;
            }
        """)
        btn_crear.clicked.connect(self.crear_proyecto)

        layout_botones.addStretch()
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_crear)
        
        layout_contenido.addLayout(layout_botones)
        
        layout.addWidget(contenido)
        
    def estilo_input(self) -> str:    
        """ Retorna el estilo para los inputs """
        return """
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Titillium Web';
                background-color: white;
                color: #333;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QLineEdit:focus {
                border: 1px solid #0065bb;
            }
            """
    def estilo_combobox(self) -> str:
        """ Retorna el estilo para los combobox """
        return """
            QComboBox {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Titillium Web';
                background-color: white;
                color: #333;
            }
            QComboBox:focus {
                border: 1px solid #0065bb;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px sold #666;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                background-color: white;
                color: #333;
                selection-background-color: #E3F2FD;
            }
        """ 
    def crear_proyecto(self):
        """ Valida y emite los datos del nuevo proyecto """
        # Validar campos obligatorios
        if not self.input_nombre.text().strip():
            self.input_nombre.setStyleSheet(self.estilo_input() + """
                                            QLineEdit { border: 1px solid #FA896B;}
                                            """)
            return
        if not self.input_empresa.text().strip():
            self.input_empresa.setStyleSheet(self.estilo_input() + """
                                             QLineEdit { border: 1px solid #FA896B;}
                                             """)
            return
        
        # Obtener tipo de licitacion
        tipo_licitacion = ""
        if self.check_publica.isChecked():
            tipo_licitacion = "Pública"
        elif self.check_privada.isChecked():
            tipo_licitacion = "Privada"
        else:
            tipo_licitacion = "Otra"
            
        # obtener tipo de especificacion
        tipo_especificacion = ""
        if self.check_basica.isChecked():
            tipo_especificacion = "Básica"
        elif self.check_premium.isChecked():
            tipo_especificacion = "Premium"
        else:
            tipo_especificacion = "Otra"
        
        # Crear diccionario con datos
        from datetime import datetime
        datos = {
            "nombre": self.input_nombre.text().strip(),
            "empresa": self.input_empresa.text().strip(),
            "tipo_licitacion": tipo_licitacion,
            "tipo_especificacion": tipo_especificacion,
            "tipo_completo": f"{tipo_licitacion}/{tipo_especificacion}",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "comentarios": self.txt_comentarios.toPlainText(),
            "Plantilla": self.combo_plantilla.currentText()
        }
        
        # Emitir señal con datos
        self.proyecto_creado.emit(datos)
        
        # Cerrar dialogo
        self.accept()    
                    
                 
                              
        
        
        
        
        