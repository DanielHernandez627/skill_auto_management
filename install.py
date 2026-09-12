#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import platform
import shutil
import sys

SKILL_NAME = "agile-hu-workflow"
EXCLUDED_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".coverage",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}


def resolve_home_dir() -> Path:
    return Path.home()


def copy_file_safe(source_file: Path, target_file: Path) -> None:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, target_file)


def copy_tree_safe(source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        if item.name in EXCLUDED_NAMES or item.name.startswith(".coverage"):
            continue
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(
                item,
                dest,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"),
            )
        else:
            shutil.copy2(item, dest)


def install_antigravity_global(source_dir: Path, dry_run: bool) -> Path:
    dest_dir = resolve_home_dir() / ".gemini" / "config" / "skills" / SKILL_NAME
    if not dry_run:
        copy_tree_safe(source_dir, dest_dir)
    return dest_dir


def install_claude_global(source_dir: Path, dry_run: bool) -> tuple[Path, Path]:
    claude_home = resolve_home_dir() / ".claude"
    commands_dest = claude_home / "commands"
    claude_md_dest = claude_home / "CLAUDE.md"

    commands_src = source_dir / ".claude" / "commands"
    claude_md_src = source_dir / "CLAUDE.md"

    if not dry_run:
        commands_dest.mkdir(parents=True, exist_ok=True)
        if commands_src.exists():
            for cmd in commands_src.glob("*.md"):
                shutil.copy2(cmd, commands_dest / cmd.name)
        if claude_md_src.exists():
            shutil.copy2(claude_md_src, claude_md_dest)

    return commands_dest, claude_md_dest


def install_workspace(
    source_dir: Path,
    workspace_path: Path,
    assistants: list[str],
    dry_run: bool,
) -> int:
    resolved_ws = workspace_path.resolve()
    if not resolved_ws.exists():
        print(f"[ERROR] El directorio del workspace no existe: {resolved_ws}")
        return 1

    print(f"\n[CONFIGURACION DE WORKSPACE] Configurando en: {resolved_ws}")

    configured: list[str] = []

    if "copilot" in assistants or "all" in assistants:
        github_src = source_dir / ".github"
        github_dest = resolved_ws / ".github"
        if github_src.exists() and not dry_run:
            copy_tree_safe(github_src, github_dest)
        configured.append(f"GitHub Copilot -> {github_dest.name}/ (instrucciones y prompts)")

    if "claude" in assistants or "all" in assistants:
        claude_src = source_dir / ".claude"
        claude_dest = resolved_ws / ".claude"
        claude_md_src = source_dir / "CLAUDE.md"
        claude_md_dest = resolved_ws / "CLAUDE.md"
        if not dry_run:
            if claude_src.exists():
                copy_tree_safe(claude_src, claude_dest)
            if claude_md_src.exists():
                shutil.copy2(claude_md_src, claude_md_dest)
        configured.append(f"Claude Code    -> {claude_dest.name}/ y CLAUDE.md")

    if "antigravity" in assistants or "all" in assistants:
        ag_dest = resolved_ws / ".agents" / "skills" / SKILL_NAME
        if not dry_run:
            copy_tree_safe(source_dir, ag_dest)
        configured.append(f"Antigravity    -> .agents/skills/{SKILL_NAME}/")

    scripts_src = source_dir / "scripts"
    templates_src = source_dir / "templates"
    references_src = source_dir / "references"

    if not dry_run:
        scripts_dest = resolved_ws / "scripts"
        templates_dest = resolved_ws / "templates"
        references_dest = resolved_ws / "references"
        if scripts_src.exists():
            copy_tree_safe(scripts_src, scripts_dest)
        if templates_src.exists():
            copy_tree_safe(templates_src, templates_dest)
        if references_src.exists():
            copy_tree_safe(references_src, references_dest)

    configured.append("Scripts y Plantillas -> scripts/, templates/, references/")

    if dry_run:
        print("[DRY-RUN] Modo simulacion. Se copiarian los artefactos al proyecto.")
        return 0

    print("\n[EXITO] Proyecto configurado para asistentes de IA:")
    for item in configured:
        print(f"  - {item}")

    print("\n[COMO USAR EN TU PROYECTO]")
    print("  - En VS Code con Copilot: Abre Copilot Chat y escribe /onboarding o /nueva-hu.")
    print("  - En Claude Code CLI: Abre la terminal en el proyecto y escribe /onboarding.")
    print("  - En Google Antigravity: Abre el proyecto y escribe /onboarding o /nueva-hu.")
    return 0


def uninstall_global() -> int:
    ag_dest = resolve_home_dir() / ".gemini" / "config" / "skills" / SKILL_NAME
    claude_commands = resolve_home_dir() / ".claude" / "commands"

    if ag_dest.exists():
        shutil.rmtree(ag_dest)
        print(f"[OK] Skill desinstalada de Antigravity: {ag_dest}")

    if claude_commands.exists():
        for cmd in (
            "onboarding.md",
            "nueva-hu.md",
            "refinar-hu.md",
            "desarrollar-hu.md",
            "cerrar-hu.md",
            "auditar-clean-code.md",
            "reportar-bug.md",
            "corregir-bug.md",
            "kpis.md",
            "chat-hu.md",
        ):
            cmd_path = claude_commands / cmd
            if cmd_path.exists():
                cmd_path.unlink()
        print(f"[OK] Comandos desinstalados de Claude Code: {claude_commands}")

    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    source_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description=f"Instalador Multi-Asistente de '{SKILL_NAME}' (Antigravity, Claude Code, Copilot)."
    )
    parser.add_argument(
        "--workspace",
        "--path",
        "--target-dir",
        "-w",
        "-p",
        "-t",
        dest="workspace",
        type=Path,
        help="Configura la metodologia directamente en un proyecto de codigo especifico.",
    )
    parser.add_argument(
        "--assistant",
        "-a",
        choices=["all", "antigravity", "claude", "copilot"],
        default="all",
        help="Asistente a instalar o configurar (por defecto: all).",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Desinstala la configuracion global de Antigravity y Claude Code.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra las acciones sin realizar cambios en disco.",
    )

    args = parser.parse_args()

    if args.uninstall:
        return uninstall_global()

    if args.workspace:
        assistants = ["all"] if args.assistant == "all" else [args.assistant]
        return install_workspace(source_dir, args.workspace, assistants, args.dry_run)

    print(f"\n[INFO] Sistema operativo detectado: {platform.system()} ({platform.release()})")

    installed_items: list[str] = []

    if args.assistant in ("all", "antigravity"):
        ag_dest = install_antigravity_global(source_dir, args.dry_run)
        installed_items.append(f"Google Antigravity (Global) -> {ag_dest}")

    if args.assistant in ("all", "claude"):
        claude_cmds, claude_md = install_claude_global(source_dir, args.dry_run)
        installed_items.append(f"Claude Code (Global)        -> {claude_cmds}")

    if args.dry_run:
        print("[DRY-RUN] Modo simulacion. No se realizaron cambios.")
        return 0

    print("\n[EXITO] Instalacion global completada exitosamente:")
    for item in installed_items:
        print(f"  [OK] {item}")

    print("\n[INFORMACION PARA GITHUB COPILOT]")
    print("GitHub Copilot opera a nivel de proyecto (en VS Code / JetBrains).")
    print("Para activar la metodologia en un proyecto de codigo especifico, ejecuta:")
    print("  python install.py --workspace /ruta/a/tu-proyecto")

    print("\n[USO INMEDIATO]")
    print("Ya puedes usar los comandos en Antigravity y Claude Code:")
    print("  /onboarding     -> Onboarding tecnico de un proyecto existente")
    print("  /nueva-hu       -> Redaccion de Historia de Usuario con Gherkin")
    print("  /refinar-hu     -> Refinamiento tecnico y diagramas Mermaid")
    print("  /desarrollar-hu -> Implementacion Clean Code multilenguaje")
    print("  /cerrar-hu      -> Cierre, tests y bitacora en dev-records/")
    print("  /reportar-bug   -> Registro formal de defecto con Gherkin")
    print("  /corregir-bug   -> Fix con RCA y test de regresion obligatorio")
    print("  /kpis           -> Tablero de calidad local (0 consumo de tokens)")
    print("  /chat-hu        -> Consulta y chat especializado sobre una HU")

    return 0


if __name__ == "__main__":
    sys.exit(main())
