@echo off
rem Abre la interfaz sin dejar una ventana de CMD abierta.
cd /d "%~dp0"

if not exist "GeneradorQR.py" (
    echo Falta el archivo GeneradorQR.py. Extrae todo el archivo ZIP antes de abrirlo.
    pause
    exit /b 1
)

py -3 -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado. Ejecuta primero Instalar.bat.
    pause
    exit /b 1
)

for /f "delims=" %%P in ('py -3 -c "import sys; print(sys.executable)"') do set "PYTHON_EXE=%%P"
if not defined PYTHON_EXE (
    echo No se encontro Python 3. Ejecuta primero Instalar.bat.
    pause
    exit /b 1
)

set "PYTHONW=%PYTHON_EXE:python.exe=pythonw.exe%"
if not exist "%PYTHONW%" (
    echo No se encontro pythonw.exe. Ejecuta primero Instalar.bat.
    pause
    exit /b 1
)

start "" "%PYTHONW%" "%~dp0GeneradorQR.py"
exit /b
