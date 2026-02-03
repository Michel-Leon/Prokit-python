"""
PROKIT - Sistema de Gestión de Licitaciones
Punto de entrada de la aplicación
"""

import sys
from PyQt6.QtWidgets import QApplication
from ventanas import VentanaPrincipal

 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())