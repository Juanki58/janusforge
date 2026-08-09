@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if errorlevel 1 (
  echo [ERROR] No se pudo cambiar al directorio del script:
  echo   %~dp0
  pause
  exit /b 1
)

set "REPO_ROOT=%CD%"
set "VENV_DIR=%REPO_ROOT%\.venv_visor"
set "PY_VENV=%VENV_DIR%\Scripts\python.exe"
set "PIP_VENV=%VENV_DIR%\Scripts\pip.exe"
set "REQ=%REPO_ROOT%\requirements-visor.txt"
set "APP_MODULE=app.main:app"
set "HOST=127.0.0.1"
set "PORT=8765"
set "URL=http://%HOST%:%PORT%/"

echo ============================================
echo  Janusforge Visor Molecular
echo  Repo: %REPO_ROOT%
echo ============================================
echo.

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  set "PY_BOOT=py -3"
) else (
  where python >nul 2>&1
  if %ERRORLEVEL%==0 (
    set "PY_BOOT=python"
  ) else (
    echo [ERROR] No se encontro Python en el PATH.
    echo Instala Python 3.10+ desde https://www.python.org/downloads/
    echo y marca "Add python.exe to PATH".
    pause
    exit /b 1
  )
)

if not exist "%REQ%" (
  echo [ERROR] Falta requirements-visor.txt en:
  echo   %REQ%
  pause
  exit /b 1
)

if not exist "%REPO_ROOT%\app\main.py" (
  echo [ERROR] Falta app\main.py. ¿Ejecutaste este BAT fuera del repo?
  pause
  exit /b 1
)

if not exist "%PY_VENV%" (
  echo [1/3] Creando entorno virtual .venv_visor ...
  %PY_BOOT% -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo [ERROR] Fallo al crear el venv.
    pause
    exit /b 1
  )
) else (
  echo [1/3] Entorno .venv_visor ya existe.
)

echo [2/3] Instalando dependencias (fastapi, uvicorn, jinja2)...
"%PY_VENV%" -m pip install --upgrade pip >nul 2>&1
"%PIP_VENV%" install -r "%REQ%"
if errorlevel 1 (
  echo [ERROR] pip install fallo. Revisa la salida anterior.
  pause
  exit /b 1
)

echo [3/3] Arrancando servidor en %URL%
echo      Cierra esta ventana para detener el visor.
echo.

start "" "%URL%"
"%PY_VENV%" -m uvicorn %APP_MODULE% --app-dir "%REPO_ROOT%" --host %HOST% --port %PORT%
set "EC=%ERRORLEVEL%"
if not "%EC%"=="0" (
  echo.
  echo [ERROR] uvicorn salio con codigo %EC%.
  echo Si el puerto %PORT% esta ocupado, cierra el otro proceso o cambia PORT en este BAT.
  pause
  exit /b %EC%
)

endlocal
exit /b 0
