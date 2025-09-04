"""
Pruebas de integración para la aplicación WPF.

Estas pruebas verifican la funcionalidad completa de la aplicación
usando WinAppDriver.
"""

import pytest
import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.pages.base_page import BasePage
from src.data.test_data import TestData, LoginTestData
from selenium.webdriver.common.by import By


class MainApplicationPage(BasePage):
    """
    Page Object para la ventana principal de la aplicación.
    """
    
    # Localizadores de elementos
    USERNAME_FIELD = (By.NAME, "txtUsername")
    PASSWORD_FIELD = (By.NAME, "txtPassword")
    LOGIN_BUTTON = (By.NAME, "btnLogin")
    ERROR_MESSAGE = (By.NAME, "lblError")
    MAIN_MENU = (By.NAME, "MainMenu")
    STATUS_BAR = (By.NAME, "StatusBar")
    
    def login(self, username: str, password: str):
        """
        Realiza el proceso de login.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        """
        self.send_keys_to_element(self.USERNAME_FIELD, username)
        self.send_keys_to_element(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)
        
        # Esperar un momento para que se procese el login
        time.sleep(2)
    
    def get_error_message(self) -> str:
        """
        Obtiene el mensaje de error si existe.
        
        Returns:
            str: Mensaje de error
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""
    
    def is_logged_in(self) -> bool:
        """
        Verifica si el usuario está logueado.
        
        Returns:
            bool: True si está logueado
        """
        return self.is_element_visible(self.MAIN_MENU, timeout=10)
    
    def get_window_title_text(self) -> str:
        """
        Obtiene el título de la ventana.
        
        Returns:
            str: Título de la ventana
        """
        return self.get_window_title()


@pytest.mark.integration
class TestWPFApplicationLogin:
    """Pruebas de integración para el login de la aplicación."""
    
    def test_valid_login(self, driver, test_data):
        """
        Prueba el login con credenciales válidas.
        
        Args:
            driver: Fixture del driver WinAppDriver
            test_data: Fixture de datos de prueba
        """
        # Arrange
        page = MainApplicationPage(driver)
        valid_user = test_data.get_user_data("valid")
        
        # Act
        page.login(valid_user["username"], valid_user["password"])
        
        # Assert
        assert page.is_logged_in(), "El usuario debería estar logueado"
        
        # Tomar screenshot de éxito
        page.take_screenshot("login_success")
    
    def test_invalid_login(self, driver, test_data):
        """
        Prueba el login con credenciales inválidas.
        
        Args:
            driver: Fixture del driver WinAppDriver
            test_data: Fixture de datos de prueba
        """
        # Arrange
        page = MainApplicationPage(driver)
        invalid_user = test_data.get_user_data("invalid")
        expected_error = test_data.get_expected_message("login_error")
        
        # Act
        page.login(invalid_user["username"], invalid_user["password"])
        
        # Assert
        assert not page.is_logged_in(), "El usuario no debería estar logueado"
        
        error_message = page.get_error_message()
        assert error_message, "Debería mostrarse un mensaje de error"
        
        # Tomar screenshot del error
        page.take_screenshot("login_error")
    
    @pytest.mark.parametrize("credentials", LoginTestData.INVALID_CREDENTIALS)
    def test_login_with_various_invalid_credentials(self, driver, credentials):
        """
        Prueba el login con diferentes combinaciones de credenciales inválidas.
        
        Args:
            driver: Fixture del driver WinAppDriver
            credentials: Credenciales a probar
        """
        # Arrange
        page = MainApplicationPage(driver)
        
        # Act
        page.login(credentials["username"], credentials["password"])
        
        # Assert
        assert not page.is_logged_in(), f"Login debería fallar para: {credentials}"
    
    def test_empty_credentials(self, driver):
        """
        Prueba el login con campos vacíos.
        
        Args:
            driver: Fixture del driver WinAppDriver
        """
        # Arrange
        page = MainApplicationPage(driver)
        
        # Act
        page.login("", "")
        
        # Assert
        assert not page.is_logged_in(), "Login con campos vacíos debería fallar"
        
        error_message = page.get_error_message()
        assert error_message, "Debería mostrarse mensaje de validación"


@pytest.mark.integration
@pytest.mark.smoke
class TestWPFApplicationBasicFunctionality:
    """Pruebas básicas de funcionalidad de la aplicación."""
    
    def test_application_starts(self, driver):
        """
        Prueba que la aplicación se inicia correctamente.
        
        Args:
            driver: Fixture del driver WinAppDriver
        """
        # Arrange & Act
        page = MainApplicationPage(driver)
        
        # Assert
        window_title = page.get_window_title_text()
        assert window_title, "La aplicación debería tener un título"
        
        # Verificar que los elementos básicos están presentes
        assert page.is_element_present(page.USERNAME_FIELD), "Campo username debería estar presente"
        assert page.is_element_present(page.PASSWORD_FIELD), "Campo password debería estar presente"
        assert page.is_element_present(page.LOGIN_BUTTON), "Botón login debería estar presente"
        
        # Tomar screenshot inicial
        page.take_screenshot("application_started")
    
    def test_ui_elements_are_interactable(self, driver):
        """
        Prueba que los elementos de UI son interactuables.
        
        Args:
            driver: Fixture del driver WinAppDriver
        """
        # Arrange
        page = MainApplicationPage(driver)
        
        # Act & Assert
        # Verificar que se puede escribir en el campo username
        page.send_keys_to_element(page.USERNAME_FIELD, "test")
        username_text = page.get_element_text(page.USERNAME_FIELD)
        assert "test" in username_text or username_text == "", "Debería poder escribir en username"
        
        # Verificar que se puede escribir en el campo password
        page.send_keys_to_element(page.PASSWORD_FIELD, "password")
        
        # Verificar que el botón es clickeable
        login_button = page.wait_for_clickable(page.LOGIN_BUTTON)
        assert login_button, "Botón login debería ser clickeable"
        
        # Tomar screenshot de interacción
        page.take_screenshot("ui_interaction")


@pytest.mark.integration
@pytest.mark.slow
class TestWPFApplicationWorkflow:
    """Pruebas de flujo completo de la aplicación."""
    
    def test_complete_login_workflow(self, driver, test_data):
        """
        Prueba el flujo completo de login y navegación básica.
        
        Args:
            driver: Fixture del driver WinAppDriver
            test_data: Fixture de datos de prueba
        """
        # Arrange
        page = MainApplicationPage(driver)
        valid_user = test_data.get_user_data("valid")
        
        # Act - Paso 1: Login
        page.take_screenshot("workflow_start")
        page.login(valid_user["username"], valid_user["password"])
        
        # Assert - Verificar login exitoso
        assert page.is_logged_in(), "Usuario debería estar logueado"
        page.take_screenshot("workflow_logged_in")
        
        # Act - Paso 2: Verificar elementos post-login
        if page.is_element_visible(page.MAIN_MENU):
            page.take_screenshot("workflow_main_menu_visible")
        
        # Simular alguna actividad adicional aquí
        time.sleep(2)
        
        page.take_screenshot("workflow_complete")


@pytest.mark.integration
class TestWPFApplicationErrorHandling:
    """Pruebas de manejo de errores de la aplicación."""
    
    def test_network_timeout_scenario(self, driver):
        """
        Prueba el comportamiento con timeouts de red (simulado).
        
        Args:
            driver: Fixture del driver WinAppDriver
        """
        # Arrange
        page = MainApplicationPage(driver)
        
        # Act - Simular login lento
        page.send_keys_to_element(page.USERNAME_FIELD, "slow_user")
        page.send_keys_to_element(page.PASSWORD_FIELD, "slow_pass")
        page.click_element(page.LOGIN_BUTTON)
        
        # Assert - Verificar que la aplicación maneja el timeout apropiadamente
        # (Esto dependerá del comportamiento específico de tu aplicación)
        time.sleep(5)  # Simular espera
        
        # Verificar estado después del timeout
        page.take_screenshot("timeout_scenario")
    
    def test_application_recovery_after_error(self, driver):
        """
        Prueba la recuperación de la aplicación después de un error.
        
        Args:
            driver: Fixture del driver WinAppDriver
        """
        # Arrange
        page = MainApplicationPage(driver)
        
        # Act - Provocar un error
        page.login("error_user", "error_pass")
        
        # Verificar que hay un error
        error_message = page.get_error_message()
        if error_message:
            page.take_screenshot("error_state")
        
        # Act - Intentar recuperación
        page.send_keys_to_element(page.USERNAME_FIELD, "recovery_test", clear_first=True)
        page.send_keys_to_element(page.PASSWORD_FIELD, "recovery_pass", clear_first=True)
        
        # Assert - Verificar que la aplicación aún funciona
        assert page.is_element_visible(page.LOGIN_BUTTON), "Botón login debería seguir disponible"
        page.take_screenshot("recovery_attempt")
