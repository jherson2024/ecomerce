#core/globals.py
from passlib.context import CryptContext

# Encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rutas de archivos
IMAGENES_PRODUCTO_DIR = "static/imagenes/producto/principal/"
IMAGENES_TIENDA_LOGO_DIR = "static/imagenes/logo_tienda/"
IMAGENES_PRODUCTO_OPCION_DIR = "static/imagenes/producto/opcion/"
IMAGENES_QR_DIR = "static/imagenes/qr/"
# Otros valores globales
ADMIN_PRINCIPAL_ID = "1"
URL_SERVER = "http://localhost:8000/"
