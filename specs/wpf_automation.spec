# Automatización de Aplicación WPF

Esta especificación contiene escenarios de prueba para automatizar una aplicación WPF.

## Inicialización de la aplicación

### Escenario: Arranque exitoso de la aplicación
* Iniciar WinAppDriver
* Configurar la aplicación objetivo
* Lanzar la aplicación WPF
* Verificar que la ventana principal se muestra correctamente
* Documentar el estado inicial

## Gestión de usuarios

### Escenario: Login de usuario administrador
* Navegar a la pantalla de login
* Introducir credenciales de administrador
    |usuario|contraseña|
    |-------|----------|
    |admin  |admin123  |
* Hacer clic en "Iniciar Sesión"
* Validar acceso al panel de administración
* Verificar que se muestran las opciones de administrador

### Escenario: Login con múltiples usuarios válidos
* Para cada usuario en la tabla de usuarios válidos
    |usuario    |contraseña|rol      |
    |-----------|----------|---------|
    |admin      |admin123  |Admin    |
    |supervisor |super123  |Supervisor|
    |operador   |oper123   |Operador |
* Introducir las credenciales del usuario
* Verificar acceso exitoso según el rol
* Cerrar sesión correctamente

### Escenario: Validación de errores de login
* Intentar login con credenciales inválidas
    |usuario      |contraseña    |mensaje_esperado                |
    |-------------|--------------|--------------------------------|
    |             |              |Campos obligatorios             |
    |admin        |wrong         |Contraseña incorrecta           |
    |inexistente  |any           |Usuario no encontrado           |
    |admin        |              |Contraseña requerida            |
* Verificar que se muestra el mensaje de error apropiado
* Confirmar que no se permite el acceso

## Navegación y formularios

### Escenario: Navegación por menú principal
Dado que el usuario está logueado como "admin"
* Hacer clic en "Archivo" en el menú principal
* Verificar que se despliega el submenú de archivo
* Seleccionar "Nuevo documento"
* Confirmar que se abre el formulario correspondiente
* Tomar captura del formulario abierto

### Escenario: Completar formulario de datos
* Abrir formulario de entrada de datos
* Llenar los campos obligatorios:
    - Nombre: "Juan Pérez"
    - Email: "juan.perez@email.com"
    - Teléfono: "+34 123 456 789"
    - Fecha de nacimiento: "01/01/1990"
* Hacer clic en "Guardar"
* Verificar mensaje de confirmación "Datos guardados correctamente"
* Validar que los datos se muestran en la lista

### Escenario: Validación de campos de formulario
* Intentar guardar formulario con campos inválidos:
    - Email inválido: "email-sin-formato"
    - Teléfono inválido: "123"
    - Fecha inválida: "32/13/2025"
* Verificar que se muestran mensajes de validación apropiados
* Confirmar que no se permite guardar con datos inválidos

## Operaciones CRUD

### Escenario: Crear nuevo registro
* Navegar a la sección de gestión de registros
* Hacer clic en "Nuevo registro"
* Completar todos los campos requeridos
* Guardar el registro
* Verificar que aparece en la lista de registros
* Confirmar que se asignó un ID único

### Escenario: Editar registro existente
* Buscar un registro existente en la lista
* Hacer clic en "Editar"
* Modificar algunos campos:
    - Cambiar nombre a "Nombre Modificado"
    - Actualizar email a "nuevo@email.com"
* Guardar los cambios
* Verificar que los cambios se reflejan en la lista

### Escenario: Eliminar registro
* Seleccionar un registro de la lista
* Hacer clic en "Eliminar"
* Confirmar la eliminación en el diálogo
* Verificar que el registro ya no aparece en la lista
* Confirmar que no se puede acceder al registro eliminado

## Búsqueda y filtros

### Escenario: Búsqueda de registros
* Introducir criterio de búsqueda "Juan" en el campo de búsqueda
* Hacer clic en "Buscar"
* Verificar que solo se muestran registros que contienen "Juan"
* Limpiar el criterio de búsqueda
* Confirmar que se muestran todos los registros nuevamente

### Escenario: Aplicar filtros
* Seleccionar filtro por fecha "Último mes"
* Aplicar filtro
* Verificar que solo se muestran registros del último mes
* Cambiar filtro a "Este año"
* Confirmar que se actualiza la lista correctamente

## Reportes y exportación

### Escenario: Generar reporte PDF
* Navegar a la sección de reportes
* Seleccionar tipo de reporte "Resumen mensual"
* Configurar parámetros:
    - Fecha inicio: "01/01/2025"
    - Fecha fin: "31/01/2025"
* Hacer clic en "Generar PDF"
* Verificar que se genera el archivo PDF
* Confirmar que contiene los datos esperados

### Escenario: Exportar datos a Excel
* Seleccionar todos los registros de la lista
* Hacer clic en "Exportar a Excel"
* Verificar que se genera el archivo Excel
* Confirmar que contiene todos los datos seleccionados
* Validar formato y estructura del archivo

## Limpieza y cierre

### Escenario: Cierre correcto de la aplicación
* Guardar todos los cambios pendientes
* Cerrar todas las ventanas secundarias
* Hacer clic en "Salir" del menú principal
* Confirmar cierre en el diálogo si aparece
* Verificar que la aplicación se cierra completamente
* Confirmar que WinAppDriver termina correctamente
