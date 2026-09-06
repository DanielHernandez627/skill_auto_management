#!/usr/bin/env python3
"""Asistente de Onboarding Técnico (Fase 0: TechLeadArchitect).

Escanea un repositorio existente (con codigo productivo o legacy), detecta
automaticamente el stack tecnologico (.NET, Java, Node, Python, etc.) e inicializa
la carpeta base-conocimiento/ con el analisis de arquitectura y estandares.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import os
import re
import sys

IGNORED_SCAN_DIRS = {
    "node_modules",
    ".git",
    ".angular",
    "dist",
    "build",
    "target",
    "bin",
    "obj",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".idea",
    ".vscode",
    ".agents",
}


def analyze_csproj_content(csproj_path: Path, detected: dict[str, list[str]]) -> None:
    try:
        content = csproj_path.read_text(encoding="utf-8", errors="replace")
        if "EntityFrameworkCore" in content:
            detected["databases"].append("Entity Framework Core")
        if "MediatR" in content:
            detected["frameworks"].append("MediatR (CQRS)")
        if "xunit" in content.lower():
            detected["tools"].append("xUnit")
    except Exception:
        pass


def analyze_pom_content(pom_path: Path, detected: dict[str, list[str]]) -> None:
    try:
        content = pom_path.read_text(encoding="utf-8", errors="replace")
        if "spring-boot" in content:
            detected["frameworks"].append("Spring Boot")
        if "postgresql" in content:
            detected["databases"].append("PostgreSQL Driver")
    except Exception:
        pass


def analyze_package_json_content(pkg_path: Path, detected: dict[str, list[str]]) -> None:
    try:
        content = pkg_path.read_text(encoding="utf-8", errors="replace")
        if "@angular" in content:
            detected["frameworks"].append("Angular")
        if "react" in content:
            detected["frameworks"].append("React")
        if "vue" in content:
            detected["frameworks"].append("Vue.js")
        if "@nestjs" in content:
            detected["frameworks"].append("NestJS")
        if "express" in content:
            detected["frameworks"].append("Express")
        if "typeorm" in content:
            detected["databases"].append("TypeORM")
        if "pg" in content:
            detected["databases"].append("PostgreSQL (pg)")
    except Exception:
        pass


def detect_stack(project_dir: Path) -> dict[str, list[str]]:
    detected: dict[str, list[str]] = {
        "frameworks": [],
        "languages": [],
        "tools": [],
        "databases": [],
    }

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_SCAN_DIRS]
        root_path = Path(root)

        for filename in files:
            lower = filename.lower()
            if lower.endswith(".csproj") or lower.endswith(".sln"):
                detected["languages"].append("C# (.NET)")
                detected["tools"].append("dotnet CLI")
                if lower.endswith(".csproj"):
                    analyze_csproj_content(root_path / filename, detected)

            elif filename == "pom.xml":
                detected["languages"].append("Java")
                detected["tools"].append("Maven")
                analyze_pom_content(root_path / filename, detected)

            elif filename.startswith("build.gradle"):
                detected["languages"].append("Java")
                detected["tools"].append("Gradle")

            elif filename == "package.json":
                detected["languages"].append("TypeScript/JavaScript")
                detected["tools"].append("NPM / Node.js")
                analyze_package_json_content(root_path / filename, detected)

            elif filename in ("pyproject.toml", "requirements.txt") or lower.endswith(".py"):
                detected["languages"].append("Python")
                detected["tools"].append("Pytest / Pip")

            elif filename == "Dockerfile" or lower.startswith("docker-compose"):
                detected["tools"].append("Docker / Docker Compose")

    for category in detected:
        detected[category] = list(dict.fromkeys(detected[category]))

    return detected


def onboard_project(
    project_dir: Path,
    templates_dir: Path,
    project_name: str | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> int:
    resolved_dir = project_dir.resolve()
    name = project_name or resolved_dir.name
    today_str = date.today().isoformat()

    print(f"[INFO] Iniciando Onboarding Tecnico para: '{name}' en {resolved_dir}")
    stack = detect_stack(resolved_dir)

    print("[INFO] Diagnostico preliminar de tecnologias detectadas:")
    print(f"  - Lenguajes:  {', '.join(stack['languages']) or 'No identificados de forma automatica'}")
    print(f"  - Frameworks: {', '.join(stack['frameworks']) or 'No identificados de forma automatica'}")
    print(f"  - Herramientas:{', '.join(stack['tools']) or 'Estandar'}")
    print(f"  - Datos:      {', '.join(stack['databases']) or 'No identificada de forma automatica'}")

    target_kb_dir = resolved_dir / "base-conocimiento"
    if dry_run:
        print(f"[DRY-RUN] Se crearia la carpeta: {target_kb_dir}")
        return 0

    target_kb_dir.mkdir(parents=True, exist_ok=True)

    files_to_generate = [
        ("01-analisis-arquitectura.md", "01-analisis-arquitectura-template.md"),
        ("02-estandares-desarrollo.md", "02-estandares-desarrollo-template.md"),
        ("03-estandares-pruebas.md", "03-estandares-pruebas-template.md"),
        ("04-dominio-negocio.md", "04-dominio-negocio-template.md"),
    ]

    kb_templates_dir = templates_dir / "base-conocimiento"
    if not kb_templates_dir.exists():
        print(f"[ERROR] No se encontro la carpeta de plantillas en '{kb_templates_dir}'.")
        return 1

    created_files: list[Path] = []
    for output_name, template_name in files_to_generate:
        target_file = target_kb_dir / output_name
        template_file = kb_templates_dir / template_name

        if target_file.exists() and not force:
            print(f"[WARN] El archivo '{output_name}' ya existe. Usa --force para sobrescribir.")
            continue

        if not template_file.exists():
            print(f"[ERROR] Plantilla no encontrada: '{template_file}'.")
            continue

        content = template_file.read_text(encoding="utf-8")
        content = content.replace("[Nombre del Proyecto]", name)
        content = content.replace("[Nombre del Sistema]", name)
        content = content.replace("[Nombre del Sistema / Repositorio]", name)
        content = content.replace("YYYY-MM-DD", today_str)

        if output_name == "01-analisis-arquitectura.md":
            backend_desc = ", ".join(stack["languages"] + stack["frameworks"]) or "Por definir"
            tools_desc = ", ".join(stack["tools"]) or "Por definir"
            content = content.replace("[Ej. C# .NET 8, Spring Boot 3, FastAPI, NestJS]", backend_desc)
            content = content.replace("[Ej. .NET SDK, Maven, Gradle, Node/NPM, Docker]", tools_desc)

        target_file.write_text(content, encoding="utf-8")
        created_files.append(target_file)

    print(f"\n[OK] Onboarding inicializado exitosamente en '{target_kb_dir}':")
    for cf in created_files:
        print(f"  - {cf.name}")

    print("\n[PROXIMOS PASOS]")
    print("1. El Líder Técnico / Asistente IA debe revisar y refinar los diagramas Mermaid en '01-analisis-arquitectura.md'.")
    print("2. Documentar las entidades clave en '04-dominio-negocio.md'.")
    print("3. Establecida la línea base, el Product Owner puede crear la primera HU con 'python scripts/scaffold_hu.py'.")

    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Asistente de Onboarding Tecnico y Generador de Base de Conocimiento (Fase 0)."
    )
    parser.add_argument(
        "--path",
        "-p",
        type=Path,
        default=Path("."),
        help="Ruta al proyecto existente a escanear (por defecto: directorio actual).",
    )
    parser.add_argument(
        "--name",
        "-n",
        type=str,
        help="Nombre formal del proyecto o sistema.",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=None,
        help="Ruta personalizada a la carpeta de plantillas.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Sobrescribe documentos existentes en base-conocimiento/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra el diagnostico sin crear archivos.",
    )

    args = parser.parse_args()

    resolved_templates_dir = args.templates_dir
    if resolved_templates_dir is None:
        resolved_templates_dir = Path(__file__).resolve().parent.parent / "templates"

    return onboard_project(
        project_dir=args.path,
        templates_dir=resolved_templates_dir,
        project_name=args.name,
        force=args.force,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
