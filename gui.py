import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import pyqtSignal
from url_expander import UrlExpander
from vt_api import VirusTotalAPI

class GUI(QWidget):
    security_result_signal = pyqtSignal(str, bool)
    def update_history(self):
        # Actualiza el widget de historial con las URLs expandidas
        self.history_text.setText('\n'.join(self.history))

    def copy_expanded_url(self):
        expanded_url = self.expander.expanded_url
        if expanded_url:
            clipboard = QApplication.instance().clipboard()
            clipboard.setText(expanded_url)
            self.result_text.setText(f'{self.result_text.toPlainText()}\n(URL copiada al portapapeles)')
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, 'Copiado', 'URL copiada al portapapeles.')
        # Si no hay URL expandida, no hacer nada ni mostrar mensajes

    def __init__(self):
        super().__init__()
        self.security_result_signal.connect(self._update_security_label)
        self.language = 'es'
        self.security_label = QLabel('')
        self.history = []
        self.expander = UrlExpander()
        self.vt_api = None
        self.api_key = None
        self.init_ui()
        self.ask_api_key()

    def _update_security_label(self, text, open_links):
        self.security_label.setText(text)
        if open_links:
            self.security_label.setOpenExternalLinks(True)
        else:
            self.security_label.setOpenExternalLinks(False)

    def export_history(self):
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        if not self.history:
            QMessageBox.information(self, 'Exportar historial', 'No hay historial para exportar.')
            return
        file_path, _ = QFileDialog.getSaveFileName(self, 'Guardar historial', 'historial.txt', 'Archivos de texto (*.txt)')
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.history))
                QMessageBox.information(self, 'Exportar historial', 'Historial exportado correctamente.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo exportar el historial: {e}')

    def ask_api_key(self):
        import os
        from PyQt6.QtWidgets import QInputDialog
        api_key = None
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('VT_API_KEY='):
                        api_key = line.strip().split('=', 1)[1]
                        break
        if api_key:
            self.api_key = api_key
            self.vt_api = VirusTotalAPI(api_key)
        else:
            api_key, ok = QInputDialog.getText(self, 'API Key de VirusTotal', 'Introduce tu API Key de VirusTotal:')
            if ok and api_key:
                self.api_key = api_key
                self.vt_api = VirusTotalAPI(api_key)
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f'VT_API_KEY={api_key}\n')
            else:
                self.api_key = None
                self.vt_api = None
                self.security_label.setText('No se configuró la API Key de VirusTotal.')

    def init_ui(self):
        self.setWindowTitle('URL Expander')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(520, 420)
        self.center()

        main_layout = QVBoxLayout()
        from PyQt6.QtWidgets import QComboBox
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(['Español', 'English'])
        self.lang_selector.currentIndexChanged.connect(self.change_language)
        main_layout.addWidget(self.lang_selector)

        self.instruction_label = QLabel('Introduce la URL acortada:')
        self.instruction_label.setStyleSheet('font-size: 12pt;')
        main_layout.addWidget(self.instruction_label)

        self.url_input = QTextEdit()
        self.url_input.setAcceptDrops(True)
        self.url_input.setPlaceholderText('')
        self.url_input.setMinimumHeight(40)
        self.url_input.setMaximumHeight(40)
        self.url_input.setFontPointSize(12)
        main_layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.expand_button = QPushButton('Expandir')
        self.expand_button.setFixedWidth(110)
        self.expand_button.setFixedHeight(32)
        self.expand_button.clicked.connect(self.expand_url)
        button_layout.addWidget(self.expand_button)
        self.open_button = QPushButton('Abrir')
        self.open_button.setFixedWidth(110)
        self.open_button.setFixedHeight(32)
        self.open_button.clicked.connect(self.open_url)
        button_layout.addWidget(self.open_button)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFontPointSize(12)
        main_layout.addWidget(self.result_text)

        self.history_label = QLabel('Historial de URLs expandidas:')
        self.history_label.setStyleSheet('font-size: 12pt;')
        main_layout.addWidget(self.history_label)
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMinimumHeight(60)
        self.history_text.setMaximumHeight(180)
        self.history_text.setFontPointSize(12)
        main_layout.addWidget(self.history_text)

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addStretch(1)
        self.export_button = QPushButton('Exportar historial')
        self.export_button.setFixedWidth(180)
        self.export_button.setFixedHeight(36)
        self.export_button.clicked.connect(self.export_history)
        action_buttons_layout.addWidget(self.export_button)
        self.copy_button = QPushButton('Copiar URL expandida')
        self.copy_button.setFixedWidth(180)
        self.copy_button.setFixedHeight(36)
        self.copy_button.clicked.connect(self.copy_expanded_url)
        action_buttons_layout.addWidget(self.copy_button)
        action_buttons_layout.addStretch(1)
        main_layout.addLayout(action_buttons_layout)

        self.security_label.setStyleSheet('font-size: 12pt;')
        main_layout.addWidget(self.security_label)
        self.setLayout(main_layout)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def expand_url(self):
        import re
        input_text = self.url_input.toPlainText().strip()
        url_regex = re.compile(r'^(https?://)?([\w.-]+)\.([a-z\.]{2,6})([/\w\.-]*)*/?$')
        if not input_text:
            self.result_text.setText('Por favor, introduce al menos una URL.')
            self.security_label.setText('')
            return
        urls = [line.strip() for line in input_text.splitlines() if line.strip()]
        resultados = []
        for short_url in urls:
            if not url_regex.match(short_url):
                resultados.append(f'❌ URL inválida: {short_url}')
                continue
            self.expander.expand_url(short_url, self.result_text)
            if self.expander.expanded_url:
                self.history.append(self.expander.expanded_url)
                resultados.append(f'✅ {short_url} → {self.expander.expanded_url}')
                # Si hay API key, analizar la URL expandida
                if self.vt_api:
                    self.security_label.setText('Analizando seguridad...')
                    import threading
                    def analizar_virustotal(url):
                        try:
                            # 1. Consultar primero el reporte
                            report = self.vt_api.get_report(url)
                            if report and not report.get('pending'):
                                stats = report['data']['attributes']['last_analysis_stats']
                                total = sum(stats.values())
                                malicious = stats.get('malicious', 0)
                                suspicious = stats.get('suspicious', 0)
                                harmless = stats.get('harmless', 0)
                                undetected = stats.get('undetected', 0)
                                resumen = f"<b>VirusTotal:</b> "
                                if malicious > 0:
                                    resumen += f"<span style='color:red;'>Maliciosos: {malicious}</span> | "
                                if suspicious > 0:
                                    resumen += f"<span style='color:orange;'>Sospechosos: {suspicious}</span> | "
                                resumen += f"<span style='color:green;'>Inofensivos: {harmless}</span> | "
                                resumen += f"No detectados: {undetected} | Total motores: {total}"
                                vt_url = report['data']['links'].get('self', None)
                                if vt_url:
                                    resumen += f"<br><a href='{vt_url}'>Ver reporte en VirusTotal</a>"
                                self.security_result_signal.emit(resumen, True)
                                return
                            # 2. Si no está listo, enviar a escanear y volver a consultar
                            enviado = self.vt_api.scan_url(url)
                            if enviado:
                                report = self.vt_api.get_report(url)
                                if report and not report.get('pending'):
                                    stats = report['data']['attributes']['last_analysis_stats']
                                    total = sum(stats.values())
                                    malicious = stats.get('malicious', 0)
                                    suspicious = stats.get('suspicious', 0)
                                    harmless = stats.get('harmless', 0)
                                    undetected = stats.get('undetected', 0)
                                    resumen = f"<b>VirusTotal:</b> "
                                    if malicious > 0:
                                        resumen += f"<span style='color:red;'>Maliciosos: {malicious}</span> | "
                                    if suspicious > 0:
                                        resumen += f"<span style='color:orange;'>Sospechosos: {suspicious}</span> | "
                                    resumen += f"<span style='color:green;'>Inofensivos: {harmless}</span> | "
                                    resumen += f"No detectados: {undetected} | Total motores: {total}"
                                    vt_url = report['data']['links'].get('self', None)
                                    if vt_url:
                                        resumen += f"<br><a href='{vt_url}'>Ver reporte en VirusTotal</a>"
                                    self.security_result_signal.emit(resumen, True)
                                elif report and report.get('pending'):
                                    vt_url = report.get('vt_url')
                                    mensaje = f"El análisis de VirusTotal aún no está listo. <a href='{vt_url}'>Ver reporte manualmente</a>"
                                    self.security_result_signal.emit(mensaje, True)
                                else:
                                    self.security_result_signal.emit('No se pudo obtener el reporte de VirusTotal.', False)
                            else:
                                self.security_result_signal.emit('No se pudo analizar la URL en VirusTotal.', False)
                        except Exception as e:
                            self.security_result_signal.emit(f'Error al analizar con VirusTotal: {e}', False)
                    threading.Thread(target=analizar_virustotal, args=(self.expander.expanded_url,), daemon=True).start()
            else:
                resultados.append(f'❌ No se pudo expandir: {short_url}')
        self.result_text.setText('\n'.join(resultados))
        self.update_history()

    def change_language(self, idx):
        if idx == 0:
            self.language = 'es'
            self.instruction_label.setText('Introduce la URL acortada:')
            self.copy_button.setText('Copiar URL expandida')
            self.open_button.setText('Abrir')
            self.expand_button.setText('Expandir')
            self.history_label.setText('Historial de URLs expandidas:')
            self.export_button.setText('Exportar historial')
            self.url_input.setPlaceholderText('Introduce una o varias URLs, una por línea o arrástralas aquí')
        else:
            self.language = 'en'
            self.instruction_label.setText('Enter the shortened URL:')
            self.copy_button.setText('Copy expanded URL')
            self.open_button.setText('Open')
            self.expand_button.setText('Expand')
            self.history_label.setText('Expanded URLs history:')
            self.export_button.setText('Export history')
            self.url_input.setPlaceholderText('Enter one or more URLs, one per line or drag them here')
    
    def open_url(self):
        self.expander.open_url()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Cargar y aplicar estilos desde style.qss
    try:
        with open('style.qss', 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f'No se pudo cargar el archivo de estilos: {e}')
    ex = GUI()
    ex.show()
    sys.exit(app.exec())