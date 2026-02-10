# vt_api.py
# Módulo para consultar la API de VirusTotal y analizar URLs
import requests

class VirusTotalAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.virustotal.com/api/v3/urls'

    def scan_url(self, url):
        # Envía la URL para escaneo
        headers = {'x-apikey': self.api_key}
        data = {'url': url}
        response = requests.post(self.base_url, headers=headers, data=data)
        # No importa el id devuelto, para el reporte se usa el hash base64-url-safe de la URL
        if response.status_code == 200:
            return True
        else:
            return False

    def get_report(self, url, retries=24, delay=5):
        # Obtiene el reporte de análisis usando el hash base64-url-safe de la URL (solo 1 intento)
        import base64
        headers = {'x-apikey': self.api_key}
        url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip('=')
        full_url = f'{self.base_url}/{url_id}'
        import time
        for intento in range(retries):
            response = requests.get(full_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                status = data.get('data', {}).get('attributes', {}).get('status', '')
                if status == 'completed':
                    return data
                else:
                    time.sleep(delay)
            else:
                print(f"[VirusTotal] Error {response.status_code}: {response.text}")
                return None
        # Si tras los reintentos no está listo, mostrar enlace
        return {'pending': True, 'vt_url': f'https://www.virustotal.com/gui/url/{url_id}'}
