#!/usr/bin/env bash
set -e

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$(dirname "$0")/install.py" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$(dirname "$0")/install.py" "$@"
fi

echo "[AVISO] Python no fue detectado en PATH."
echo "[INFO] Ejecutando instalador nativo de sistema (Zero-Python fallback)..."

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="agile-hu-workflow"
AG_DEST="$HOME/.gemini/config/skills/$SKILL_NAME"
CLAUDE_CMDS="$HOME/.claude/commands"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

mkdir -p "$AG_DEST"
mkdir -p "$CLAUDE_CMDS"

if command -v rsync >/dev/null 2>&1; then
    rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.coverage*' --exclude='.venv' --exclude='venv' --exclude='.idea' --exclude='.vscode' "$SRC_DIR/" "$AG_DEST/" >/dev/null
else
    cp -R "$SRC_DIR/." "$AG_DEST/"
    rm -rf "$AG_DEST/.git" "$AG_DEST/__pycache__" "$AG_DEST/.pytest_cache" "$AG_DEST/.venv" "$AG_DEST/venv" "$AG_DEST/.coverage"* 2>/dev/null || true
fi

if [ -d "$SRC_DIR/.claude/commands" ]; then
    cp -f "$SRC_DIR/.claude/commands/"*.md "$CLAUDE_CMDS/" 2>/dev/null || true
fi

if [ -f "$SRC_DIR/CLAUDE.md" ]; then
    cp -f "$SRC_DIR/CLAUDE.md" "$CLAUDE_MD"
fi

echo ""
echo "[EXITO] Instalacion global (Zero-Python) completada exitosamente:"
echo "  [OK] Google Antigravity -> $AG_DEST"
echo "  [OK] Claude Code        -> $CLAUDE_CMDS"
echo ""
echo "[USO INMEDIATO]"
echo "Ya puedes usar los comandos en Antigravity y Claude Code:"
echo "  /iniciarproyecto -> Creacion e ideacion de proyecto desde cero"
echo "  /onboarding      -> Onboarding tecnico de un proyecto existente"
echo "  /nueva-hu        -> Redaccion de Historia de Usuario con Gherkin"
echo "  /refinar-hu      -> Refinamiento tecnico y diagramas Mermaid"
echo "  /desarrollar-hu  -> Implementacion Clean Code multilenguaje"
echo "  /cerrar-hu       -> Cierre, tests y bitacora en dev-records/"
echo "  /reportar-bug    -> Registro formal de defecto con Gherkin"
echo "  /corregir-bug    -> Fix con RCA y test de regresion obligatorio"
echo "  /kpis            -> Tablero de calidad local (0 consumo de tokens)"
echo "  /chat-hu         -> Consulta y chat especializado sobre una HU"
