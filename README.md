# test-app-wpf

Este repositorio implementa pruebas automatizadas sobre una aplicación WPF (Windows Presentation Foundation) utilizando Python, WinAppDriver, Gauge (BDD) y Allure para reportes.

## 🚀 Tecnologías Utilizadas

- **Python**: Lenguaje principal de automatización
- **WinAppDriver**: Automatización de aplicaciones WPF/Windows
- **Gauge**: Framework BDD para especificaciones en lenguaje natural
- **pytest**: Framework de testing para pruebas unitarias
- **Allure**: Generación de reportes visuales
- **Selenium/Appium**: Integración con WinAppDriver

## 📋 Estructura del Proyecto

```
test-app-wpf/
├── src/                    # Código fuente principal de automatización
│   ├── __init__.py        # Configuración del paquete
│   ├── drivers/           # Configuración de drivers
│   │   ├── __init__.py
│   │   └── winapp_driver.py
│   ├── pages/             # Page Object Model
│   │   ├── __init__.py
│   │   └── base_page.py
│   ├── utils/             # Funciones de utilidad
│   │   ├── __init__.py
│   │   ├── config.py      # Configuraciones globales
│   │   └── helpers.py     # Funciones auxiliares
│   └── data/              # Datos de prueba
│       ├── __init__.py
│       └── test_data.py
├── tests/                  # Pruebas automatizadas con pytest
│   ├── __init__.py
│   ├── conftest.py        # Configuración global de pytest
│   ├── unit/              # Pruebas unitarias
│   │   ├── __init__.py
│   │   └── test_utils.py
│   └── integration/       # Pruebas de integración
│       ├── __init__.py
│       └── test_wpf_app.py
├── specs/                  # Especificaciones Gauge (BDD)
│   ├── concepts/          # Conceptos reutilizables
│   ├── example.spec       # Especificación de ejemplo
│   └── wpf_automation.spec
├── step_impl/             # Implementación de pasos Gauge
│   ├── __init__.py
│   └── step_implementation.py
├── reports/               # Reportes de ejecución (Allure)
│   └── .gitkeep
├── .vscode/               # Configuraciones de VS Code
│   ├── settings.json     # Configuración del workspace
│   ├── extensions.json   # Extensiones recomendadas
│   └── launch.json       # Configuración de debug
├── docs/                  # Documentación
│   ├── setup.md          # Guía de instalación
│   └── usage.md          # Guía de uso
├── venv/                  # Entorno virtual (no incluido en Git)
├── .gitignore            # Archivos excluidos del control de versiones
├── .env.example          # Variables de entorno de ejemplo
├── activar.bat           # Script de activación (Windows CMD)
├── activar.ps1           # Script de activación (PowerShell)
├── pyproject.toml        # Configuración del proyecto
├── requirements.txt      # Dependencias del proyecto
├── gauge.properties      # Configuración de Gauge
├── manifest.json         # Manifiesto de Gauge
└── README.md             # Este archivo
```

## ⚙️ Configuración Inicial

### 1. Clonar el repositorio
```powershell
git clone <url-del-repositorio>
cd test-app-wpf
```

### 2. Crear y activar entorno virtual
```powershell
python -m venv venv
.\activar.ps1  # o .\activar.bat para CMD
```

### 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 4. Configurar WinAppDriver
- Descargar e instalar WinAppDriver desde [GitHub](https://github.com/Microsoft/WinAppDriver)
- Habilitar "Developer Mode" en Windows
- Ejecutar WinAppDriver.exe

### 5. Configurar Gauge
```powershell
gauge install python
gauge config check_updates false
```

## 🧪 Ejecutar Pruebas

### Pytest (Pruebas unitarias e integración)
```powershell
# Ejecutar todas las pruebas
pytest

# Ejecutar con reporte Allure
pytest --alluredir=reports/allure-results

# Generar reporte Allure
allure serve reports/allure-results
```

### Gauge (Especificaciones BDD)
```powershell
# Ejecutar todas las especificaciones
gauge run specs

# Ejecutar especificación específica
gauge run specs/wpf_automation.spec

# Ejecutar con reporte HTML
gauge run specs --html-report
```

## 📊 Reportes

Los reportes se generan en la carpeta `reports/`:
- **Allure**: Reportes interactivos HTML para pytest
- **Gauge**: Reportes HTML para especificaciones BDD

## 🔧 Configuración de VS Code

El proyecto incluye configuraciones optimizadas para VS Code:
- Extensiones recomendadas para Python, Gauge y testing
- Configuración de debugging
- Formateo automático con black y isort

## 📝 Uso

### 1. Crear nuevas pruebas pytest
Agregar archivos en `tests/` siguiendo el patrón `test_*.py`

### 2. Crear especificaciones Gauge
Agregar archivos `.spec` en `specs/` e implementar los pasos en `step_impl/`

### 3. Page Object Model
Crear nuevas páginas en `src/pages/` heredando de `BasePage`

## 🤝 Contribución

1. Crear rama feature
2. Implementar cambios
3. Ejecutar todas las pruebas
4. Crear Pull Request
