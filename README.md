# URL Expander

URL Expander es una aplicación de escritorio multiplataforma desarrollada en Python con PyQt6. Permite expandir URLs acortadas y verificar su reputación en VirusTotal de forma sencilla, rápida y segura. Es ideal para usuarios que desean analizar enlaces sospechosos antes de abrirlos, así como para quienes gestionan múltiples URLs en su trabajo diario.

---

## 🚀 Características principales

- **Expansión de URLs acortadas**: Soporta servicios populares como bit.ly, tinyurl, t.co, adf.ly, entre otros.
- **Análisis de reputación con VirusTotal**: Consulta automática de la reputación de la URL expandida usando la API oficial.
- **Historial persistente**: Guarda todas las URLs expandidas en la sesión y permite exportarlas a un archivo de texto.
- **Soporte para múltiples URLs**: Puedes expandir y analizar varias URLs a la vez, ingresándolas una por línea.
- **Arrastrar y soltar**: Arrastra enlaces directamente a la aplicación para analizarlos.
- **Multilenguaje**: Interfaz disponible en español e inglés, seleccionable desde la propia app.
- **Notificaciones visuales**: Mensajes claros para cada acción y resultado.
- **Atajos de teclado**: Acceso rápido a funciones clave para usuarios avanzados.
- **Persistencia segura de la API Key**: Tu clave de VirusTotal se almacena localmente en `.env` y nunca se comparte.
- **Interfaz moderna y responsiva**: Basada en PyQt6 y personalizable mediante `style.qss`.

---

## 🛠️ Instalación y requisitos

1. **Clona este repositorio o descarga los archivos.**
2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecuta la aplicación:**
   ```bash
   python gui.py
   ```

**Requisitos mínimos:**
- Python 3.8 o superior
- PyQt6
- requests

---

## 🔑 Requisito importante: API Key de VirusTotal

Para que la aplicación pueda consultar la reputación de URLs, es obligatorio contar con una API Key de VirusTotal.

- Al primer uso, la app solicitará tu API Key de VirusTotal y la guardará en el archivo `.env`.
- Sin esta clave, la funcionalidad de reputación y análisis de URLs no estará disponible.
- Puedes obtener una API Key gratuita registrándote en https://www.virustotal.com/gui/user/<tu_usuario>/apikey
- Si necesitas cambiarla, elimina o edita el archivo `.env`.

---

## 🖥️ Uso básico

1. **Introduce una o varias URLs acortadas** en el campo principal (una por línea).
2. Haz clic en **"Expandir"** para obtener la URL original y su reputación.
3. Consulta el **historial** de URLs expandidas, copia cualquier resultado o expórtalo fácilmente.
4. Cambia el idioma desde el selector superior según tu preferencia.
5. Haz clic en el enlace de VirusTotal para ver el reporte completo si lo deseas.

---

## 📁 Estructura del proyecto

- `gui.py`: Interfaz principal y lógica de la app.
- `url_expander.py`: Lógica para expandir URLs acortadas.
- `vt_api.py`: Integración y comunicación con la API de VirusTotal.
- `style.qss`: Estilos visuales personalizados para la interfaz.
- `.env`: Archivo local donde se almacena tu API Key de VirusTotal.
- `README.md`, `CHANGELOG.md`, `.gitignore`: Documentación y configuración del proyecto.

---

## 🧩 Extensiones y personalización

- Puedes modificar el archivo `style.qss` para adaptar la apariencia a tu gusto.
- El código está modularizado para facilitar la integración de nuevas funciones (por ejemplo, soporte para otros servicios de reputación).

---

## ❓ Soporte y contacto

¿Tienes dudas, sugerencias o encontraste un bug?
- Abre un issue en el repositorio.
- O contacta al autor vía GitHub: [MixDark](https://github.com/MixDark)

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, siempre citando al autor original.
