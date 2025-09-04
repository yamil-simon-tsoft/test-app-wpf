# Guía de Uso del Proyecto de Automatización WPF

## Introducción

Este proyecto permite automatizar pruebas sobre aplicaciones WPF usando:
- **WinAppDriver**: Para la automatización de la interfaz
- **pytest**: Para pruebas unitarias e integración
- **Gauge**: Para especificaciones BDD en lenguaje natural
- **Allure**: Para reportes visuales

## Estructura del Flujo de Trabajo

### 1. Configuración Inicial (una sola vez)
```powershell
# Activar entorno y configurar
.\activar.ps1

# Configurar aplicación objetivo
# Editar .env con la ruta de tu aplicación WPF
```

### 2. Desarrollo de Pruebas

#### Crear pruebas pytest
```python
# tests/integration/test_mi_funcionalidad.py
import pytest
from src.pages.base_page import BasePage

@pytest.mark.integration
def test_mi_funcionalidad(driver):
    page = BasePage(driver)
    # Tu código de prueba aquí
```

#### Crear especificaciones Gauge
```markdown
# specs/mi_funcionalidad.spec
# Mi Funcionalidad

## Escenario: Validar funcionalidad X
* Abrir la aplicación WPF
* Hacer clic en "Botón X"
* Verificar que aparece "Mensaje Y"
```

#### Implementar pasos Gauge
```python
# step_impl/step_implementation.py
@step("Hacer clic en <boton>")
def hacer_clic_boton(boton):
    # Implementación del paso
```

### 3. Ejecución de Pruebas

#### Ejecutar todas las pruebas pytest
```powershell
pytest
```

#### Ejecutar pruebas específicas
```powershell
# Solo pruebas unitarias
pytest tests/unit/

# Solo pruebas de integración
pytest tests/integration/

# Pruebas por marcador
pytest -m smoke        # Pruebas smoke
pytest -m login        # Pruebas de login
pytest -m "not slow"   # Excluir pruebas lentas
```

#### Ejecutar con reportes Allure
```powershell
# Generar datos para Allure
pytest --alluredir=reports/allure-results

# Servir reporte Allure (requiere allure instalado)
allure serve reports/allure-results
```

#### Ejecutar especificaciones Gauge
```powershell
# Todas las especificaciones
gauge run specs/

# Especificación específica
gauge run specs/example.spec

# Con reporte HTML
gauge run specs/ --html-report
```

### 4. Debugging

#### Debug con VS Code
1. Establecer breakpoints en el código
2. Presionar F5 o usar configuraciones de debug
3. Seleccionar configuración apropiada:
   - "Python: Current File"
   - "Python: Pytest Current File"
   - "Python: All Tests"

#### Debug manual
```powershell
# Ejecutar con debug
pytest tests/integration/test_wpf_app.py::test_valid_login -v -s

# Con logging detallado
pytest tests/ -v -s --log-cli-level=DEBUG
```

## Patrones de Uso Comunes

### 1. Page Object Model

#### Crear nueva página
```python
# src/pages/mi_pagina.py
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class MiPagina(BasePage):
    # Localizadores
    BOTON_GUARDAR = (By.NAME, "btnGuardar")
    CAMPO_TEXTO = (By.NAME, "txtCampo")
    
    def guardar_datos(self, texto):
        self.send_keys_to_element(self.CAMPO_TEXTO, texto)
        self.click_element(self.BOTON_GUARDAR)
```

#### Usar página en pruebas
```python
def test_guardar_datos(driver):
    pagina = MiPagina(driver)
    pagina.guardar_datos("Datos de prueba")
    assert pagina.is_element_visible(MiPagina.MENSAJE_EXITO)
```

### 2. Datos de Prueba

#### Agregar nuevos datos
```python
# src/data/test_data.py
class MisDatos:
    DATOS_FORMULARIO = {
        "nombre": "Juan Pérez",
        "email": "juan@email.com"
    }
```

#### Usar datos en pruebas
```python
def test_con_datos(driver, test_data):
    datos = test_data.DATOS_FORMULARIO
    # Usar datos en la prueba
```

### 3. Fixtures Personalizadas

#### Crear fixture para configuración específica
```python
# tests/conftest.py
@pytest.fixture
def app_configurada(driver):
    # Configuración específica
    driver.set_window_size(1024, 768)
    yield driver
    # Limpieza específica
```

## Comandos Útiles por Escenario

### Desarrollo Diario
```powershell
# Activar entorno
.\activar.ps1

# Ejecutar pruebas rápidas
pytest -m smoke

# Ejecutar prueba específica mientras desarrollas
pytest tests/integration/test_mi_prueba.py::test_funcion -v -s
```

### Antes de un Commit
```powershell
# Ejecutar todas las pruebas
pytest

# Verificar formato de código
black src/ tests/
isort src/ tests/

# Ejecutar lint
flake8 src/ tests/
```

### Ejecución Completa (Nightly/CI)
```powershell
# Pruebas completas con reportes
pytest --alluredir=reports/allure-results --html=reports/pytest-report.html

# Especificaciones Gauge
gauge run specs/ --html-report

# Generar reporte Allure
allure generate reports/allure-results -o reports/allure-reports --clean
```

## Configuración de Diferentes Entornos

### Entorno de Desarrollo
```bash
# .env
APP_PATH=C:\Dev\MiApp\Debug\App.exe
LOG_LEVEL=DEBUG
RETRY_COUNT=1
```

### Entorno de Pruebas
```bash
# .env
APP_PATH=C:\Test\MiApp\Release\App.exe
LOG_LEVEL=INFO
RETRY_COUNT=3
```

## Solución de Problemas en Uso

### La aplicación no se abre
1. Verificar que WinAppDriver está ejecutándose
2. Verificar la ruta en APP_PATH
3. Verificar permisos de la aplicación

### Elementos no se encuentran
1. Usar herramientas de inspección (Inspect.exe)
2. Verificar localizadores en Page Objects
3. Ajustar timeouts si es necesario

### Pruebas intermitentes
1. Agregar waits explícitos
2. Verificar sincronización de la aplicación
3. Usar retry en operaciones críticas

## Reportes y Métricas

### Ubicación de Reportes
- **pytest HTML**: `reports/pytest-report.html`
- **Allure**: `reports/allure-reports/index.html`
- **Gauge**: `reports/html-report/index.html`
- **Screenshots**: `reports/screenshots/`
- **Logs**: `reports/automation.log`

### Interpretar Resultados
- **Verde**: Pruebas exitosas
- **Rojo**: Pruebas fallidas (revisar logs y screenshots)
- **Amarillo**: Pruebas saltadas o con warnings

## Mejores Prácticas

### 1. Organización de Pruebas
- Una clase por funcionalidad
- Nombres descriptivos para pruebas
- Usar marcadores para categorizar

### 2. Mantenimiento
- Actualizar Page Objects cuando cambie la UI
- Revisar y limpiar datos de prueba
- Mantener documentación actualizada

### 3. Performance
- Usar pruebas unitarias para lógica de negocio
- Reservar pruebas de integración para flujos críticos
- Ejecutar en paralelo cuando sea posible

## Extensión del Framework

### Agregar nueva funcionalidad
1. Crear módulo en `src/`
2. Agregar pruebas en `tests/`
3. Documentar en `docs/`
4. Actualizar `requirements.txt` si es necesario

### Integración con CI/CD
- Ver documentación específica de CI/CD
- Configurar variables de entorno en el pipeline
- Archivar reportes como artefactos
