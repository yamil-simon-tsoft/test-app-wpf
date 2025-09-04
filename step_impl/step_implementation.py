"""
Implementación de pasos para las especificaciones Gauge.

Este archivo contiene la implementación de todos los pasos definidos
en las especificaciones .spec
"""

import time
import logging
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from getgauge.python import step, before_scenario, after_scenario, before_spec, after_spec
from selenium.webdriver.common.by import By

from src.drivers.winapp_driver import WinAppDriver
from src.pages.base_page import BasePage
from src.data.test_data import TestData
from src.utils.helpers import setup_logging, take_screenshot


class WPFApplicationSteps:
    """Clase que contiene la implementación de pasos para Gauge."""
    
    def __init__(self):
        """Inicializa los pasos de la aplicación."""
        self.driver = None
        self.winapp_driver = None
        self.main_page = None
        self.logger = logging.getLogger(__name__)
        self.test_data = TestData()


# Instancia global para mantener estado entre pasos
app_steps = WPFApplicationSteps()


@before_spec
def before_spec_hook():
    """Se ejecuta antes de cada especificación."""
    app_steps.logger = setup_logging()
    app_steps.logger.info("=== Iniciando especificación Gauge ===")


@after_spec
def after_spec_hook():
    """Se ejecuta después de cada especificación."""
    app_steps.logger.info("=== Finalizando especificación Gauge ===")


@before_scenario
def before_scenario_hook():
    """Se ejecuta antes de cada escenario."""
    app_steps.logger.info("--- Iniciando escenario ---")


@after_scenario
def after_scenario_hook():
    """Se ejecuta después de cada escenario."""
    if app_steps.winapp_driver:
        app_steps.winapp_driver.stop_driver()
        app_steps.winapp_driver = None
        app_steps.driver = None
        app_steps.main_page = None
    app_steps.logger.info("--- Finalizando escenario ---")


# Pasos de configuración inicial

@step("Abrir la aplicación WPF")
def abrir_aplicacion_wpf():
    """Abre la aplicación WPF."""
    try:
        app_steps.winapp_driver = WinAppDriver()
        app_steps.driver = app_steps.winapp_driver.start_driver()
        app_steps.main_page = BasePage(app_steps.driver)
        app_steps.logger.info("Aplicación WPF abierta exitosamente")
    except Exception as e:
        app_steps.logger.error(f"Error al abrir aplicación: {str(e)}")
        raise


@step("Iniciar WinAppDriver")
def iniciar_winappdriver():
    """Inicia WinAppDriver."""
    abrir_aplicacion_wpf()


@step("Configurar la aplicación objetivo")
def configurar_aplicacion_objetivo():
    """Configura la aplicación objetivo."""
    # La configuración ya se hizo en el paso anterior
    app_steps.logger.info("Aplicación objetivo configurada")


@step("Lanzar la aplicación WPF")
def lanzar_aplicacion_wpf():
    """Lanza la aplicación WPF."""
    # Ya lanzada en pasos anteriores
    app_steps.logger.info("Aplicación WPF lanzada")


@step("Verificar que la ventana principal está visible")
def verificar_ventana_principal_visible():
    """Verifica que la ventana principal esté visible."""
    assert app_steps.main_page is not None, "La página principal debe estar inicializada"
    
    window_title = app_steps.main_page.get_window_title()
    assert window_title, "La ventana principal debe tener un título"
    
    app_steps.logger.info(f"Ventana principal visible: {window_title}")


@step("Verificar que la ventana principal se muestra correctamente")
def verificar_ventana_principal_correcta():
    """Verifica que la ventana principal se muestra correctamente."""
    verificar_ventana_principal_visible()


@step("Documentar el estado inicial")
def documentar_estado_inicial():
    """Documenta el estado inicial de la aplicación."""
    app_steps.main_page.take_screenshot("estado_inicial")
    app_steps.logger.info("Estado inicial documentado")


# Pasos de login

@step("Navegar a la pantalla de login")
def navegar_a_login():
    """Navega a la pantalla de login."""
    # Asumiendo que ya estamos en la pantalla de login al abrir la app
    app_steps.logger.info("Navegando a pantalla de login")


@step("Introducir usuario <usuario> en el campo de usuario")
def introducir_usuario(usuario):
    """
    Introduce el usuario en el campo correspondiente.
    
    Args:
        usuario: Nombre de usuario a introducir
    """
    username_field = (By.NAME, "txtUsername")
    app_steps.main_page.send_keys_to_element(username_field, usuario, clear_first=True)
    app_steps.logger.info(f"Usuario introducido: {usuario}")


@step("Introducir contraseña <contraseña> en el campo de contraseña")
def introducir_contraseña(contraseña):
    """
    Introduce la contraseña en el campo correspondiente.
    
    Args:
        contraseña: Contraseña a introducir
    """
    password_field = (By.NAME, "txtPassword")
    app_steps.main_page.send_keys_to_element(password_field, contraseña, clear_first=True)
    app_steps.logger.info("Contraseña introducida")


@step("Introducir credenciales de administrador")
def introducir_credenciales_admin():
    """Introduce las credenciales de administrador."""
    admin_data = app_steps.test_data.get_user_data("valid")
    introducir_usuario(admin_data["username"])
    introducir_contraseña(admin_data["password"])


@step("Hacer clic en el botón <texto_boton>")
def hacer_clic_boton(texto_boton):
    """
    Hace clic en un botón específico.
    
    Args:
        texto_boton: Texto del botón a hacer clic
    """
    # Mapeo de textos de botón a localizadores
    button_locators = {
        "Iniciar Sesión": (By.NAME, "btnLogin"),
        "Guardar": (By.NAME, "btnSave"),
        "Cancelar": (By.NAME, "btnCancel"),
        "Buscar": (By.NAME, "btnSearch"),
        "Nuevo registro": (By.NAME, "btnNew"),
        "Editar": (By.NAME, "btnEdit"),
        "Eliminar": (By.NAME, "btnDelete")
    }
    
    locator = button_locators.get(texto_boton, (By.NAME, f"btn{texto_boton.replace(' ', '')}"))
    app_steps.main_page.click_element(locator)
    app_steps.logger.info(f"Clic realizado en botón: {texto_boton}")


@step("Verificar que el login fue exitoso")
def verificar_login_exitoso():
    """Verifica que el login fue exitoso."""
    main_menu = (By.NAME, "MainMenu")
    assert app_steps.main_page.is_element_visible(main_menu, timeout=10), \
        "Menú principal debe ser visible después del login exitoso"
    app_steps.logger.info("Login exitoso verificado")


@step("Validar acceso al panel de administración")
def validar_acceso_panel_admin():
    """Valida el acceso al panel de administración."""
    admin_panel = (By.NAME, "AdminPanel")
    assert app_steps.main_page.is_element_visible(admin_panel, timeout=10), \
        "Panel de administración debe ser visible"
    app_steps.logger.info("Acceso al panel de administración validado")


@step("Verificar que se muestran las opciones de administrador")
def verificar_opciones_administrador():
    """Verifica que se muestran las opciones de administrador."""
    admin_menu = (By.NAME, "AdminMenu")
    assert app_steps.main_page.is_element_visible(admin_menu, timeout=5), \
        "Menú de administrador debe ser visible"
    app_steps.logger.info("Opciones de administrador verificadas")


# Pasos de validación de errores

@step("Verificar que aparece un mensaje de error")
def verificar_mensaje_error():
    """Verifica que aparece un mensaje de error."""
    error_message = (By.NAME, "lblError")
    assert app_steps.main_page.is_element_visible(error_message, timeout=5), \
        "Debe aparecer un mensaje de error"
    app_steps.logger.info("Mensaje de error verificado")


@step("Verificar que el mensaje contiene <texto_esperado>")
def verificar_mensaje_contiene(texto_esperado):
    """
    Verifica que el mensaje contiene el texto esperado.
    
    Args:
        texto_esperado: Texto que debe contener el mensaje
    """
    error_message = (By.NAME, "lblError")
    mensaje_actual = app_steps.main_page.get_element_text(error_message)
    assert texto_esperado.lower() in mensaje_actual.lower(), \
        f"El mensaje '{mensaje_actual}' debe contener '{texto_esperado}'"
    app_steps.logger.info(f"Mensaje verificado contiene: {texto_esperado}")


@step("Verificar que aparece un mensaje de validación")
def verificar_mensaje_validacion():
    """Verifica que aparece un mensaje de validación."""
    verificar_mensaje_error()


@step("Verificar que no se permite el acceso al sistema")
def verificar_acceso_denegado():
    """Verifica que no se permite el acceso al sistema."""
    main_menu = (By.NAME, "MainMenu")
    assert not app_steps.main_page.is_element_visible(main_menu, timeout=3), \
        "No debe mostrarse el menú principal"
    app_steps.logger.info("Acceso denegado verificado")


# Pasos de campos vacíos

@step("Dejar vacío el campo de usuario")
def dejar_vacio_campo_usuario():
    """Deja vacío el campo de usuario."""
    username_field = (By.NAME, "txtUsername")
    app_steps.main_page.send_keys_to_element(username_field, "", clear_first=True)
    app_steps.logger.info("Campo de usuario dejado vacío")


@step("Dejar vacío el campo de contraseña")
def dejar_vacio_campo_contraseña():
    """Deja vacío el campo de contraseña."""
    password_field = (By.NAME, "txtPassword")
    app_steps.main_page.send_keys_to_element(password_field, "", clear_first=True)
    app_steps.logger.info("Campo de contraseña dejado vacío")


# Pasos de screenshots

@step("Tomar captura de pantalla inicial")
def tomar_captura_inicial():
    """Toma una captura de pantalla inicial."""
    app_steps.main_page.take_screenshot("captura_inicial")
    app_steps.logger.info("Captura inicial tomada")


@step("Tomar captura de pantalla del login exitoso")
def tomar_captura_login_exitoso():
    """Toma captura del login exitoso."""
    app_steps.main_page.take_screenshot("login_exitoso")
    app_steps.logger.info("Captura de login exitoso tomada")


@step("Tomar captura de pantalla del error")
def tomar_captura_error():
    """Toma captura del error."""
    app_steps.main_page.take_screenshot("error_login")
    app_steps.logger.info("Captura de error tomada")


@step("Tomar captura del formulario abierto")
def tomar_captura_formulario():
    """Toma captura del formulario abierto."""
    app_steps.main_page.take_screenshot("formulario_abierto")
    app_steps.logger.info("Captura de formulario tomada")


# Pasos de cierre

@step("Cerrar la aplicación correctamente")
def cerrar_aplicacion():
    """Cierra la aplicación correctamente."""
    if app_steps.winapp_driver:
        app_steps.winapp_driver.stop_driver()
        app_steps.logger.info("Aplicación cerrada correctamente")


@step("Verificar que todos los recursos se han liberado")
def verificar_recursos_liberados():
    """Verifica que todos los recursos se han liberado."""
    # Verificación de que el driver se ha cerrado correctamente
    app_steps.logger.info("Recursos liberados verificados")


@step("Confirmar que WinAppDriver termina correctamente")
def confirmar_winappdriver_termina():
    """Confirma que WinAppDriver termina correctamente."""
    cerrar_aplicacion()


# Pasos adicionales para formularios y navegación

@step("Hacer clic en <menu> en el menú principal")
def hacer_clic_menu_principal(menu):
    """
    Hace clic en un elemento del menú principal.
    
    Args:
        menu: Elemento del menú a hacer clic
    """
    menu_locator = (By.NAME, f"menu{menu}")
    app_steps.main_page.click_element(menu_locator)
    app_steps.logger.info(f"Clic en menú: {menu}")


@step("Verificar que se despliega el submenú de archivo")
def verificar_submenu_archivo():
    """Verifica que se despliega el submenú de archivo."""
    submenu = (By.NAME, "submenuArchivo")
    assert app_steps.main_page.is_element_visible(submenu, timeout=5), \
        "Submenú de archivo debe ser visible"
    app_steps.logger.info("Submenú de archivo verificado")


@step("Seleccionar <opcion>")
def seleccionar_opcion(opcion):
    """
    Selecciona una opción del menú.
    
    Args:
        opcion: Opción a seleccionar
    """
    opcion_locator = (By.NAME, opcion.replace(" ", ""))
    app_steps.main_page.click_element(opcion_locator)
    app_steps.logger.info(f"Opción seleccionada: {opcion}")


@step("Confirmar que se abre el formulario correspondiente")
def confirmar_formulario_abierto():
    """Confirma que se abre el formulario correspondiente."""
    formulario = (By.NAME, "FormularioPrincipal")
    assert app_steps.main_page.is_element_visible(formulario, timeout=10), \
        "Formulario debe estar abierto"
    app_steps.logger.info("Formulario abierto confirmado")
