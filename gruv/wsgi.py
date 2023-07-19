import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gruv.settings')

application = get_wsgi_application()

# Añade el directorio raíz de tu proyecto a sys.path
path = '/home/malcovarela90/gruv'  # Reemplaza 'usuario' y 'nombre_proyecto' con tu información
if path not in sys.path:
    sys.path.append(path)

# Configura las variables de entorno necesarias
os.environ['DJANGO_SETTINGS_MODULE'] = 'gruv.settings'  # Reemplaza 'nombre_proyecto' con el nombre real de tu proyecto

# Activa tu entorno virtual (si estás utilizando uno)
# Si no estás utilizando un entorno virtual, puedes omitir esta parte
# venv_path = '/home/malcovarela90/entornoVirtual'  # Reemplaza 'usuario' y 'nombre_entorno' con tu información
# activate_this = os.path.join(venv_path, 'bin/activate')
# with open(activate_this) as f:
#     exec(f.read(), {'__file__': activate_this})

# Importa el framework o la aplicación que deseas ejecutar
from django.core.wsgi import get_wsgi_application

# Crea una instancia de la aplicación WSGI
application = get_wsgi_application()

