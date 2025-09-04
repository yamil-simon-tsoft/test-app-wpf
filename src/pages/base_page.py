"""
Clase base para implementar el patrón Page Object Model.

Esta clase proporciona funcionalidades comunes para todas las páginas
de la aplicación WPF.
"""

import logging
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.config import config
from src.utils.helpers import take_screenshot


class BasePage:
    """
    Clase base para todas las páginas usando Page Object Model.
    """
    
    def __init__(self, driver):
        """
        Inicializa la página base.
        
        Args:
            driver: Instancia del driver WinAppDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get_explicit_wait())
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def find_element(self, locator: tuple, timeout: Optional[int] = None):
        """
        Encuentra un elemento en la página.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            timeout: Tiempo de espera personalizado
        
        Returns:
            WebElement: Elemento encontrado
        """
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                return wait.until(EC.presence_of_element_located(locator))
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Elemento no encontrado: {locator}")
            self.take_screenshot(f"element_not_found_{locator[1]}")
            raise
    
    def find_elements(self, locator: tuple) -> List:
        """
        Encuentra múltiples elementos en la página.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
        
        Returns:
            List: Lista de elementos encontrados
        """
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            self.logger.warning(f"Elementos no encontrados: {locator}")
            return []
    
    def click_element(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """
        Hace clic en un elemento.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            timeout: Tiempo de espera personalizado
        """
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
            self.logger.info(f"Clic realizado en elemento: {locator}")
        except Exception as e:
            self.logger.error(f"Error al hacer clic en elemento {locator}: {str(e)}")
            self.take_screenshot(f"click_error_{locator[1]}")
            raise
    
    def send_keys_to_element(self, locator: tuple, text: str, clear_first: bool = True) -> None:
        """
        Envía texto a un elemento.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            text: Texto a enviar
            clear_first: Si limpiar el campo antes de escribir
        """
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Texto enviado a elemento {locator}: {text}")
        except Exception as e:
            self.logger.error(f"Error al enviar texto a elemento {locator}: {str(e)}")
            self.take_screenshot(f"send_keys_error_{locator[1]}")
            raise
    
    def get_element_text(self, locator: tuple) -> str:
        """
        Obtiene el texto de un elemento.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
        
        Returns:
            str: Texto del elemento
        """
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.info(f"Texto obtenido de elemento {locator}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error al obtener texto de elemento {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Verifica si un elemento es visible.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            timeout: Tiempo de espera
        
        Returns:
            bool: True si el elemento es visible
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator: tuple) -> bool:
        """
        Verifica si un elemento está presente en el DOM.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
        
        Returns:
            bool: True si el elemento está presente
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_clickable(self, locator: tuple, timeout: Optional[int] = None):
        """
        Espera a que un elemento sea clickeable.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            timeout: Tiempo de espera personalizado
        
        Returns:
            WebElement: Elemento clickeable
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_element_to_disappear(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """
        Espera a que un elemento desaparezca.
        
        Args:
            locator: Tupla con el tipo y valor del localizador
            timeout: Tiempo de espera personalizado
        
        Returns:
            bool: True si el elemento desapareció
        """
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                wait.until_not(EC.presence_of_element_located(locator))
            else:
                self.wait.until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator: tuple) -> None:
        """
        Hace scroll hacia un elemento (si es aplicable en WPF).
        
        Args:
            locator: Tupla con el tipo y valor del localizador
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.logger.info(f"Scroll realizado hacia elemento: {locator}")
        except Exception as e:
            self.logger.warning(f"No se pudo hacer scroll hacia elemento {locator}: {str(e)}")
    
    def take_screenshot(self, step_name: str) -> str:
        """
        Toma una captura de pantalla.
        
        Args:
            step_name: Nombre del paso actual
        
        Returns:
            str: Ruta del archivo de screenshot
        """
        test_name = self.__class__.__name__
        return take_screenshot(self.driver, test_name, step_name)
    
    def get_window_title(self) -> str:
        """
        Obtiene el título de la ventana actual.
        
        Returns:
            str: Título de la ventana
        """
        try:
            return self.driver.title
        except Exception as e:
            self.logger.error(f"Error al obtener título de ventana: {str(e)}")
            return ""
    
    def switch_to_window(self, window_handle: str) -> None:
        """
        Cambia a una ventana específica.
        
        Args:
            window_handle: Handle de la ventana
        """
        try:
            self.driver.switch_to.window(window_handle)
            self.logger.info(f"Cambiado a ventana: {window_handle}")
        except Exception as e:
            self.logger.error(f"Error al cambiar a ventana {window_handle}: {str(e)}")
            raise
    
    def close_current_window(self) -> None:
        """
        Cierra la ventana actual.
        """
        try:
            self.driver.close()
            self.logger.info("Ventana actual cerrada")
        except Exception as e:
            self.logger.error(f"Error al cerrar ventana: {str(e)}")
            raise
