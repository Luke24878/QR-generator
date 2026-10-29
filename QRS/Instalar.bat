@echo off
setlocal
title Instalador - Generador de codigos QR
cd /d "%~dp0"

if not exist "GeneradorQR.py" (
    echo.
    echo Falta el archivo GeneradorQR.py en esta carpeta.
    echo Extrae primero todo el contenido del archivo ZIP.
    echo.
    pause
    exit /b 1
)

if not exist "requerimientos.txt" (
    echo.
    echo Falta el archivo requerimientos.txt en esta carpeta.
    echo.
    pause
    exit /b 1
)

py -3 -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python 3 no esta instalado. Descargandolo con winget...
    where winget >nul 2>&1
    if errorlevel 1 (
        echo.
        echo No se encontro winget en este equipo.
        echo Instala Python 3 desde https://www.python.org/downloads/
        echo y despues vuelve a ejecutar este archivo.
        echo.
        pause
        exit /b 1
    )

    winget install --id Python.Python.3.12 --exact --source winget --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo.
        echo No se pudo instalar Python automaticamente.
        echo Descargalo desde https://www.python.org/downloads/ y vuelve a ejecutar este archivo.
        echo.
        pause
        exit /b 1
    )
)

py -3 -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python se instalo, pero Windows aun no actualiza esta ventana.
    echo Cierra esta ventana y vuelve a ejecutar Instalar.bat.
    echo.
    pause
    exit /b 1
)

echo.
echo Instalando las bibliotecas necesarias...
py -3 -m pip --version >nul 2>&1
if errorlevel 1 py -3 -m ensurepip --upgrade

py -3 -m pip install --disable-pip-version-check -r "requerimientos.txt"
if errorlevel 1 (
    echo.
    echo No se pudieron instalar las bibliotecas.
    echo Revisa tu conexion a Internet e intenta de nuevo.
    echo.
    pause
    exit /b 1
)

echo.
echo Instalacion terminada.
echo En adelante, abre la aplicacion con GeneradorQR.bat.
echo.
pause
endlocal
