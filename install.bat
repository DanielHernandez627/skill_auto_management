@echo off
setlocal enabledelayedexpansion

where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0install.py" %*
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 "%~dp0install.py" %*
    goto :end
)

echo [AVISO] Python no fue detectado en PATH.
echo [INFO] Ejecutando instalador nativo de Windows (Zero-Python fallback)...

set "SRC_DIR=%~dp0"
if "%SRC_DIR:~-1%"=="\" set "SRC_DIR=%SRC_DIR:~0,-1%"
set "SKILL_NAME=agile-hu-workflow"
set "AG_DEST=%USERPROFILE%\.gemini\config\skills\%SKILL_NAME%"
set "CLAUDE_CMDS=%USERPROFILE%\.claude\commands"
set "CLAUDE_MD=%USERPROFILE%\.claude\CLAUDE.md"

if not exist "%AG_DEST%" mkdir "%AG_DEST%"
if not exist "%CLAUDE_CMDS%" mkdir "%CLAUDE_CMDS%"

robocopy "%SRC_DIR%" "%AG_DEST%" /E /XD .git __pycache__ .pytest_cache .coverage .venv venv .idea .vscode /XF .coverage* /NJH /NJS /NDL /NC /NS >nul

if exist "%SRC_DIR%\.claude\commands" (
    copy /Y "%SRC_DIR%\.claude\commands\*.md" "%CLAUDE_CMDS%\" >nul
)
if exist "%SRC_DIR%\CLAUDE.md" (
    copy /Y "%SRC_DIR%\CLAUDE.md" "%CLAUDE_MD%" >nul
)

echo.
echo [EXITO] Instalacion global (Zero-Python) completada exitosamente:
echo   [OK] Google Antigravity -^> %AG_DEST%
echo   [OK] Claude Code        -^> %CLAUDE_CMDS%
echo.
echo [USO INMEDIATO]
echo Ya puedes usar los comandos en Antigravity y Claude Code:
echo   /iniciarproyecto -^> Creacion e ideacion de proyecto desde cero
echo   /onboarding      -^> Onboarding tecnico de un proyecto existente
echo   /nueva-hu        -^> Redaccion de Historia de Usuario con Gherkin
echo   /refinar-hu      -^> Refinamiento tecnico y diagramas Mermaid
echo   /desarrollar-hu  -^> Implementacion Clean Code multilenguaje
echo   /cerrar-hu       -^> Cierre, tests y bitacora en dev-records/
echo   /reportar-bug    -^> Registro formal de defecto con Gherkin
echo   /corregir-bug    -^> Fix con RCA y test de regresion obligatorio
echo   /kpis            -^> Tablero de calidad local (0 consumo de tokens)
echo   /chat-hu         -^> Consulta y chat especializado sobre una HU

:end
pause
