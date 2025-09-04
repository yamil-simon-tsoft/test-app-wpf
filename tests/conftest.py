"""
Configuración global para pytest.

Este archivo contiene fixtures y configuraciones que se aplicarán
a todas las pruebas del proyecto.
"""

import pytest
import logging
import os
import sys
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.drivers.winapp_driver import WinAppDriver
from src.utils.config import config
from src.utils.helpers import setup_logging, clean_old_reports


def pytest_configure(config_obj):
    """Configuración inicial de pytest."""
    # Configurar logging
    setup_logging()
    
    # Crear directorios necesarios
    config.create_directories()
    
    # Limpiar reportes antiguos
    clean_old_reports()


def pytest_sessionstart(session):
    """Se ejecuta al inicio de la sesión de pruebas."""
    logger = logging.getLogger(__name__)
    logger.info("=== Iniciando sesión de pruebas automatizadas ===")
    logger.info(f"Configuración de WinAppDriver: {config.get_winappdriver_url()}")
    logger.info(f"Aplicación objetivo: {config.get_app_path()}")


def pytest_sessionfinish(session, exitstatus):
    """Se ejecuta al final de la sesión de pruebas."""
    logger = logging.getLogger(__name__)
    if exitstatus == 0:
        logger.info("=== Todas las pruebas completadas exitosamente ===")
    else:
        logger.error(f"=== Sesión de pruebas terminada con errores (código: {exitstatus}) ===")


@pytest.fixture(scope="session")
def app_config():
    """
    Fixture que proporciona la configuración de la aplicación.
    
    Returns:
        Config: Instancia de configuración
    """
    return config


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia de WinAppDriver.
    
    Yields:
        webdriver.Remote: Instancia del driver configurado
    """
    win_driver = None
    try:
        # Inicializar driver
        win_driver = WinAppDriver()
        driver_instance = win_driver.start_driver()
        
        yield driver_instance
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error al inicializar driver: {str(e)}")
        raise
    finally:
        # Limpiar recursos
        if win_driver:
            win_driver.stop_driver()


@pytest.fixture(scope="function")
def driver_with_app(request):
    """
    Fixture que proporciona un driver con una aplicación específica.
    
    Args:
        request: Objeto request de pytest (debe tener param con la ruta de la app)
    
    Yields:
        webdriver.Remote: Instancia del driver configurado para la app específica
    """
    app_path = getattr(request, 'param', None)
    if not app_path:
        pytest.skip("No se especificó ruta de aplicación")
    
    win_driver = None
    try:
        # Inicializar driver con aplicación específica
        win_driver = WinAppDriver(app_path)
        driver_instance = win_driver.start_driver()
        
        yield driver_instance
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error al inicializar driver para {app_path}: {str(e)}")
        raise
    finally:
        # Limpiar recursos
        if win_driver:
            win_driver.stop_driver()


@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """
    Fixture que configura logging específico para cada prueba.
    
    Args:
        request: Objeto request de pytest
    """
    logger = logging.getLogger(request.node.name)
    logger.info(f"=== Iniciando prueba: {request.node.name} ===")
    
    def finalizer():
        logger.info(f"=== Finalizando prueba: {request.node.name} ===")
    
    request.addfinalizer(finalizer)
    return logger


@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """
    Fixture que toma screenshot en caso de fallo.
    
    Args:
        request: Objeto request de pytest
        driver: Instancia del driver
    """
    yield
    
    if request.node.rep_call.failed:
        try:
            from src.utils.helpers import take_screenshot
            test_name = request.node.name
            screenshot_path = take_screenshot(driver, test_name, "failure")
            
            # Agregar screenshot al reporte de Allure si está disponible
            try:
                import allure
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"Screenshot - {test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except ImportError:
                pass  # Allure no está instalado
                
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error al tomar screenshot: {str(e)}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar el resultado de las pruebas.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# Marcadores personalizados
def pytest_configure(config):
    """Configurar marcadores personalizados."""
    config.addinivalue_line(
        "markers", "smoke: Pruebas de smoke básicas"
    )
    config.addinivalue_line(
        "markers", "regression: Pruebas de regresión completas"
    )
    config.addinivalue_line(
        "markers", "login: Pruebas específicas de login"
    )
    config.addinivalue_line(
        "markers", "forms: Pruebas de formularios"
    )
    config.addinivalue_line(
        "markers", "ui: Pruebas de interfaz de usuario"
    )
    config.addinivalue_line(
        "markers", "integration: Pruebas de integración"
    )
    config.addinivalue_line(
        "markers", "slow: Pruebas que tardan más tiempo en ejecutarse"
    )


# Configuración para ejecución en paralelo (si se usa pytest-xdist)
@pytest.fixture(scope="session")
def worker_id(request):
    """
    Fixture que proporciona el ID del worker para ejecución en paralelo.
    """
    if hasattr(request.config, 'slaveinput'):
        return request.config.slaveinput['slaveid']
    else:
        return 'master'


# Fixture para datos de prueba
@pytest.fixture(scope="session")
def test_data():
    """
    Fixture que proporciona acceso a los datos de prueba.
    
    Returns:
        TestData: Clase con datos de prueba
    """
    from src.data.test_data import TestData
    return TestData
