"""
Configuración y manejo del driver WinAppDriver para automatización WPF.

Este módulo proporciona una abstracción para inicializar y manejar
conexiones con WinAppDriver para automatizar aplicaciones WPF.
"""

from appium import webdriver
from appium.options.windows import WindowsOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from typing import Optional
from src.utils.config import Config


class WinAppDriver:
    """
    Clase para manejar la conexión con WinAppDriver.
    """
    
    def __init__(self, app_path: Optional[str] = None):
        """
        Inicializa el driver de WinAppDriver.
        
        Args:
            app_path: Ruta a la aplicación WPF a automatizar
        """
        self.driver = None
        self.wait = None
        self.config = Config()
        self.app_path = app_path or self.config.get_app_path()
        self.logger = logging.getLogger(__name__)
        
    def start_driver(self) -> webdriver.Remote:
        """
        Inicia el driver WinAppDriver.
        
        Returns:
            webdriver.Remote: Instancia del driver configurado
        """
        try:
            options = WindowsOptions()
            options.app = self.app_path
            options.platform_name = "Windows"
            options.device_name = "WindowsPC"
            
            # Configuraciones adicionales
            options.set_capability("ms:waitForAppLaunch", "25")
            options.set_capability("ms:experimental-webdriver", True)
            
            self.driver = webdriver.Remote(
                command_executor=self.config.get_winappdriver_url(),
                options=options
            )
            
            # Configurar wait implícito
            self.driver.implicitly_wait(self.config.get_implicit_wait())
            self.wait = WebDriverWait(self.driver, self.config.get_explicit_wait())
            
            self.logger.info(f"WinAppDriver iniciado exitosamente para: {self.app_path}")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Error al iniciar WinAppDriver: {str(e)}")
            raise
    
    def stop_driver(self) -> None:
        """
        Detiene el driver WinAppDriver.
        """
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("WinAppDriver detenido exitosamente")
        except Exception as e:
            self.logger.error(f"Error al detener WinAppDriver: {str(e)}")
    
    def find_element_by_automation_id(self, automation_id: str):
        """
        Encuentra un elemento por su AutomationId.
        
        Args:
            automation_id: ID de automatización del elemento
            
        Returns:
            WebElement: Elemento encontrado
        """
        return self.wait.until(
            EC.presence_of_element_located((By.NAME, automation_id))
        )
    
    def find_element_by_name(self, name: str):
        """
        Encuentra un elemento por su nombre.
        
        Args:
            name: Nombre del elemento
            
        Returns:
            WebElement: Elemento encontrado
        """
        return self.wait.until(
            EC.presence_of_element_located((By.NAME, name))
        )
    
    def find_element_by_class_name(self, class_name: str):
        """
        Encuentra un elemento por su clase.
        
        Args:
            class_name: Nombre de la clase del elemento
            
        Returns:
            WebElement: Elemento encontrado
        """
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
    
    def get_driver(self) -> webdriver.Remote:
        """
        Obtiene la instancia del driver.
        
        Returns:
            webdriver.Remote: Instancia del driver actual
        """
        if not self.driver:
            raise RuntimeError("Driver no inicializado. Llamar start_driver() primero.")
        return self.driver
    
    def get_wait(self) -> WebDriverWait:
        """
        Obtiene la instancia de WebDriverWait.
        
        Returns:
            WebDriverWait: Instancia de wait configurada
        """
        if not self.wait:
            raise RuntimeError("Wait no inicializado. Llamar start_driver() primero.")
        return self.wait
