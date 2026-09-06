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
import re
import sys


def scan_dotnet_ecosystem(project_dir: Path, detected: dict[str, list[str]]) -> None:
    csproj_files = list(project_dir.rglob("*.csproj"))
    sln_files = list(project_dir.rglob("*.sln"))
    if csproj_files or sln_files:
        detected["languages"].append("C# (.NET)")
        detected["tools"].append("dotnet CLI")
        for csproj in csproj_files[:5]:
            try:
                content = csproj.read_text(encoding="utf-8", errors="replace")
                if "EntityFrameworkCore" in content:
                    detected["databases"].append("Entity Framework Core")
                if "MediatR" in content:
                    detected["frameworks"].append("MediatR (CQRS)")
                if "xunit" in content.lower():
                    detected["tools"].append("xUnit")
            except Exception:
                pass


def scan_jvm_ecosystem(project_dir: Path, detected: dict[str, list[str]]) -> None:
    pom_files = list(project_dir.rglob("pom.xml"))
    gradle_files = list(project_dir.rglob("build.gradle*"))
    if pom_files or gradle_files:
        detected["languages"].append("Java")
        if pom_files:
            detected["tools"].append("Maven")
        if gradle_files:
            detected["tools"].append("Gradle")
        for pom in pom_files[:5]:
            try:
                content = pom.read_text(encoding="utf-8", errors="replace")
                if "spring-boot" in content:
                    detected["frameworks"].append("Spring Boot")
                if "postgresql" in content:
                    detected["databases"].append("PostgreSQL Driver")
            except Exception:
                pass


def scan_node_ecosystem(project_dir: Path, detected: dict[str, list[str]]) -> None:
    pkg_files = list(project_dir.rglob("package.json"))
    for pkg in pkg_files:
        if "node_modules" in pkg.parts:
            continue
        detected["languages"].append("TypeScript/JavaScript")
        detected["tools"].append("NPM / Node.js")
        try:
            content = pkg.read_text(encoding="utf-8", errors="replace")
            if "@angular" in content:
                detected["frameworks"].append("Angular")
            if "react" in content:
                detected["frameworks"].append("React")
            if "vue" in content:
                detected["frameworks"].append("Vue.js")
            if "@nestjs" in content:
                detected["frameworks"].append("NestJS")
        except Exception:
            pass


def scan_python_ecosystem(project_dir: Path, detected: dict[str, list[str]]) -> None:
    pyproject = list(project_dir.rglob("pyproject.toml"))
    requirements = list(project_dir.rglob("requirements.txt"))
    if pyproject or requirements or list(project_dir.rglob("*.py")):
        if not any("node_modules" in p.parts for p in pyproject):
            detected["languages"].append("Python")
            detected["tools"].append("Pytest / Pip")


def scan_container_ecosystem(project_dir: Path, detected: dict[str, list[str]]) -> None:
    if list(project_dir.rglob("Dockerfile")) or list(project_dir.rglob("docker-compose*.yml")):
        detected["tools"].append("Docker / Docker Compose")


def detect_stack(project_dir: Path) -> dict[str, list[str]]:
    detected: dict[str, list[str]] = {
        "frameworks": [],
        "languages": [],
        "tools": [],
        "databases": [],
    }

    scan_dotnet_ecosystem(project_dir, detected)
    scan_jvm_ecosystem(project_dir, detected)
    scan_node_ecosystem(project_dir, detected)
    scan_python_ecosystem(project_dir, detected)
    scan_container_ecosystem(project_dir, detected)

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
