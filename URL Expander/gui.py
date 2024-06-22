import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from url_expander import UrlExpander

class GUI(QWidget):

    def __init__(self):
        super().__init__()
        
        self.UI()
        self.expander = UrlExpander()
        
    def UI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('URL Expander')
        self.setWindowIcon(QIcon('icon.ico')) 
        self.setFixedSize(400, 250)  
        self.center()

        # Configuración del layout
        main_layout = QVBoxLayout()
        
        # Etiqueta de instrucción
        self.instruction_label = QLabel('Introduce la URL acortada:')
        main_layout.addWidget(self.instruction_label)
        
        # Campo de entrada de la URL
        self.url_input = QLineEdit()
        main_layout.addWidget(self.url_input)
        
        # Layout para los botones
        button_layout = QHBoxLayout()
        self.expand_button = QPushButton('Expandir')
        self.expand_button.clicked.connect(self.expand_url)
        button_layout.addStretch(1)
        button_layout.addWidget(self.expand_button)
        
        self.open_button = QPushButton('Abrir')
        self.open_button.clicked.connect(self.open_url)
        button_layout.addWidget(self.open_button)
        button_layout.addStretch(1)
        
        main_layout.addLayout(button_layout)
        
        # Campo de texto para mostrar la URL expandida
        self.result_text = QTextEdit()
        # Hacer que el campo de texto sea solo lectura
        self.result_text.setReadOnly(True)  
        main_layout.addWidget(self.result_text)
        
        # Configuración del layout principal
        self.setLayout(main_layout)
        
    def center(self):
        # Obtener el rectángulo de la ventana principal
        qr = self.frameGeometry()
        # Obtener el centro de la pantalla
        cp = QApplication.primaryScreen().availableGeometry().center()
        # Mover el rectángulo al centro de la pantalla
        qr.moveCenter(cp)
        # Mover la esquina superior izquierda de la ventana al rectángulo centrado
        self.move(qr.topLeft())
        
    def expand_url(self):
        short_url = self.url_input.text()
        self.expander.expand_url(short_url, self.result_text)
    
    def open_url(self):
        self.expander.open_url()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec())