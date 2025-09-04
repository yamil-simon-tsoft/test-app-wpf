"""
Pruebas unitarias para las utilidades del proyecto.

Estas pruebas verifican que las funciones auxiliares 
funcionan correctamente.
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.utils.config import Config
from src.utils.helpers import (
    generate_test_data_filename,
    get_project_root,
    retry_on_failure
)


class TestConfig:
    """Pruebas para la clase Config."""
    
    def test_config_initialization(self):
        """Prueba la inicialización de la configuración."""
        config = Config()
        
        assert config.get_winappdriver_url() == 'http://127.0.0.1:4723'
        assert config.get_implicit_wait() == 10
        assert config.get_explicit_wait() == 20
        assert config.get_retry_count() == 3
    
    def test_set_app_path(self):
        """Prueba el establecimiento de la ruta de la aplicación."""
        config = Config()
        test_path = r"C:\Test\App.exe"
        
        config.set_app_path(test_path)
        
        assert config.get_app_path() == test_path
    
    def test_create_directories(self):
        """Prueba la creación de directorios."""
        config = Config()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config.REPORTS_DIR = os.path.join(temp_dir, "reports")
            config.SCREENSHOTS_DIR = os.path.join(temp_dir, "screenshots")
            
            config.create_directories()
            
            assert os.path.exists(config.REPORTS_DIR)
            assert os.path.exists(config.SCREENSHOTS_DIR)


class TestHelpers:
    """Pruebas para las funciones auxiliares."""
    
    def test_generate_test_data_filename(self):
        """Prueba la generación de nombres de archivo."""
        test_name = "login_test"
        filename = generate_test_data_filename(test_name)
        
        assert test_name in filename
        assert filename.endswith(".json")
        assert "data" in filename
    
    def test_generate_test_data_filename_custom_extension(self):
        """Prueba la generación con extensión personalizada."""
        test_name = "form_test"
        extension = "xml"
        filename = generate_test_data_filename(test_name, extension)
        
        assert filename.endswith(f".{extension}")
    
    def test_get_project_root(self):
        """Prueba la obtención de la ruta raíz del proyecto."""
        root = get_project_root()
        
        assert isinstance(root, Path)
        assert root.exists()
    
    def test_retry_decorator_success(self):
        """Prueba el decorador de reintentos con éxito."""
        call_count = 0
        
        @retry_on_failure(max_retries=3)
        def test_function():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = test_function()
        
        assert result == "success"
        assert call_count == 1
    
    def test_retry_decorator_failure_then_success(self):
        """Prueba el decorador con fallo inicial y luego éxito."""
        call_count = 0
        
        @retry_on_failure(max_retries=3)
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = test_function()
        
        assert result == "success"
        assert call_count == 3
    
    def test_retry_decorator_max_retries_exceeded(self):
        """Prueba el decorador cuando se exceden los reintentos."""
        call_count = 0
        
        @retry_on_failure(max_retries=2)
        def test_function():
            nonlocal call_count
            call_count += 1
            raise Exception("Persistent failure")
        
        with pytest.raises(Exception, match="Persistent failure"):
            test_function()
        
        assert call_count == 3  # 1 intento inicial + 2 reintentos


class TestConfigEnvironmentVariables:
    """Pruebas para variables de entorno en la configuración."""
    
    @patch.dict(os.environ, {
        'WINAPPDRIVER_URL': 'http://custom-url:4724',
        'IMPLICIT_WAIT': '15',
        'EXPLICIT_WAIT': '25'
    })
    def test_config_with_environment_variables(self):
        """Prueba la configuración con variables de entorno."""
        config = Config()
        
        assert config.get_winappdriver_url() == 'http://custom-url:4724'
        assert config.get_implicit_wait() == 15
        assert config.get_explicit_wait() == 25
    
    @patch.dict(os.environ, {'HEADLESS': 'true'})
    def test_headless_mode_true(self):
        """Prueba el modo headless activado."""
        config = Config()
        
        assert config.is_headless() is True
    
    @patch.dict(os.environ, {'HEADLESS': 'false'})
    def test_headless_mode_false(self):
        """Prueba el modo headless desactivado."""
        config = Config()
        
        assert config.is_headless() is False


@pytest.mark.parametrize("test_name,extension,expected_pattern", [
    ("login", "json", r"login_data_\d{8}_\d{6}\.json"),
    ("form_validation", "xml", r"form_validation_data_\d{8}_\d{6}\.xml"),
    ("user_management", "csv", r"user_management_data_\d{8}_\d{6}\.csv"),
])
def test_filename_generation_patterns(test_name, extension, expected_pattern):
    """Prueba patrones de generación de nombres de archivo."""
    import re
    
    filename = generate_test_data_filename(test_name, extension)
    
    assert re.match(expected_pattern, filename)


class TestIntegrationHelpers:
    """Pruebas de integración para las funciones auxiliares."""
    
    def test_full_workflow_config_and_helpers(self):
        """Prueba un flujo completo usando config y helpers."""
        # Inicializar configuración
        config = Config()
        config.set_app_path(r"C:\TestApp\MyApp.exe")
        
        # Generar nombre de archivo de prueba
        test_name = "integration_test"
        filename = generate_test_data_filename(test_name)
        
        # Verificar que todo funciona junto
        assert config.get_app_path() == r"C:\TestApp\MyApp.exe"
        assert test_name in filename
        assert isinstance(get_project_root(), Path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
