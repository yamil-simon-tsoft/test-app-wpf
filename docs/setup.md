# Guía de Instalación y Configuración

## Requisitos Previos

### 1. Python
- **Versión requerida**: Python 3.8 o superior
- **Instalación**: Descargar desde [python.org](https://www.python.org/downloads/)
- **Verificación**: `python --version`

### 2. WinAppDriver
- **Descarga**: [GitHub WinAppDriver](https://github.com/Microsoft/WinAppDriver/releases)
- **Instalación**: Ejecutar el instalador como administrador
- **Ubicación por defecto**: `C:\Program Files (x86)\Windows Application Driver\`

### 3. Configuración de Windows
1. Habilitar "Developer Mode" en Windows:
   - Configuración → Actualización y seguridad → Para desarrolladores
   - Seleccionar "Modo de desarrollador"

2. Configurar permisos para WinAppDriver:
   - Ejecutar WinAppDriver como administrador la primera vez

### 4. Gauge (opcional para BDD)
```powershell
# Instalar Gauge desde chocolatey
choco install gauge

# O descargar desde: https://gauge.org/get-started/
```

## Configuración del Proyecto

### 1. Clonar el repositorio
```powershell
git clone <url-del-repositorio>
cd test-app-wpf
```

### 2. Configurar entorno virtual
```powershell
# Opción 1: Usar script de activación
.\activar.ps1

# Opción 2: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```powershell
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones específicas
```

### 4. Configurar aplicación objetivo
Editar `src/utils/config.py` o archivo `.env`:
```python
APP_PATH = r"C:\Ruta\A\Tu\Aplicacion.exe"
```

## Verificación de la Instalación

### 1. Verificar Python y dependencias
```powershell
python --version
pip list | findstr pytest
pip list | findstr selenium
```

### 2. Verificar WinAppDriver
```powershell
# Iniciar WinAppDriver (en otra terminal)
& "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"

# Verificar que está corriendo en http://127.0.0.1:4723
```

### 3. Ejecutar prueba básica
```powershell
# Prueba unitaria
pytest tests/unit/test_utils.py -v

# Prueba de configuración
python -c "from src.utils.config import Config; print('Config OK')"
```

## Configuración de VS Code

### 1. Extensiones recomendadas
VS Code instalará automáticamente las extensiones recomendadas al abrir el proyecto.

### 2. Configuración de Python Interpreter
1. Abrir VS Code en la carpeta del proyecto
2. Presionar `Ctrl+Shift+P`
3. Escribir "Python: Select Interpreter"
4. Seleccionar `.\venv\Scripts\python.exe`

### 3. Configuración de debug
Las configuraciones de debug ya están incluidas en `.vscode/launch.json`

## Solución de Problemas Comunes

### Error: "Import could not be resolved"
```powershell
# Verificar PYTHONPATH
echo $env:PYTHONPATH

# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### Error: WinAppDriver no se conecta
1. Verificar que WinAppDriver está ejecutándose
2. Verificar que la aplicación objetivo existe
3. Verificar permisos de administrador
4. Verificar que Developer Mode está habilitado

### Error: Gauge no funciona
```powershell
# Instalar plugin de Python para Gauge
gauge install python

# Verificar instalación
gauge version
```

### Error: PowerShell ExecutionPolicy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Estructura de Directorios de Instalación

```
C:\Program Files (x86)\Windows Application Driver\
├── WinAppDriver.exe
├── WinAppDriver.exe.config
└── ...

<proyecto>\
├── venv\
│   ├── Scripts\
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── activate.ps1
│   └── Lib\
└── ...
```

## Configuración Avanzada

### 1. Configuración de proxy (si aplica)
```powershell
pip install --proxy http://proxy:port -r requirements.txt
```

### 2. Configuración de certificados SSL (si aplica)
```powershell
pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
```

### 3. Configuración para CI/CD
Ver archivos de configuración en `.github/workflows/` (si existen)

## Verificación Final

Ejecutar la suite completa de verificación:
```powershell
# 1. Pruebas unitarias
pytest tests/unit/ -v

# 2. Configuración
python -c "from src.drivers.winapp_driver import WinAppDriver; print('WinAppDriver config OK')"

# 3. Gauge (si está instalado)
gauge run specs/example.spec --dry-run
```

Si todos los comandos anteriores ejecutan sin errores, la instalación está completa.
