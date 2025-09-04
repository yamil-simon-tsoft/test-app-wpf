"""
Datos de prueba para la aplicación WPF.

Este módulo contiene todos los datos necesarios para ejecutar
las pruebas automatizadas.
"""

from typing import Dict, Any


class TestData:
    """
    Clase que contiene todos los datos de prueba.
    """
    
    # Datos de usuario para pruebas
    VALID_USER = {
        "username": "testuser",
        "password": "testpass123",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    
    INVALID_USER = {
        "username": "invaliduser",
        "password": "wrongpass",
        "email": "invalid@email"
    }
    
    # Datos para formularios
    FORM_DATA = {
        "text_field": "Texto de prueba",
        "number_field": 12345,
        "date_field": "2025-01-01",
        "dropdown_option": "Opción 1",
        "checkbox_value": True,
        "radio_button": "option2"
    }
    
    # Configuración de elementos UI
    UI_ELEMENTS = {
        "main_window": {
            "title": "Aplicación WPF - Test",
            "class_name": "Window"
        },
        "login_form": {
            "username_field": "txtUsername",
            "password_field": "txtPassword",
            "login_button": "btnLogin",
            "error_message": "lblError"
        },
        "main_menu": {
            "file_menu": "menuFile",
            "edit_menu": "menuEdit",
            "help_menu": "menuHelp"
        }
    }
    
    # Mensajes esperados
    EXPECTED_MESSAGES = {
        "login_success": "Bienvenido al sistema",
        "login_error": "Usuario o contraseña incorrectos",
        "validation_error": "Por favor complete todos los campos",
        "save_success": "Datos guardados correctamente",
        "delete_confirmation": "¿Está seguro de eliminar este elemento?"
    }
    
    # URLs y rutas de archivos
    TEST_FILES = {
        "sample_document": r"C:\TestData\sample.pdf",
        "test_image": r"C:\TestData\test_image.png",
        "config_file": r"C:\TestData\config.xml"
    }
    
    # Configuración de base de datos (si aplica)
    DATABASE = {
        "connection_string": "Data Source=test.db;Version=3;",
        "test_table": "TestUsers",
        "backup_file": "test_backup.db"
    }
    
    @classmethod
    def get_user_data(cls, user_type: str = "valid") -> Dict[str, Any]:
        """
        Obtiene datos de usuario según el tipo.
        
        Args:
            user_type: Tipo de usuario ('valid' o 'invalid')
        
        Returns:
            Dict: Datos del usuario
        """
        if user_type == "valid":
            return cls.VALID_USER.copy()
        elif user_type == "invalid":
            return cls.INVALID_USER.copy()
        else:
            raise ValueError(f"Tipo de usuario no válido: {user_type}")
    
    @classmethod
    def get_form_data(cls) -> Dict[str, Any]:
        """
        Obtiene datos para formularios.
        
        Returns:
            Dict: Datos del formulario
        """
        return cls.FORM_DATA.copy()
    
    @classmethod
    def get_ui_element(cls, section: str, element: str = None) -> Any:
        """
        Obtiene configuración de elementos UI.
        
        Args:
            section: Sección del elemento
            element: Elemento específico (opcional)
        
        Returns:
            Any: Configuración del elemento
        """
        if element:
            return cls.UI_ELEMENTS.get(section, {}).get(element)
        return cls.UI_ELEMENTS.get(section, {})
    
    @classmethod
    def get_expected_message(cls, message_type: str) -> str:
        """
        Obtiene mensaje esperado según el tipo.
        
        Args:
            message_type: Tipo de mensaje
        
        Returns:
            str: Mensaje esperado
        """
        return cls.EXPECTED_MESSAGES.get(message_type, "")
    
    @classmethod
    def get_test_file_path(cls, file_type: str) -> str:
        """
        Obtiene ruta de archivo de prueba.
        
        Args:
            file_type: Tipo de archivo
        
        Returns:
            str: Ruta del archivo
        """
        return cls.TEST_FILES.get(file_type, "")


# Datos específicos para diferentes tipos de pruebas
class LoginTestData:
    """Datos específicos para pruebas de login."""
    
    VALID_CREDENTIALS = [
        {"username": "admin", "password": "admin123"},
        {"username": "user1", "password": "pass123"},
        {"username": "test@example.com", "password": "testpass"}
    ]
    
    INVALID_CREDENTIALS = [
        {"username": "", "password": ""},
        {"username": "admin", "password": "wrongpass"},
        {"username": "nonexistent", "password": "anypass"},
        {"username": "admin", "password": ""}
    ]


class FormTestData:
    """Datos específicos para pruebas de formularios."""
    
    VALID_FORM_DATA = {
        "personal_info": {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@email.com",
            "phone": "+34 123 456 789",
            "birth_date": "01/01/1990"
        },
        "address_info": {
            "street": "Calle Principal 123",
            "city": "Madrid",
            "postal_code": "28001",
            "country": "España"
        }
    }
    
    INVALID_FORM_DATA = {
        "invalid_email": "email-invalido",
        "invalid_phone": "123",
        "empty_required": "",
        "special_chars": "!@#$%^&*()"
    }
