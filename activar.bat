@echo off
REM Script de activación del entorno virtual para Windows CMD

echo Activando entorno virtual Python...

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo Error: No se pudo crear el entorno virtual
        echo Asegurate de tener Python instalado y accesible desde CMD
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar que el entorno virtual está activo
python -c "import sys; print('Python:', sys.executable)"

REM Instalar dependencias si es necesario
if not exist "venv\Lib\site-packages\pytest" (
    echo Instalando dependencias...
    pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo.
echo ======================================
echo Entorno virtual activado exitosamente
echo ======================================
echo.
echo Comandos útiles:
echo   pytest                 - Ejecutar todas las pruebas
echo   pytest tests/unit/     - Ejecutar solo pruebas unitarias
echo   pytest -m smoke        - Ejecutar pruebas smoke
echo   gauge run specs/       - Ejecutar especificaciones Gauge
echo   deactivate            - Desactivar entorno virtual
echo.

REM Mantener la ventana abierta
cmd /k
