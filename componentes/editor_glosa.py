"""Componente: Editor de Glosas - Redacción de proyecto"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QScrollArea, QSplitter, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
import qtawesome as qta


# ============================================================
# DATOS DE PRUEBA - Estructura jerárquica del sistema eléctrico
# En el futuro esto vendrá de una base de datos
# ============================================================
DATOS_SISTEMA = {
    "Sección de Media Tensión": {
        "tipo_celda": {
            "titulo": "Tipo de celda",
            "opciones": ["Primaria", "Secundaria"]
        },
        "nivel_tension": {
            "titulo": "Nivel de tensión",
            "opciones": ["24 Kv", "36 Kv"]
        },
        "familia_celda": {
            "titulo": "Familia de la celda",
            "opciones": ["AIS", "2SIS"],
        },
        "celda": {
            "dependencias": {
                "AIS": ["SM6", "SM AIRSET"],
                "2SIS": ["MCSet", "PIX"]
            },
            "titulo": "Celda"
        },
        "condiciones_generales": {
            "titulo": "Condiciones Generales",
            "opciones": ["Aplica", "No aplica"]
        },
        "caracteristicas_generales": {
            "titulo": "Características generales",
            "opciones": ["Aplica", "No aplica"]
        },
        "clases_celdas": {
            "titulo": "Clases de Celdas",
            "opciones": [
                "IM", "QM", "GBC", "DM1-A", "GAM-0", "GAM-2",
                "NSM-0", "NSM-1", "NSM-2", "NSM-3", "GAM-3"
            ],
            "tipo": "multiple"
        },
        "killin_products": {
            "titulo": "Killin products",
            "opciones": ["H-Guard", "Sistema de Testigos"]
        },
        "documentos": {
            "titulo": "Documentos",
            "opciones": ["Aplica", "No aplica"]
        },
        "pruebas_fat": {
            "titulo": "Pruebas FAT",
            "opciones": ["Aplica", "No aplica"]
        }
    }
}


class BotonOpcion(QPushButton):
    """Botón de opción estilizado (toggle)"""

    def __init__(self, texto: str, grupo: str = ""):
        super().__init__(texto)
        self.seleccionado = False
        self.grupo = grupo
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
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


class SeccionCaracteristica(QWidget):
    """Una sección dentro del panel de contenido (ej: Tipo de celda)"""

    seleccion_hecha = pyqtSignal(str, str, str)

    def __init__(self, titulo: str, opciones: list, nota: str = "", tipo: str = "single"):
        super().__init__()
        self.titulo = titulo
        self.opciones = opciones
        self.tipo = tipo
        self.nota = nota
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
        if self.nota:
            lbl_nota = QLabel(self.nota)
            lbl_nota.setStyleSheet("""
                font-size: 10px; color: #E67E22; font-family: 'Titillium Web';
            """)
            lbl_nota.setWordWrap(True)
            layout_titulo.addWidget(lbl_nota)

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

        # Línea vertical azul
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
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(420)
        self.setMaximumWidth(450)
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
        self.layout_contenido = QVBoxLayout(contenido_scroll)
        self.layout_contenido.setContentsMargins(20, 10, 20, 20)
        self.layout_contenido.setSpacing(5)

        # Título categoría
        lbl_categoria = QLabel("Características del sistema")
        lbl_categoria.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            font-weight: bold; color: #0065bb;
            padding: 5px 0;
        """)
        self.layout_contenido.addWidget(lbl_categoria)

        # Sección colapsable
        self._crear_seccion_media_tension()

        self.layout_contenido.addStretch()
        scroll.setWidget(contenido_scroll)
        layout_principal.addWidget(scroll)

    def _crear_seccion_media_tension(self):
        datos_mt = DATOS_SISTEMA["Sección de Media Tensión"]

        self.seccion_mt = SeccionColapsable("Sección de Media Tensión")

        # 1. Tipo de celda
        sec_tipo = SeccionCaracteristica(
            datos_mt["tipo_celda"]["titulo"],
            datos_mt["tipo_celda"]["opciones"]
        )
        sec_tipo.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["tipo_celda"] = sec_tipo
        self.seccion_mt.agregar_widget(sec_tipo)

        # 2. Nivel de tensión
        sec_nivel = SeccionCaracteristica(
            datos_mt["nivel_tension"]["titulo"],
            datos_mt["nivel_tension"]["opciones"]
        )
        sec_nivel.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["nivel_tension"] = sec_nivel
        self.seccion_mt.agregar_widget(sec_nivel)

        # 3. Familia de la celda
        sec_familia = SeccionCaracteristica(
            datos_mt["familia_celda"]["titulo"],
            datos_mt["familia_celda"]["opciones"],
            nota="Nota: celda cambia según la selección de familia"
        )
        sec_familia.seleccion_hecha.connect(self._on_seleccion_familia)
        self.secciones_widgets["familia_celda"] = sec_familia
        self.seccion_mt.agregar_widget(sec_familia)

        # 4. Celda
        sec_celda = SeccionCaracteristica(
            datos_mt["celda"]["titulo"],
            datos_mt["celda"]["dependencias"].get("AIS", [])
        )
        sec_celda.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["celda"] = sec_celda
        self.seccion_mt.agregar_widget(sec_celda)

        # 5. Condiciones Generales
        sec_condiciones = SeccionCaracteristica(
            datos_mt["condiciones_generales"]["titulo"],
            datos_mt["condiciones_generales"]["opciones"],
            nota="Se empieza a agregar información a partir de aquí"
        )
        sec_condiciones.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["condiciones_generales"] = sec_condiciones
        self.seccion_mt.agregar_widget(sec_condiciones)

        # 6. Características generales
        sec_caract = SeccionCaracteristica(
            datos_mt["caracteristicas_generales"]["titulo"],
            datos_mt["caracteristicas_generales"]["opciones"]
        )
        sec_caract.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["caracteristicas_generales"] = sec_caract
        self.seccion_mt.agregar_widget(sec_caract)

        # 7. Clases de Celdas
        sec_clases = SeccionCaracteristica(
            datos_mt["clases_celdas"]["titulo"],
            datos_mt["clases_celdas"]["opciones"],
            tipo="multiple"
        )
        sec_clases.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["clases_celdas"] = sec_clases
        self.seccion_mt.agregar_widget(sec_clases)

        # 8. Killin products
        sec_killin = SeccionCaracteristica(
            datos_mt["killin_products"]["titulo"],
            datos_mt["killin_products"]["opciones"]
        )
        sec_killin.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["killin_products"] = sec_killin
        self.seccion_mt.agregar_widget(sec_killin)

        # 9. Documentos
        sec_docs = SeccionCaracteristica(
            datos_mt["documentos"]["titulo"],
            datos_mt["documentos"]["opciones"]
        )
        sec_docs.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["documentos"] = sec_docs
        self.seccion_mt.agregar_widget(sec_docs)

        # 10. Pruebas FAT
        sec_fat = SeccionCaracteristica(
            datos_mt["pruebas_fat"]["titulo"],
            datos_mt["pruebas_fat"]["opciones"]
        )
        sec_fat.seleccion_hecha.connect(self._on_seleccion)
        self.secciones_widgets["pruebas_fat"] = sec_fat
        self.seccion_mt.agregar_widget(sec_fat)

        self.layout_contenido.addWidget(self.seccion_mt)

    def _on_seleccion(self, seccion: str, campo: str, valor: str):
        self.selecciones[campo] = valor
        self.contenido_actualizado.emit(self.selecciones)

    def _on_seleccion_familia(self, seccion: str, campo: str, valor: str):
        self.selecciones[campo] = valor

        datos_celda = DATOS_SISTEMA["Sección de Media Tensión"]["celda"]
        nuevas_opciones = datos_celda["dependencias"].get(valor, [])

        sec_celda_actual = self.secciones_widgets.get("celda")
        if sec_celda_actual:
            idx = self.seccion_mt.indice_de(sec_celda_actual)
            sec_celda_actual.setParent(None)
            sec_celda_actual.deleteLater()

            nueva_sec_celda = SeccionCaracteristica(
                datos_celda["titulo"],
                nuevas_opciones
            )
            nueva_sec_celda.seleccion_hecha.connect(self._on_seleccion)
            self.secciones_widgets["celda"] = nueva_sec_celda
            self.seccion_mt.insertar_widget(idx, nueva_sec_celda)

        self.contenido_actualizado.emit(self.selecciones)


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
        self._limpiar_pagina()

        tiene_contenido = False
        for campo, valor in selecciones.items():
            if valor and valor not in ["No aplica", ""]:
                tiene_contenido = True
                break

        if not tiene_contenido:
            self._mostrar_vacio()
            return

        # ====== ENCABEZADO ======
        titulo_doc = QLabel("TABLEROS DE DISTRIBUCIÓN ELÉCTRICA")
        titulo_doc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_doc.setStyleSheet("""
            font-size: 18px; font-family: 'Titillium Web';
            color: #888; font-weight: bold; padding: 10px 0;
        """)
        self.layout_pagina.addWidget(titulo_doc)

        subtitulo = QLabel("ESPECIFICACIONES TÉCNICAS")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 14px; font-family: 'Titillium Web';
            color: #888; padding-bottom: 10px;
        """)
        self.layout_pagina.addWidget(subtitulo)

        meta = QLabel("Fecha: --/--/2025     Código:     Proyecto:     Versión: N°.1")
        meta.setStyleSheet("""
            font-size: 11px; font-family: 'Titillium Web';
            color: #999; padding: 5px 0 15px 0;
        """)
        self.layout_pagina.addWidget(meta)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #E0E0E0;")
        self.layout_pagina.addWidget(sep)
        self.layout_pagina.addSpacing(10)

        # ====== SECCIÓN 1 ======
        celda = selecciones.get("Celda", "")
        nivel_tension = selecciones.get("Nivel de tensión", "")
        tipo_celda = selecciones.get("Tipo de celda", "")

        titulo_seccion = "Celdas de media tensión"
        if celda and nivel_tension:
            titulo_seccion = f"Celdas de media tensión {celda} {nivel_tension}"
        elif celda:
            titulo_seccion = f"Celdas de media tensión {celda}"

        lbl_seccion = QLabel(f"1.  {titulo_seccion}")
        lbl_seccion.setStyleSheet("""
            font-size: 16px; font-family: 'Titillium Web';
            font-weight: bold; color: #333; padding: 10px 0 5px 0;
        """)
        self.layout_pagina.addWidget(lbl_seccion)

        num = 1

        if celda or tipo_celda:
            self._agregar_subseccion(f"1.{num} Descripción",
                                      self._generar_descripcion(selecciones))
            num += 1

        if selecciones.get("Condiciones Generales", "") == "Aplica":
            self._agregar_subseccion(f"1.{num} Condiciones Generales",
                                      self._generar_condiciones(selecciones))
            num += 1

        if selecciones.get("Características generales", "") == "Aplica":
            self._agregar_subseccion(f"1.{num} Características generales",
                                      self._generar_caracteristicas(selecciones))
            num += 1

        clases = selecciones.get("Clases de Celdas", "")
        if clases:
            self._agregar_subseccion(
                f"1.{num} Clases de Celdas",
                f"Clases seleccionadas: {clases}\n\n"
                "Las celdas deben cumplir con las clasificaciones "
                "indicadas según normas IEC aplicables."
            )
            num += 1

        killin = selecciones.get("Killin products", "")
        if killin:
            self._agregar_subseccion(
                f"1.{num} Killin Products",
                f"Producto seleccionado: {killin}\n\n"
                "El sistema incluirá los componentes de protección "
                "y monitoreo especificados."
            )
            num += 1

        if selecciones.get("Documentos", "") == "Aplica":
            self._agregar_subseccion(
                f"1.{num} Documentos",
                "Se deberán entregar los siguientes documentos:\n\n"
                "• Planos de fabricación\n"
                "• Manuales de operación y mantenimiento\n"
                "• Certificados de pruebas\n"
                "• Diagramas unifilares"
            )
            num += 1

        if selecciones.get("Pruebas FAT", "") == "Aplica":
            self._agregar_subseccion(
                f"1.{num} Pruebas FAT",
                "Se realizarán pruebas de aceptación en fábrica (FAT) que incluyen:\n\n"
                "• Pruebas de rutina según IEC 62271-200\n"
                "• Verificación de circuitos de control\n"
                "• Pruebas de aislamiento\n"
                "• Verificación de enclavamientos mecánicos"
            )

        self.layout_pagina.addStretch()

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
        