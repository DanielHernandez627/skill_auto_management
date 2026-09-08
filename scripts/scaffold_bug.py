#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys


def resolve_docs_directory(target_dir: Path, docs_dir_name: str) -> Path:
    resolved = target_dir.resolve()
    return resolved if resolved.name == docs_dir_name else resolved / docs_dir_name


def format_bug_id(raw_id: str) -> str:
    cleaned = raw_id.strip().upper()
    if cleaned.startswith("BUG-"):
        return cleaned
    if "-" in cleaned:
        parts = cleaned.split("-")
        return f"BUG-{parts[0].zfill(3)}-{parts[1].zfill(2)}"
    if cleaned.isdigit():
        return f"BUG-{int(cleaned):03d}-01"
    return f"BUG-{cleaned}"


def update_metrics_on_bug_created(docs_dir: Path) -> None:
    metrics_file = docs_dir / "metricas.json"
    data: dict = {
        "hus_creadas": 0,
        "hus_completadas": 0,
        "bugs_reportados": 0,
        "bugs_resueltos": 0,
        "auditorias_clean_code": 0,
        "comentarios_limpiados": 0,
        "ultima_cobertura": None,
        "total_tests": None,
        "actualizado_en": date.today().isoformat(),
    }

    if metrics_file.exists():
        try:
            loaded = json.loads(metrics_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data.update(loaded)
        except Exception:
            pass

    data["bugs_reportados"] = data.get("bugs_reportados", 0) + 1
    data["actualizado_en"] = date.today().isoformat()
    metrics_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def update_docs_readme_bugs(
    readme_file: Path,
    bug_id: str,
    title: str,
    hu_id: str,
    severity: str,
) -> None:
    if not readme_file.exists():
        return

    content = readme_file.read_text(encoding="utf-8")

    hu_link = f"[`{hu_id}`](hus/{hu_id}.md)" if hu_id and hu_id.upper() != "TRANSVERSAL" else "Transversal"
    severity_tag = f"[{severity}]"

    row_entry = f"| [`{bug_id}`](bugs/{bug_id}.md) | {hu_link} | {title} | {severity_tag} | [Reportado] |"

    bugs_section_header = "## Tabla de Defectos y Bugs"
    legacy_header = "## 🐞 Tabla de Defectos y Bugs"
    active_header = legacy_header if legacy_header in content else bugs_section_header

    if bugs_section_header not in content and legacy_header not in content:
        section = (
            f"\n\n---\n\n{bugs_section_header}\n\n"
            "| ID Defecto | Historia Asociada | Título | Severidad | Estado |\n"
            "|---|---|---|---|---|\n"
            f"{row_entry}\n"
        )
        content = content.rstrip() + section
    else:
        if row_entry not in content:
            lines = content.splitlines()
            header_idx = -1
            for idx, line in enumerate(lines):
                if active_header in line:
                    header_idx = idx
                    break

            if header_idx != -1:
                insert_idx = len(lines)
                for idx in range(header_idx + 1, len(lines)):
                    if lines[idx].startswith("## "):
                        insert_idx = idx
                        break
                lines.insert(insert_idx, row_entry)
                content = "\n".join(lines) + "\n"

    readme_file.write_text(content, encoding="utf-8")


def scaffold_bug(
    bug_id: str,
    title: str,
    hu_id: str | None,
    severity: str,
    target_dir: Path,
    templates_dir: Path,
    docs_dir_name: str = "automanagement_docs",
    force: bool = False,
) -> int:
    formatted_id = format_bug_id(bug_id)
    template_file = templates_dir / "bug-template.md"
    if not template_file.exists():
        print(f"[ERROR] No se encontro la plantilla requerida: {template_file}")
        return 1

    docs_dir = resolve_docs_directory(target_dir, docs_dir_name)
    bugs_dir = docs_dir / "bugs"
    bugs_dir.mkdir(parents=True, exist_ok=True)

    target_bug_file = bugs_dir / f"{formatted_id}.md"
    if target_bug_file.exists() and not force:
        print(f"[WARN] El archivo {target_bug_file} ya existe. Usa --force para sobrescribir.")
        return 1

    content = template_file.read_text(encoding="utf-8")
    content = content.replace("[BUG-ID]", formatted_id)
    content = content.replace("[Título del Defecto]", title)
    content = content.replace("YYYY-MM-DD", date.today().isoformat())

    clean_hu = hu_id.strip().upper() if hu_id else "Transversal"
    content = content.replace("[HU-ID]", clean_hu)
    content = content.replace("[Bloqueante] / [Alta] / [Media] / [Baja]", f"[{severity}]")
    content = content.replace("[🔴 Bloqueante / 🟠 Alta / 🟡 Media / 🟢 Baja]", f"[{severity}]")

    target_bug_file.write_text(content, encoding="utf-8")

    readme_file = docs_dir / "README.md"
    update_docs_readme_bugs(readme_file, formatted_id, title, clean_hu, severity)
    update_metrics_on_bug_created(docs_dir)

    print(f"\n[OK] Defecto {formatted_id} creado exitosamente:")
    print(f"  - {docs_dir_name}/bugs/{formatted_id}.md")
    print(f"  - Registrado en {docs_dir_name}/README.md")
    print("\n[PROXIMOS PASOS]")
    print(f"1. Completa la evidencia y pasos para reproducir en '{target_bug_file.name}'.")
    print(f"2. Para resolverlo, el DevQA debe ejecutar '/corregir-bug {formatted_id}'.")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Generador interactivo de fichas de defectos y bugs (Fase de Calidad)."
    )
    parser.add_argument("bug_id", type=str, help="ID del defecto (ej. BUG-001-01 o BUG-001).")
    parser.add_argument("title", type=str, help="Titulo o resumen breve del defecto.")
    parser.add_argument("--hu", type=str, default=None, help="ID de la Historia de Usuario asociada (ej. HU-001).")
    parser.add_argument(
        "--severity",
        type=str,
        choices=["Bloqueante", "Alta", "Media", "Baja"],
        default="Alta",
        help="Severidad del defecto (por defecto: Alta).",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path("."),
        help="Directorio raiz del proyecto (donde reside automanagement_docs).",
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="automanagement_docs",
        help="Nombre del directorio central de documentacion.",
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
        help="Sobrescribe el archivo si ya existe.",
    )

    args = parser.parse_args()

    resolved_templates_dir = args.templates_dir
    if resolved_templates_dir is None:
        resolved_templates_dir = Path(__file__).resolve().parent.parent / "templates"

    return scaffold_bug(
        bug_id=args.bug_id,
        title=args.title,
        hu_id=args.hu,
        severity=args.severity,
        target_dir=args.target_dir,
        templates_dir=resolved_templates_dir,
        docs_dir_name=args.docs_dir,
        force=args.force,
    )


if __name__ == "__main__":
    sys.exit(main())
