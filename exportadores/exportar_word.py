"""Exportador de documentos a Word (.docx)"""
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
import os

class ExportarWord:
    """Clase para exportar documentos de glosa a word"""
    def __init__(self,datos_proyecto:dict,contenidos:list,selecciones:dict):
        """Parametros:
        datos_proyecto: Diccionario con datos del proyecto
                {"nombre:"...","codigo_crm": "...","version": "v1",...}
                contenidos: Lista de contenidos obtenidos de la base de datos
                selecciones: Diccionario con las selecciones del usuario
        """
        
        self.datos_proyecto = datos_proyecto
        self.contenidos = contenidos
        self.selecciones = selecciones
        self.documento = Document()
        self._configurar_documento()
        
    def _configurar_documento(self):
        """Configura las margen y estilo del documento"""
        secciones = self.documento.sections
        for seccion in secciones:
            seccion.top_margin = Cm(2.5)    
            seccion.bottom_margin = Cm(2.5)
            seccion.left_margin = Cm(2.5)
            seccion.right_margin = Cm(2.5)
    def _agregar_encabezado(self):
        """Agrega el encabezado con titulo, fecha, codigo,proyecto y version""" 
        
        #Titulo principal centrado
        titulo = self.documento.add_paragraph()
        titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER    
        run_titulo = titulo.add_run("TABLERO DE DISTRIBUCIÓN ELECTRICA")
        run_titulo.bold = True
        run_titulo.font.size = Pt(16)
        run_titulo.font.name = 'Arial'
        
        #subtitulo
        subtitulo = self.documento.add_paragraph()
        subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER    
        run_sub = subtitulo.add_run("ESPECIFICACIONES TÉCNICAS")
        run_sub.font.size = Pt(12)
        run_sub.font.name = 'Arial'
        
        #ESPACIO
        self.documento.add_paragraph()
        
        #Tabla con metadatos (fecha, codigo, proyecto, version)
        tabla_meta = self.documento.add_table(rows=1, cols=4)
        tabla_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # obtener datos del proyecto
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        nombre_proyecto = self.datos_proyecto.get('nombre','')
        codigo_crm = self.datos_proyecto.get('codigo_crm','')
        version = self.datos_proyecto.get('version','v1')
        
        # Formatear version (V1 -> V1, vel1 -> V1)
        if version:
            version_num = ''.join(filter(str.isdigit, version))
            version_formatear = f"V{version_num}" if version_num else "V1"
        else:
            version_formatear = "V1"
            
        # Llenar la tabla
        celdas = tabla_meta.rows[0].cells
        celdas[0].text = f"Fecha: {fecha_actual}"
        celdas[1].text = f"Código: {codigo_crm}"
        celdas[2].text = f"Proyecto: {nombre_proyecto}"
        celdas[3].text = f"Versión: {version_formatear}"
        
        # Estilo de las celdas
        for celda in celdas:
            for paragraph in celda.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    run.font.name = 'Arial' 
        
        # Linea separadora
        self.documento.add_paragraph()
        separador = self.documento.add_paragraph()
        separador.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_sep = separador.add_run("-" * 80) 
        run_sep.font.size = Pt(8) 
        
        self.documento.add_paragraph()
        
    def _agregar_titulo_seccion_principal(self):
        """ Agregar el tutulo d ela seccion pricipal (ej: 1. celdas de media tension)"""
        celda = self.selecciones.get("Celda", "")
        nivel = self.selecciones.get("Nivel de tensión","")
        
        # Ignorar placeholders
        if celda in ["seleccione las opciones anteriores","Seleccione tipo, tension y familia"]:
            celda = ""
            
        titulo_texto = "1.Celdas de media tensión"
        if celda and nivel:
            titulo_texto = f"1. Celdas de media tensión {celda} {nivel}"
        elif celda:
            titulo_texto = f"1. Celdas de media tensión {celda}"
            
        titulo = self.documento.add_paragraph()
        run = titulo.add_run(titulo_texto)
        run.bold = True
        run.font.size = Pt(14) 
        run.font.name = 'Arial'
        
        self.documento.add_paragraph()
     
    def _agregar_contenido(self):
        """Agrega todo el contenido del documento"""
        seccion_actual = ""
        for item in self.contenido:
            # si cambio la seccion, agregar titulo de seccion
            seccion_num=item.get('seccion_numero','')
            seccion_nom =item.get('seccion_nombre','')
            
            if seccion_num and seccion_num != seccion_actual:
                seccion_actual = seccion_num
                
                titulo_seccion = self.documento.add_paragraph()
                run = titulo_seccion.add_run(f"{seccion_num} {seccion_nom}")             
                run.bold = True
                run.font.size = Pt(12)
                run.font.name = 'Arial'
                
            # Agregar contenido segun tipo
            tipo = item.get('tipo','texto')
            
            if tipo == 'texto':
                self._agregar_parrafo(item.get('texto', ''))
            
            elif tipo == 'lista':
                self._agregar_lista(item.get('texto', ''))
            
            elif tipo == 'imagen':
                imagen_data = item.get('imagen')
                if imagen_data:
                    self._agregar_imagen(imagen_data)
    
    def _agregar_parrafo(self, texto: str):
        """Agrga un párrafo de texto"""
        if not texto: 
            return
        
        parrafo = self.documento.add_paragraph()
        run = parrafo.add_run(texto)
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        
        # Justificar texto
        parrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
    def _agregar_lista(self, texto: str):
        """Agrega una lista con viñetas""" 
        if not texto:
            return
        
        items = texto.split(';')
        for item in items:
            item = item.strip()
            if item:
                parrafo = self.documento.add_paragraph(item, style='List Bullet')
                run = parrafo.runs[0]
                run.font.size = Pt(11)
                run.font.name = 'Arial'
                
    def _agregar_imagen(self, imagen_data:dict):
        """Agrega una imagen centrada con pie de imagen"""
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "datos", imagen_data.get('ruta',''))
        
        if os.path.exists(ruta_imagen):
            #Agregar imagen centrada
            parrafo_img = self.documento.add_paragraph()
            parrafo_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = parrafo_img.add_run()
            
            # Calcular tamaño (maximo 4 pulgadas de ancho)
            ancho = min(imagen_data.get('ancho',400)/96,4) # Convertor px a pulgadas
            run.add_picture(ruta_imagen, width=Inches(ancho))
            
            # Agregar pie de imagen
            pie = imagen_data.get('pie','')
            if pie:
                parrafo_pie = self.documento.add_paragraph()
                parrafo_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_pie = parrafo_pie.add_run(pie)
                run_pie.bold = True
                run_pie.font.size = Pt(10)
                run_pie.font.name = 'Arial'
        self.documento.add_paragraph()
    
    def exportar(self, ruta_archivo:str) -> bool:
        """
        Genera y guarda el documento word.
        parametros:
            ruta_archivo: Ruta donde guardar el archivo .docx
            
        Retorna:
            true si se exportó correctamente, False en caso contrario    
        """
        try:
            # Construir el documento
            self._agregar_encabezado()
            self._agregar_titulo_seccion_principal()
            self._agregar_contenido()
            # Guardar el documento
            self.documento.save(ruta_archivo)
            return True
        except Exception as e:
            print(f"Error al exportar a Word: {e}")
            return False
    
    """Exportador de documentos a Word (.docx)"""

from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
import os


class ExportadorWord:
    """Clase para exportar el documento de glosa a Word"""
    
    def __init__(self, datos_proyecto: dict, contenidos: list, selecciones: dict):
        """
        Parámetros:
            datos_proyecto: Diccionario con datos del proyecto
                           {"nombre": "...", "codigo_crm": "...", "version": "v1", ...}
            contenidos: Lista de contenidos obtenidos de la base de datos
            selecciones: Diccionario con las selecciones del usuario
        """
        self.datos_proyecto = datos_proyecto
        self.contenidos = contenidos
        self.selecciones = selecciones
        self.documento = Document()
        self._configurar_documento()
    
    def _configurar_documento(self):
        """Configura los márgenes y estilos del documento"""
        secciones = self.documento.sections
        for seccion in secciones:
            seccion.top_margin = Cm(2.5)
            seccion.bottom_margin = Cm(2.5)
            seccion.left_margin = Cm(2.5)
            seccion.right_margin = Cm(2.5)
    
    def _agregar_encabezado(self):
        """Agrega el encabezado con título, fecha, código, proyecto y versión"""
        
        # Título principal centrado
        titulo = self.documento.add_paragraph()
        titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = titulo.add_run("TABLEROS DE DISTRIBUCIÓN ELÉCTRICA")
        run_titulo.bold = True
        run_titulo.font.size = Pt(16)
        run_titulo.font.name = 'Arial'
        
        # Subtítulo
        subtitulo = self.documento.add_paragraph()
        subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_sub = subtitulo.add_run("ESPECIFICACIONES TÉCNICAS")
        run_sub.font.size = Pt(12)
        run_sub.font.name = 'Arial'
        
        # Espacio
        self.documento.add_paragraph()
        
        # Tabla con metadatos (Fecha, Código, Proyecto, Versión)
        tabla_meta = self.documento.add_table(rows=1, cols=4)
        tabla_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Obtener datos
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        nombre_proyecto = self.datos_proyecto.get('nombre', '')
        codigo_crm = self.datos_proyecto.get('codigo_crm', '')
        version = self.datos_proyecto.get('version', 'v1')
        
        # Formatear versión (v1 → V1, ve1 → V1)
        if version:
            version_num = ''.join(filter(str.isdigit, version))
            version_formateada = f"V{version_num}" if version_num else "V1"
        else:
            version_formateada = "V1"
        
        # Llenar la tabla
        celdas = tabla_meta.rows[0].cells
        
        celdas[0].text = f"Fecha: {fecha_actual}"
        celdas[1].text = f"Código: {codigo_crm}"
        celdas[2].text = f"Proyecto: {nombre_proyecto}"
        celdas[3].text = f"Versión: N°{version_formateada}"
        
        # Estilo de las celdas
        for celda in celdas:
            for paragraph in celda.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    run.font.name = 'Arial'
        
        # Línea separadora
        self.documento.add_paragraph()
        separador = self.documento.add_paragraph()
        separador.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_sep = separador.add_run("_" * 80)
        run_sep.font.size = Pt(8)
        
        self.documento.add_paragraph()
    
    def _agregar_titulo_seccion_principal(self):
        """Agrega el título de la sección principal (ej: 1. Celdas de media tensión SM6 24Kv)"""
        celda = self.selecciones.get("Celda", "")
        nivel = self.selecciones.get("Nivel de tensión", "")
        
        # Ignorar placeholders
        if celda in ["Seleccione las opciones anteriores", "Seleccione tipo, tensión y familia"]:
            celda = ""
        
        titulo_texto = "1. Celdas de media tensión"
        if celda and nivel:
            titulo_texto = f"1. Celdas de media tensión {celda} {nivel}"
        elif celda:
            titulo_texto = f"1. Celdas de media tensión {celda}"
        
        titulo = self.documento.add_paragraph()
        run = titulo.add_run(titulo_texto)
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Arial'
        
        self.documento.add_paragraph()
    
    def _agregar_contenido(self):
        """Agrega todo el contenido del documento"""
        seccion_actual = ""
        
        for item in self.contenidos:
            # Si cambió la sección, agregar título de sección
            seccion_num = item.get('seccion_numero', '')
            seccion_nom = item.get('seccion_nombre', '')
            
            if seccion_num and seccion_num != seccion_actual:
                seccion_actual = seccion_num
                
                titulo_seccion = self.documento.add_paragraph()
                run = titulo_seccion.add_run(f"{seccion_num} {seccion_nom}")
                run.bold = True
                run.font.size = Pt(12)
                run.font.name = 'Arial'
            
            # Agregar contenido según tipo
            tipo = item.get('tipo', 'texto')
            
            if tipo == 'texto':
                self._agregar_parrafo(item.get('texto', ''))
            
            elif tipo == 'lista':
                self._agregar_lista(item.get('texto', ''))
            
            elif tipo == 'imagen':
                imagen_data = item.get('imagen')
                if imagen_data:
                    self._agregar_imagen(imagen_data)
    
    def _agregar_parrafo(self, texto: str):
        """Agrega un párrafo de texto"""
        if not texto:
            return
        
        parrafo = self.documento.add_paragraph()
        run = parrafo.add_run(texto)
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        
        # Justificar texto
        parrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    def _agregar_lista(self, texto: str):
        """Agrega una lista con viñetas"""
        if not texto:
            return
        
        items = texto.split(';')
        for item in items:
            item = item.strip()
            if item:
                parrafo = self.documento.add_paragraph(style='List Bullet')
                run = parrafo.add_run(item)
                run.font.size = Pt(11)
                run.font.name = 'Arial'
    
    def _agregar_imagen(self, imagen_data: dict):
        """Agrega una imagen centrada con pie de imagen"""
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(ruta_base, "datos", imagen_data.get('ruta', ''))
        
        if os.path.exists(ruta_imagen):
            # Agregar imagen centrada
            parrafo_img = self.documento.add_paragraph()
            parrafo_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = parrafo_img.add_run()
            
            # Calcular tamaño (máximo 4 pulgadas de ancho)
            ancho = min(imagen_data.get('ancho', 400) / 96, 4)  # Convertir px a pulgadas
            run.add_picture(ruta_imagen, width=Inches(ancho))
            
            # Pie de imagen
            pie = imagen_data.get('pie', '')
            if pie:
                parrafo_pie = self.documento.add_paragraph()
                parrafo_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_pie = parrafo_pie.add_run(pie)
                run_pie.bold = True
                run_pie.font.size = Pt(10)
                run_pie.font.name = 'Arial'
        
        self.documento.add_paragraph()
    
    def exportar(self, ruta_archivo: str) -> bool:
        """
        Genera y guarda el documento Word.
        
        Parámetros:
            ruta_archivo: Ruta donde guardar el archivo .docx
        
        Retorna:
            True si se guardó correctamente, False si hubo error
        """
        try:
            # Construir el documento
            self._agregar_encabezado()
            self._agregar_titulo_seccion_principal()
            self._agregar_contenido()
            
            # Guardar
            self.documento.save(ruta_archivo)
            return True
        
        except Exception as e:
            print(f"Error al exportar a Word: {e}")
            return False


def exportar_glosa_a_word(datos_proyecto: dict, contenidos: list, selecciones: dict, ruta_archivo: str) -> bool:
    """
    Función auxiliar para exportar una glosa a Word.
    
    Parámetros:
        datos_proyecto: {"nombre": "...", "codigo_crm": "...", "version": "v1"}
        contenidos: Lista de contenidos de la base de datos
        selecciones: Selecciones del usuario
        ruta_archivo: Ruta donde guardar el .docx
    
    Retorna:
        True si se exportó correctamente
    """
    exportador = ExportadorWord(datos_proyecto, contenidos, selecciones)
    return exportador.exportar(ruta_archivo)
        