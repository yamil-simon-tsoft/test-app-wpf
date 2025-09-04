# Especificación de ejemplo para automatización WPF

Esta especificación demuestra cómo escribir pruebas en lenguaje natural usando Gauge.

## Configuración inicial de la aplicación

* Abrir la aplicación WPF
* Verificar que la ventana principal está visible
* Tomar captura de pantalla inicial

## Login con credenciales válidas

* Introducir usuario "admin" en el campo de usuario
* Introducir contraseña "admin123" en el campo de contraseña
* Hacer clic en el botón "Iniciar Sesión"
* Verificar que el login fue exitoso
* Tomar captura de pantalla del login exitoso

## Login con credenciales inválidas

* Introducir usuario "usuario_invalido" en el campo de usuario
* Introducir contraseña "contraseña_incorrecta" en el campo de contraseña
* Hacer clic en el botón "Iniciar Sesión"
* Verificar que aparece un mensaje de error
* Verificar que el mensaje contiene "Usuario o contraseña incorrectos"
* Tomar captura de pantalla del error

## Validación de campos obligatorios

* Dejar vacío el campo de usuario
* Dejar vacío el campo de contraseña
* Hacer clic en el botón "Iniciar Sesión"
* Verificar que aparece un mensaje de validación
* Verificar que no se permite el acceso al sistema

## Cerrar la aplicación

* Cerrar la aplicación correctamente
* Verificar que todos los recursos se han liberado
