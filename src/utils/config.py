"""
Configuración global del proyecto.

Este módulo contiene todas las configuraciones necesarias para
ejecutar las pruebas automatizadas.
"""

import os
from typing import Optional
from pathlib import Path


class Config:
    """
    Clase de configuración centralizada.
    """
    
    def __init__(self):
        """Inicializa la configuración con valores por defecto."""
        self.load_environment_variables()
    
    def load_environment_variables(self) -> None:
        """Carga variables de entorno si existen."""
        # Configuración de WinAppDriver
        self.WINAPPDRIVER_URL = os.getenv('WINAPPDRIVER_URL', 'http://127.0.0.1:4723')
        
        # Configuración de la aplicación
        self.APP_PATH = os.getenv('APP_PATH', r'C:\Path\To\Your\WPF\Application.exe')
        
        # Configuración de timeouts
        self.IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
        self.EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
        self.PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
        
        # Configuración de reportes
        self.REPORTS_DIR = os.getenv('REPORTS_DIR', str(Path(__file__).parent.parent.parent / 'reports'))
        self.SCREENSHOTS_DIR = os.getenv('SCREENSHOTS_DIR', os.path.join(self.REPORTS_DIR, 'screenshots'))
        
        # Configuración de logs
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', os.path.join(self.REPORTS_DIR, 'automation.log'))
        
        # Configuración de pruebas
        self.HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
        self.RETRY_COUNT = int(os.getenv('RETRY_COUNT', '3'))
        
    def get_winappdriver_url(self) -> str:
        """Obtiene la URL de WinAppDriver."""
        return self.WINAPPDRIVER_URL
    
    def get_app_path(self) -> str:
        """Obtiene la ruta de la aplicación WPF."""
        return self.APP_PATH
    
    def set_app_path(self, path: str) -> None:
        """Establece la ruta de la aplicación WPF."""
        self.APP_PATH = path
    
    def get_implicit_wait(self) -> int:
        """Obtiene el timeout implícito."""
        return self.IMPLICIT_WAIT
    
    def get_explicit_wait(self) -> int:
        """Obtiene el timeout explícito."""
        return self.EXPLICIT_WAIT
    
    def get_page_load_timeout(self) -> int:
        """Obtiene el timeout de carga de página."""
        return self.PAGE_LOAD_TIMEOUT
    
    def get_reports_dir(self) -> str:
        """Obtiene el directorio de reportes."""
        return self.REPORTS_DIR
    
    def get_screenshots_dir(self) -> str:
        """Obtiene el directorio de screenshots."""
        return self.SCREENSHOTS_DIR
    
    def get_log_level(self) -> str:
        """Obtiene el nivel de log."""
        return self.LOG_LEVEL
    
    def get_log_file(self) -> str:
        """Obtiene el archivo de log."""
        return self.LOG_FILE
    
    def is_headless(self) -> bool:
        """Verifica si se ejecuta en modo headless."""
        return self.HEADLESS
    
    def get_retry_count(self) -> int:
        """Obtiene el número de reintentos."""
        return self.RETRY_COUNT
    
    def create_directories(self) -> None:
        """Crea los directorios necesarios si no existen."""
        os.makedirs(self.REPORTS_DIR, exist_ok=True)
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)


# Instancia global de configuración
config = Config()
