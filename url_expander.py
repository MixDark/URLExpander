import requests
import webbrowser
from PyQt6.QtWidgets import QMessageBox
# Para integración futura
try:
    from vt_api import VirusTotalAPI
except ImportError:
    VirusTotalAPI = None

class UrlExpander:

    def __init__(self):
        self.expanded_url = None

    @staticmethod
    def get_expanded_url(short_url):
        try:
            response = requests.head(short_url, allow_redirects=True)
            return response.url
        except requests.RequestException as e:
            print(f"Error al expandir la URL: {e}")
            return None

    def expand_url(self, short_url, result_text):
        self.expanded_url = self.get_expanded_url(short_url)
        
        if self.expanded_url:
            result_text.setText(f'La URL expandida es:\n{self.expanded_url}')
        else:
            QMessageBox.warning(None, 'Error', 'No se pudo expandir la URL.')

    def open_url(self):
        if self.expanded_url:
            webbrowser.open(self.expanded_url)
        else:
            QMessageBox.warning(None, 'Error', 'No hay URL expandida para abrir.')