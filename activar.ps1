# Script de activación del entorno virtual para PowerShell

Write-Host "Activando entorno virtual Python..." -ForegroundColor Green

# Verificar si existe el entorno virtual
if (!(Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: No se pudo crear el entorno virtual" -ForegroundColor Red
        Write-Host "Asegúrate de tener Python instalado y accesible desde PowerShell" -ForegroundColor Red
        Read-Host "Presiona Enter para continuar"
        exit 1
    }
}

# Verificar política de ejecución de PowerShell
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Host "Advertencia: La política de ejecución está restringida." -ForegroundColor Yellow
    Write-Host "Ejecuta: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Presiona Enter después de cambiar la política"
}

# Activar entorno virtual
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado" -ForegroundColor Green
}
catch {
    Write-Host "Error al activar entorno virtual: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Presiona Enter para continuar"
    exit 1
}

# Verificar que el entorno virtual está activo
$pythonPath = python -c "import sys; print(sys.executable)"
Write-Host "Python activo: $pythonPath" -ForegroundColor Cyan

# Verificar si las dependencias están instaladas
$pytestInstalled = pip list | Select-String "pytest"
if (!$pytestInstalled) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: No se pudieron instalar las dependencias" -ForegroundColor Red
        Read-Host "Presiona Enter para continuar"
        exit 1
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Entorno virtual activado exitosamente" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Cyan
Write-Host "  pytest                 - Ejecutar todas las pruebas" -ForegroundColor White
Write-Host "  pytest tests/unit/     - Ejecutar solo pruebas unitarias" -ForegroundColor White
Write-Host "  pytest -m smoke        - Ejecutar pruebas smoke" -ForegroundColor White
Write-Host "  gauge run specs/       - Ejecutar especificaciones Gauge" -ForegroundColor White
Write-Host "  deactivate            - Desactivar entorno virtual" -ForegroundColor White
Write-Host ""

# Configurar variables de entorno para la sesión actual
$env:PYTHONPATH = "$PWD\src"
Write-Host "PYTHONPATH configurado: $env:PYTHONPATH" -ForegroundColor Cyan
