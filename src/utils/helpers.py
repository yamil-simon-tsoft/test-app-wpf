"""
Funciones auxiliares para automatización de pruebas.

Este módulo contiene utilidades comunes que se usan en las pruebas
automatizadas como captura de pantallas, logs, etc.
"""

import os
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from src.utils.config import config


def setup_logging() -> logging.Logger:
    """
    Configura el sistema de logging.
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(config.get_log_file()), exist_ok=True)
    
    # Configurar formato de log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, config.get_log_level()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(config.get_log_file(), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def take_screenshot(driver, test_name: str, step_name: Optional[str] = None) -> str:
    """
    Toma una captura de pantalla.
    
    Args:
        driver: Instancia del driver
        test_name: Nombre de la prueba
        step_name: Nombre del paso (opcional)
    
    Returns:
        str: Ruta del archivo de screenshot
    """
    try:
        # Crear directorio de screenshots si no existe
        os.makedirs(config.get_screenshots_dir(), exist_ok=True)
        
        # Generar nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        step_suffix = f"_{step_name}" if step_name else ""
        filename = f"{test_name}{step_suffix}_{timestamp}.png"
        filepath = os.path.join(config.get_screenshots_dir(), filename)
        
        # Tomar screenshot
        driver.save_screenshot(filepath)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Screenshot guardado: {filepath}")
        
        return filepath
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error al tomar screenshot: {str(e)}")
        return ""


def wait_for_element_to_be_clickable(driver, locator, timeout: int = None):
    """
    Espera a que un elemento sea clickeable.
    
    Args:
        driver: Instancia del driver
        locator: Localizador del elemento
        timeout: Tiempo de espera en segundos
    
    Returns:
        WebElement: Elemento clickeable
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    timeout = timeout or config.get_explicit_wait()
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable(locator))


def wait_for_element_to_be_visible(driver, locator, timeout: int = None):
    """
    Espera a que un elemento sea visible.
    
    Args:
        driver: Instancia del driver
        locator: Localizador del elemento
        timeout: Tiempo de espera en segundos
    
    Returns:
        WebElement: Elemento visible
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    timeout = timeout or config.get_explicit_wait()
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located(locator))


def retry_on_failure(max_retries: int = None):
    """
    Decorador para reintentar una función en caso de fallo.
    
    Args:
        max_retries: Número máximo de reintentos
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = max_retries or config.get_retry_count()
            last_exception = None
            
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        logger = logging.getLogger(__name__)
                        logger.warning(f"Intento {attempt + 1} falló: {str(e)}. Reintentando...")
                        time.sleep(1)  # Esperar antes del siguiente intento
                    else:
                        logger = logging.getLogger(__name__)
                        logger.error(f"Función falló después de {retries + 1} intentos")
            
            raise last_exception
        return wrapper
    return decorator


def generate_test_data_filename(test_name: str, extension: str = "json") -> str:
    """
    Genera un nombre de archivo para datos de prueba.
    
    Args:
        test_name: Nombre de la prueba
        extension: Extensión del archivo
    
    Returns:
        str: Nombre del archivo generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{test_name}_data_{timestamp}.{extension}"


def clean_old_reports(days_to_keep: int = 7) -> None:
    """
    Limpia reportes antiguos.
    
    Args:
        days_to_keep: Número de días a mantener los reportes
    """
    try:
        reports_dir = Path(config.get_reports_dir())
        if not reports_dir.exists():
            return
        
        cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
        
        for file_path in reports_dir.rglob('*'):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                
        logger = logging.getLogger(__name__)
        logger.info(f"Reportes antiguos eliminados (más de {days_to_keep} días)")
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error al limpiar reportes antiguos: {str(e)}")


def get_project_root() -> Path:
    """
    Obtiene la ruta raíz del proyecto.
    
    Returns:
        Path: Ruta raíz del proyecto
    """
    return Path(__file__).parent.parent.parent
