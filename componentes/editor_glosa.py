"""Componente: Editor de Glosas - Redacción de proyecto"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QScrollArea, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
import qtawesome as qta
import json
import os


# ============================================================
# Configuracion_de_sistema - Estructura jerárquica del sistema eléctrico
# proviene de la carpeta datos/configuracion_de_sistema.json
# ============================================================
def cargar_datos_sistema():
    """Carga los datos del sistema desde el archivo JSON"""
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_json = os.path.join(ruta_base, "datos", "configuracion_de_sistema.json")
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_json}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_json} no contiene un JSON válido")
        return {}

DATOS_SISTEMA = cargar_datos_sistema()


class BotonOpcion(QPushButton):
    """Botón de opción estilizado (toggle)"""

    def __init__(self, texto: str, grupo: str = ""):
        super().__init__(texto)
        self.seleccionado = False
        self.grupo = grupo
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.actualizar_estilo()

    def toggle(self):
        self.seleccionado = not self.seleccionado
        self.actualizar_estilo()

    def actualizar_estilo(self):
        if self.seleccionado:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0065bb;
                    color: white;
                    border: none;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 12px;
                    font-family: 'Titillium Web';
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #666;
                    border: 1px solid #E0E0E0;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 12px;
                    font-family: 'Titillium Web';
                }
                QPushButton:hover {
                    border-color: #0065bb;
                    color: #0065bb;
                }
            """)

    def set_seleccionado(self, estado: bool):
        self.seleccionado = estado
        self.actualizar_estilo()


class CheckOpcion(QWidget):
    """Checkbox estilizado para selección múltiple"""

    seleccion_cambio = pyqtSignal(str, bool)

    def __init__(self, texto: str):
        super().__init__()
        self.texto = texto
        self.seleccionado = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 10, 2)
        layout.setSpacing(5)

        self.check = QLabel()
        self.check.setFixedSize(16, 16)
        self.check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.check.setStyleSheet("""
            background-color: white;
            border: 2px solid #CCC;
            border-radius: 3px;
            font-size: 10px;
        """)

        self.label = QLabel(texto)
        self.label.setStyleSheet("""
            font-size: 12px; color: #333; font-family: 'Titillium Web';
        """)

        layout.addWidget(self.check)
        layout.addWidget(self.label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self.seleccionado = not self.seleccionado
        if self.seleccionado:
            self.check.setText("✓")
            self.check.setStyleSheet("""
                background-color: #0065bb;
                border: 2px solid #0065bb;
                border-radius: 3px;
                color: white;
                font-size: 10px;
                font-weight: bold;
            """)
        else:
            self.check.setText("")
            self.check.setStyleSheet("""
                background-color: white;
                border: 2px solid #CCC;
                border-radius: 3px;
                font-size: 10px;
            """)
        self.seleccion_cambio.emit(self.texto, self.seleccionado)
        event.accept()


class SeccionCaracteristica(QWidget):
    """Una sección dentro del panel de contenido (ej: Tipo de celda)"""

    seleccion_hecha = pyqtSignal(str, str, str)

    def __init__(self, titulo: str, opciones: list, nota: str = "", tipo: str = "single"):
        super().__init__()
        self.titulo = titulo
        self.opciones = opciones
        self.tipo = tipo
        #self.nota = nota
        self.botones = []
        self.checks = []
        self.valor_seleccionado = ""
        self.valores_multiples = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 5, 0, 5)
        layout.setSpacing(5)

        # Título con ícono +
        layout_titulo = QHBoxLayout()
        layout_titulo.setSpacing(5)

        icono = QLabel()
        icono.setPixmap(qta.icon('fa5s.plus-circle', color='#0065bb').pixmap(14, 14))

        lbl_titulo = QLabel(self.titulo)
        lbl_titulo.setStyleSheet("""
            font-size: 13px; font-family: 'Titillium Web';
            font-weight: bold; color: #333;
        """)

        layout_titulo.addWidget(icono)
        layout_titulo.addWidget(lbl_titulo)

        # Nota si existe
       # if self.nota:
        #    lbl_nota = QLabel(self.nota)
        #    lbl_nota.setStyleSheet("""
        #        font-size: 10px; color: #E67E22; font-family: 'Titillium Web';
        #    """)
        #    lbl_nota.setWordWrap(True)
       #     layout_titulo.addWidget(lbl_nota)

        layout_titulo.addStretch()
        layout.addLayout(layout_titulo)

        # Opciones
        if self.tipo == "multiple":
            layout_grid = QHBoxLayout()
            layout_grid.setSpacing(5)
            layout_grid.setContentsMargins(20, 0, 0, 0)

            col1 = QVBoxLayout()
            col2 = QVBoxLayout()

            for i, opcion in enumerate(self.opciones):
                check = CheckOpcion(opcion)
                check.seleccion_cambio.connect(self._on_check_cambio)
                self.checks.append(check)
                if i % 2 == 0:
                    col1.addWidget(check)
                else:
                    col2.addWidget(check)

            layout_grid.addLayout(col1)
            layout_grid.addLayout(col2)
            layout.addLayout(layout_grid)
        else:
            layout_opciones = QHBoxLayout()
            layout_opciones.setSpacing(8)
            layout_opciones.setContentsMargins(20, 0, 0, 0)

            for opcion in self.opciones:
                btn = BotonOpcion(opcion)
                btn.clicked.connect(lambda checked, b=btn: self._on_boton_click(b))
                self.botones.append(btn)
                layout_opciones.addWidget(btn)

            layout_opciones.addStretch()
            layout.addLayout(layout_opciones)

    def _on_boton_click(self, boton: BotonOpcion):
        for btn in self.botones:
            btn.set_seleccionado(False)
        boton.set_seleccionado(True)
        self.valor_seleccionado = boton.text()
        self.seleccion_hecha.emit("", self.titulo, self.valor_seleccionado)

    def _on_check_cambio(self, texto: str, estado: bool):
        if estado and texto not in self.valores_multiples:
            self.valores_multiples.append(texto)
        elif not estado and texto in self.valores_multiples:
            self.valores_multiples.remove(texto)
        self.seleccion_hecha.emit("", self.titulo, ", ".join(self.valores_multiples))


class SeccionColapsable(QWidget):
    """Sección con botón que despliega/oculta su contenido"""

    def __init__(self, titulo: str):
        super().__init__()
        self.titulo = titulo
        self.desplegado = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Botón de la sección
        self.btn_seccion = QPushButton()
        self.btn_seccion.setCursor(Qt.CursorShape.PointingHandCursor)
        self._actualizar_boton()
        self.btn_seccion.clicked.connect(self.toggle)
        layout.addWidget(self.btn_seccion)

        # Contenedor con línea vertical decorativa
        self.contenedor_con_linea = QWidget()
        self.contenedor_con_linea.setStyleSheet("background-color: transparent; border: none;")
        layout_linea = QHBoxLayout(self.contenedor_con_linea)
        layout_linea.setContentsMargins(8, 0, 0, 0)
        layout_linea.setSpacing(0)

        # Línea vertical
        linea = QFrame()
        linea.setFixedWidth(2)
        linea.setStyleSheet("background-color: #D0D0D0; border: none;")

        # Contenedor del contenido
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent; border: none;")
        self.layout_contenido = QVBoxLayout(self.contenedor)
        self.layout_contenido.setContentsMargins(5, 0, 0, 0)
        self.layout_contenido.setSpacing(2)

        layout_linea.addWidget(linea)
        layout_linea.addWidget(self.contenedor, 1)

        self.contenedor_con_linea.setVisible(False)
        layout.addWidget(self.contenedor_con_linea)

    def _actualizar_boton(self):
        if self.desplegado:
            self.btn_seccion.setText(f"  ▾  {self.titulo}")
            self.btn_seccion.setStyleSheet("""
                QPushButton {
                    background-color: #E3F2FD;
                    border: none;
                    text-align: left;
                    font-size: 14px;
                    font-family: 'Titillium Web';
                    font-weight: bold;
                    color: #0065bb;
                    padding: 10px 8px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #BBDEFB;
                }
            """)
        else:
            self.btn_seccion.setText(f"  ▸  {self.titulo}")
            self.btn_seccion.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    font-size: 14px;
                    font-family: 'Titillium Web';
                    font-weight: bold;
                    color: #333;
                    padding: 10px 8px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #F0F4F8;
                }
            """)

    def toggle(self):
        self.desplegado = not self.desplegado
        self.contenedor_con_linea.setVisible(self.desplegado)
        self._actualizar_boton()

    def agregar_widget(self, widget):
        self.layout_contenido.addWidget(widget)

    def insertar_widget(self, indice: int, widget):
        self.layout_contenido.insertWidget(indice, widget)

    def indice_de(self, widget) -> int:
        return self.layout_contenido.indexOf(widget)


class PanelContenido(QFrame):
    """Panel izquierdo con las características del sistema"""

    contenido_actualizado = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.selecciones = {}
        self.secciones_widgets = {}
        self.secciones_colapsables = {}
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(550)
        self.setMaximumWidth(5800)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Encabezado
        encabezado = QWidget()
        encabezado.setStyleSheet("background-color: transparent; border: none;")
        layout_enc = QHBoxLayout(encabezado)
        layout_enc.setContentsMargins(20, 20, 20, 10)
        layout_enc.setSpacing(10)

        icono = QLabel()
        icono.setPixmap(qta.icon('ri.file-list-3-line', color='#0065bb').pixmap(28, 28))

        titulo = QLabel("Contenido")
        titulo.setStyleSheet("""
            font-size: 22px; font-family: 'Titillium Web';
            font-weight: bold; color: #0065bb;
        """)

        layout_enc.addWidget(icono)
        layout_enc.addWidget(titulo)
        layout_enc.addStretch()
        layout_principal.addWidget(encabezado)

        # Área scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                background-color: #F5F5F5; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0; border-radius: 4px; min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        contenido_scroll = QWidget()
        contenido_scroll.setStyleSheet("background-color: transparent; border: none;")
        self.layout_scroll = QVBoxLayout(contenido_scroll)
        self.layout_scroll.setContentsMargins(20, 10, 20, 20)
        self.layout_scroll.setSpacing(5)

        # Título categoría
        lbl_categoria = QLabel("Características del sistema")
        lbl_categoria.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            font-weight: bold; color: #0065bb;
            padding: 5px 0;
        """)
        self.layout_scroll.addWidget(lbl_categoria)

        # crear todas las secciones del JSON
        self.secciones_colapsables = {}  # Diccionario para guardar secciones
        self._crear_secciones_desde_json()

        self.layout_scroll.addStretch()
        scroll.setWidget(contenido_scroll)
        layout_principal.addWidget(scroll)

    def _crear_secciones_desde_json(self):
       """Crea todas las secciones del JSON DINAMICAMENTE"""
       for nombre_seccion,datos_seccion in DATOS_SISTEMA.items():
            #crer seccion colapsable para cada seccion principal del json
            seccion_colapsable = SeccionColapsable(nombre_seccion)
            
            # crear las caracteristicas dentro de cada seccion
            self._crear_caracteristicas_seccion(seccion_colapsable, nombre_seccion, datos_seccion)
            
            # agregar al layout
            self.layout_scroll.addWidget(seccion_colapsable)
            
            # guardar referencia para futuras actualizaciones
            self.secciones_widgets[nombre_seccion] = seccion_colapsable
    
    def _crear_caracteristicas_seccion(self, seccion_colapsable, nombre_seccion, datos_seccion):
         """crea las caracteristicas dentro de una seccion colapsable segun el json""" 
         for clave, config in datos_seccion.items():
             # verifica que sea un diccionario con configuracion valida
            if not isinstance(config, dict) or "titulo" not in config:
                continue
             
            titulo = config.get("titulo", clave)
            opciones = config.get("opciones", [])
            nota = config.get("nota", "")
            tipo = config.get("tipo", "")
            
            # si tiene dependencias (como "celda"), mostrar  mensaje inicial
            if "dependencias" in config:
                opciones = ["Seleccione las opciones validad para acceder"]
            # crear la seccion caracteristicas
            sec= SeccionCaracteristica(titulo, opciones, nota=nota, tipo=tipo) 
            sec.seleccion_hecha.connect(self._on_seleccion)
            
            # guardar referencia con clave unica:"nombre_secccion.clave"
            clave_unica = f"{nombre_seccion}.{clave}"
            self.secciones_widgets[clave_unica] = sec
            
            # agregar a la seccion colapsable
            seccion_colapsable.agregar_widget(sec)
                         
    def _on_seleccion(self, seccion: str, campo: str, valor: str):
        """Maneja una selección genérica"""
        self.selecciones[campo] = valor
        
        #buscar si hay capos con dependencias que actualizar
        self._actualizar_dependencias()
        
        self .contenido_actualizado.emit(self.selecciones)

    def _actualizar_dependencias(self):
        """Actualizar un campo especifico que tiene dopendencias"""
        for nombre_seccion,datos_seccion in DATOS_SISTEMA.items():
            for clave,config in datos_seccion.items():
                if not isinstance(config, dict):
                    continue
                if "dependencias"  in config:
                    self._actualizar_campo_con_dependencias(nombre_seccion, clave, config)
    
    def _actualizar_campo_con_dependencias(self, nombre_seccion, clave, config):
        """Actualizar un campo especifico que tiene dependencias"""
        dependencias = config.get("dependencias", {})
        titulo = config.get("titulo", clave)
        
        # Obtener valores seleccionados para navegar las dependencias
        # para media tension : familia -> tension -> tipo 
        familia = self.selecciones.get("Familia de la celda", "")
        tension = self.selecciones.get("Nivel de tensión", "")
        tipo = self.selecciones.get("Tipo de celda", "")
        
        # navegar las dependencias
        nuevas_opciones = []
        if familia in dependencias:
            if tension in dependencias[familia]:
                if tipo in dependencias[familia][tension]:
                    nuevas_opciones = dependencias[familia][tension][tipo]
                    
        if not nuevas_opciones:
            nuevas_opciones = ["Seleccione tipo, tensión y familia"]
            
        # Buscar y actualizar el widget
        clave_unica = f"{nombre_seccion}.{clave}"
        sec_actual = self.secciones_widgets[clave_unica]
        
        if sec_actual:
            seccion_colapsable = self.secciones_widgets[nombre_seccion]
            if seccion_colapsable:
                idx = seccion_colapsable.indice_de(sec_actual)
                
                sec_actual.setParent(None) 
                sec_actual.deleteLater()
                
                nueva_sec = SeccionCaracteristica(titulo, nuevas_opciones)
                nueva_sec.seleccion_hecha.connect(self._on_seleccion)
                
                self.secciones_widgets[clave_unica] = nueva_sec
                seccion_colapsable.insertar_widget(idx, nueva_sec)  # ← usar insertar_widget             
            
       
class PrevisualizadorDocumento(QFrame):
    """Panel derecho que muestra la vista previa del documento"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #E8E8E8;
                border: none;
                border-radius: 5px;
            }
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                background-color: #D0D0D0; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #0065bb; border-radius: 5px; min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        self.pagina = QFrame()
        self.pagina.setStyleSheet("""
            QFrame { background-color: white; border: none; }
        """)
        self.pagina.setMinimumWidth(580)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(QColor(0, 0, 0, 40))
        sombra.setOffset(3, 3)
        self.pagina.setGraphicsEffect(sombra)

        self.layout_pagina = QVBoxLayout(self.pagina)
        self.layout_pagina.setContentsMargins(50, 40, 50, 40)
        self.layout_pagina.setSpacing(15)

        self._mostrar_vacio()

        scroll.setWidget(self.pagina)
        layout_principal.addWidget(scroll)

    def _mostrar_vacio(self):
        self._limpiar_pagina()

        lbl_sistema = QLabel("Sistema eléctrico")
        lbl_sistema.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            font-weight: bold; color: #333; padding: 10px 0;
        """)
        self.layout_pagina.addWidget(lbl_sistema)
        self.layout_pagina.addSpacing(40)

        lbl_vacio = QLabel("Su proyecto está Vacío")
        lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_vacio.setStyleSheet("""
            font-size: 28px; font-family: 'Titillium Web';
            color: #C0C0C0; font-weight: bold;
        """)
        self.layout_pagina.addWidget(lbl_vacio)

        lbl_instruccion = QLabel(
            "Añadir Características a su sistema\n"
            "Puede definir los detalles de estas características más adelante"
        )
        lbl_instruccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_instruccion.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            color: #888; line-height: 1.5;
        """)
        self.layout_pagina.addWidget(lbl_instruccion)

        self.layout_pagina.addSpacing(20)
        for _ in range(4):
            self._agregar_placeholder()
        self.layout_pagina.addStretch()

    def _agregar_placeholder(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(15)

        check = QLabel("✓")
        check.setFixedSize(30, 30)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check.setStyleSheet("""
            background-color: #E8F5E9; color: #4CAF50;
            border-radius: 15px; font-size: 14px; font-weight: bold;
        """)

        barras = QVBoxLayout()
        barras.setSpacing(5)
        barra1 = QFrame()
        barra1.setFixedHeight(12)
        barra1.setFixedWidth(250)
        barra1.setStyleSheet("background-color: #E0E0E0; border-radius: 6px;")
        barra2 = QFrame()
        barra2.setFixedHeight(10)
        barra2.setFixedWidth(200)
        barra2.setStyleSheet("background-color: #EEEEEE; border-radius: 5px;")
        barras.addWidget(barra1)
        barras.addWidget(barra2)

        layout.addWidget(check)
        layout.addLayout(barras)
        layout.addStretch()
        self.layout_pagina.addWidget(widget)

    def _limpiar_pagina(self):
        while self.layout_pagina.count():
            item = self.layout_pagina.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

    def actualizar_documento(self, selecciones: dict):
        """Actualiza el documento con contenido de la base de datos"""
        from database.consultas import obtener_contenido_por_selecciones
        from PyQt6.QtGui import QPixmap
        import os
        
        self._limpiar_pagina()
        
        # verificar que haya selecciones validas
        tiene_seleccion = False
        for campo, valor in selecciones.items():
            if valor and valor not in ["No aplica", "Seleccione las opciones anteriores", "Seleccione tipo, tensión y familia"]:
                tiene_seleccion = True
                break
        if not tiene_seleccion:
            self._mostrar_vacio()
            return
        
        # Obtener contenido de la base de datos
        contenidos = obtener_contenido_por_selecciones(selecciones)
        
        if not contenidos:
            self._mostrar_vacio()
            return
        
        # ====== ENCABEZADO ======
        celda = selecciones.get("Celda", "")
        nivel = selecciones.get("Nivel de tensión", "")
        
        # ignorar placeholders
        if celda in ["Seleccione las opciones anteriores", "Seleccione tipo, tensión y familia"]:
            celda = ""
        
        titulo_doc = QLabel(f"1. Celdas de media tensión {celda} {nivel}")
        titulo_doc.setStyleSheet("""
            font-size: 18px; font-family: 'Titillium Web';
            font-weight: bold; color: #333; padding: 10px 0;
        """)
        self.layout_pagina.addWidget(titulo_doc)
        
        # ====== CONTENIDO POR SECCIONES ======
        seccion_actual = ""
        
        for item in contenidos:
            # Si cambió la sección, mostrar título de sección
            if item['seccion_numero'] != seccion_actual:
                seccion_actual = item['seccion_numero']
                lbl_seccion = QLabel(f"{item['seccion_numero']} {item['seccion_nombre']}")
                lbl_seccion.setStyleSheet("""
                    font-size: 14px; font-family: 'Titillium Web';
                    font-weight: bold; color: #333; padding: 15px 0 5px 0;
                """)
                self.layout_pagina.addWidget(lbl_seccion)
            
            # Mostrar contenido según el tipo
            if item['tipo'] == 'texto':
                self._agregar_texto(item['texto'])
            
            elif item['tipo'] == 'lista':
                self._agregar_lista(item['texto'])
            
            elif item['tipo'] == 'imagen':
                if item.get('imagen'):
                    self._agregar_imagen(item['imagen'])
        
        self.layout_pagina.addStretch()


    def _agregar_texto(self, texto: str):
        """Agrega un párrafo de texto"""
        lbl = QLabel(texto)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("""
            font-size: 11px; font-family: 'Titillium Web';
            color: #333; line-height: 1.6; padding: 5px 0;
        """)
        self.layout_pagina.addWidget(lbl)


    def _agregar_lista(self, texto: str):
        """Agrega una lista (items separados por ;)"""
        items = texto.split(';')
        
        for item in items:
            contenedor = QWidget()
            layout = QHBoxLayout(contenedor)
            layout.setContentsMargins(20, 2, 0, 2)
            layout.setSpacing(10)
            
            # Viñeta
            bullet = QLabel("•")
            bullet.setStyleSheet("font-size: 14px; color: #333;")
            bullet.setFixedWidth(15)
            
            # Texto
            lbl = QLabel(item.strip())
            lbl.setStyleSheet("""
                font-size: 11px; font-family: 'Titillium Web'; color: #333;
            """)
            
            layout.addWidget(bullet)
            layout.addWidget(lbl)
            layout.addStretch()
            
            self.layout_pagina.addWidget(contenedor)


    def _agregar_imagen(self, imagen: dict):
        """Agrega una imagen con su pie"""
        import os
        from PyQt6.QtGui import QPixmap
        
        # Contenedor centrado
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)
        
        # Cargar imagen
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "datos", imagen['ruta'])
        
        lbl_imagen = QLabel()
        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            pixmap = pixmap.scaled(
                imagen['ancho'], imagen['alto'],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_imagen.setPixmap(pixmap)
        else:
            lbl_imagen.setText(f"[Imagen no encontrada: {imagen['nombre']}]")
            lbl_imagen.setStyleSheet("color: red; padding: 20px;")
        
        lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_imagen)
        
        # Pie de imagen
        if imagen['pie']:
            lbl_pie = QLabel(imagen['pie'])
            lbl_pie.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_pie.setStyleSheet("""
                font-size: 10px; font-family: 'Titillium Web';
                font-weight: bold; color: #333; padding: 5px 0;
            """)
            layout.addWidget(lbl_pie)
    
        self.layout_pagina.addWidget(contenedor)
        
    def _agregar_subseccion(self, titulo: str, texto: str):
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            font-weight: bold; color: #333; padding: 8px 0 5px 0;
        """)
        self.layout_pagina.addWidget(lbl_titulo)

        lbl_texto = QLabel(texto)
        lbl_texto.setWordWrap(True)
        lbl_texto.setStyleSheet("""
            font-size: 12px; font-family: 'Titillium Web';
            color: #333; line-height: 1.6; padding: 5px 0;
        """)
        self.layout_pagina.addWidget(lbl_texto)

    def _generar_descripcion(self, sel: dict) -> str:
        tipo = sel.get("Tipo de celda", "")
        familia = sel.get("Familia de la celda", "")
        texto = "Las siguientes especificaciones se aplican a celdas de distribución modular"
        if tipo:
            texto += f", tipo {tipo.lower()}"
        if familia:
            texto += f", tecnología {familia}"
        texto += (", incluyendo el conjunto de equipos de maniobra y/o protección "
                  "en celdas compartimentadas. El equipo para suministrar "
                  "consistirá de celdas alineadas que cumplen los siguientes criterios:\n\n"
                  "• Diseño evolutivo\n"
                  "• Fácil de instalar\n"
                  "• Seguro y fácil de operar\n"
                  "• Diseño compacto\n"
                  "• Bajo mantenimiento")
        return texto

    def _generar_condiciones(self, sel: dict) -> str:
        celda = sel.get("Celda", "")
        nivel = sel.get("Nivel de tensión", "")
        
        # Ignorar placeholder
        if celda == "Seleccione tipo, tensión y familia":
            celda = ""
            
        texto = "Las condiciones generales de operación son:\n\n"
        if nivel:
            texto += f"• Tensión nominal: {nivel}\n"
        texto += ("• Frecuencia: 60 Hz\n"
                  "• Temperatura ambiente: -5°C a 40°C\n"
                  "• Altitud: hasta 1000 msnm\n"
                  "• Humedad relativa: hasta 95%\n\n")
        if celda:
            texto += (f"Los equipos {celda} deberán cumplir con las normas "
                      "IEC 62271-200 e IEC 62271-1 en su última edición vigente.")
        return texto

    def _generar_caracteristicas(self, sel: dict) -> str:
        celda = sel.get("Celda", "")
        familia = sel.get("Familia de la celda", "")
        
        # Ignorar placeholder
        if celda == "Seleccione tipo, tensión y familia":
            celda = ""
            
        texto = "Características técnicas generales:\n\n"
        if celda:
            texto += f"• Tipo de celda: {celda}\n"
        if familia:
            texto += f"• Familia: {familia}\n"
        texto += ("• Material de envolvente: Acero inoxidable\n"
                  "• Grado de protección: IP3X\n"
                  "• Resistencia al arco interno: IAC AFLR\n"
                  "• Tipo de aislamiento: SF6 / Aire\n"
                  "• Vida útil mínima: 30 años")
        return texto


class EditorGlosa(QWidget):
    """Ventana principal del editor de glosas"""

    cerrar_signal = pyqtSignal()

    def __init__(self, datos_proyecto: dict = None):
        super().__init__()
        self.datos_proyecto = datos_proyecto or {}
        self.setup_ui()
        self.conectar_senales()

    def setup_ui(self):
        self.setStyleSheet("background-color: #FAFBFC;")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Breadcrumb
        breadcrumb = QWidget()
        breadcrumb.setStyleSheet("background-color: transparent;")
        layout_bread = QHBoxLayout(breadcrumb)
        layout_bread.setContentsMargins(30, 15, 30, 5)
        layout_bread.setSpacing(5)

        icono_home = QLabel()
        icono_home.setPixmap(qta.icon('fa5s.home', color='#888').pixmap(14, 14))
        lbl_inicio = QLabel("Inicio/")
        lbl_inicio.setStyleSheet("color: #888; font-size: 13px; font-family: 'Titillium Web';")
        icono_edit = QLabel()
        icono_edit.setPixmap(qta.icon('fa5s.edit', color='#888').pixmap(12, 12))
        lbl_redaccion = QLabel("Redacción de proyecto")
        lbl_redaccion.setStyleSheet("color: #888; font-size: 13px; font-family: 'Titillium Web';")

        layout_bread.addWidget(icono_home)
        layout_bread.addWidget(lbl_inicio)
        layout_bread.addWidget(icono_edit)
        layout_bread.addWidget(lbl_redaccion)
        layout_bread.addStretch()
        
        # Botón Exportar a Word
        self.btn_exportar = QPushButton("  Exportar a Word")
        self.btn_exportar.setIcon(qta.icon('fa5s.file-word', color='#ffffff'))
        self.btn_exportar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #0065bb;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-family: 'Titillium Web';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056a0;
            }
        """)
        self.btn_exportar.clicked.connect(self.exportar_a_word)
        layout_bread.addWidget(self.btn_exportar)
        
        layout_principal.addWidget(breadcrumb)

        # Contenido principal
        contenido = QWidget()
        contenido.setStyleSheet("background-color: transparent;")
        layout_contenido = QHBoxLayout(contenido)
        layout_contenido.setContentsMargins(15, 5, 15, 15)
        layout_contenido.setSpacing(15)

        self.panel_contenido = PanelContenido()
        self.previsualizador = PrevisualizadorDocumento()

        layout_contenido.addWidget(self.panel_contenido)
        layout_contenido.addWidget(self.previsualizador, 1)
        layout_principal.addWidget(contenido, 1)

    def conectar_senales(self):
        self.panel_contenido.contenido_actualizado.connect(
            self.previsualizador.actualizar_documento
        )
    def exportar_a_word(self):
        """Exporta el documento actual a Word"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        from database.consultas import obtener_contenido_por_selecciones
        from exportadores.exportar_word import exportar_glosa_a_word
        
        # Obtener selecciones actuales
        selecciones = self.panel_contenido.selecciones
        
        # Verificar que hay contenido
        if not selecciones:
            QMessageBox.warning(
                self, 
                "Sin contenido", 
                "No hay contenido para exportar.\nPor favor, seleccione las características del sistema."
            )
            return
        
        # Obtener contenido de la base de datos
        contenidos = obtener_contenido_por_selecciones(selecciones)
        
        if not contenidos:
            QMessageBox.warning(
                self, 
                "Sin contenido", 
                "No se encontró contenido para las selecciones actuales."
            )
            return
        
        # Preparar nombre de archivo sugerido
        nombre_proyecto = self.datos_proyecto.get('nombre', 'Glosa')
        version = self.datos_proyecto.get('version', 'v1')
        nombre_archivo = f"{nombre_proyecto}_Glosa_{version}.docx"
        
        # Diálogo para guardar archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar documento Word",
            nombre_archivo,
            "Documento Word (*.docx)"
        )
        
        if not ruta_archivo:
            return  # Usuario canceló
        
        # Exportar
        exito = exportar_glosa_a_word(
            datos_proyecto=self.datos_proyecto,
            contenidos=contenidos,
            selecciones=selecciones,
            ruta_archivo=ruta_archivo
        )
        
        if exito:
            QMessageBox.information(
                self,
                "Exportación exitosa",
                f"El documento se guardó correctamente en:\n{ruta_archivo}"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Hubo un error al exportar el documento."
            )    