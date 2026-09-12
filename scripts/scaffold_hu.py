#!/usr/bin/env python3
"""Generador de Artefactos de Historias de Usuario (Scaffolding).

Crea de forma estandarizada la Historia de Usuario para la Fase 1 en automanagement_docs/:
1. automanagement_docs/hus/HU-XXX.md
2. automanagement_docs/README.md (registro y estado inicial en refinamiento)
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys


def resolve_docs_directory(target_dir: Path, docs_dir_name: str) -> Path:
    if target_dir.name == docs_dir_name:
        return target_dir
    return target_dir / docs_dir_name


def update_docs_index_table(
    docs_dir: Path,
    hu_id: str,
    title: str,
) -> None:
    readme_file = docs_dir / "README.md"
    if not readme_file.exists():
        return

    content = readme_file.read_text(encoding="utf-8")
    if f"[`{hu_id}`]" in content:
        return

    row_entry = (
        f"| [`{hu_id}`](hus/{hu_id}.md) | {title} | [En Refinamiento] | "
        f"Pendiente (`/refinar-hu`) | "
        f"Pendiente (`/cerrar-hu`) |"
    )

    placeholder = "| *(Las nuevas HUs creadas con `/nueva-hu` se registrarán en esta sección)* | | | | |"
    if placeholder in content:
        content = content.replace(placeholder, row_entry)
    elif "| ID | Título | Estado | Refinamiento | Registro Dev / QA |" in content:
        content = content.rstrip() + "\n" + row_entry + "\n"

    readme_file.write_text(content, encoding="utf-8")


def update_metrics_on_hu_created(docs_dir: Path) -> None:
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

    data["hus_creadas"] = data.get("hus_creadas", 0) + 1
    data["actualizado_en"] = date.today().isoformat()
    metrics_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def scaffold_hu(
    hu_id: str,
    title: str,
    target_dir: Path,
    templates_dir: Path,
    docs_dir_name: str = "automanagement_docs",
    force: bool = False,
    force_raw: bool = False,
) -> int:
    clean_id = hu_id.strip()
    upper_id = clean_id.upper()
    if force_raw:
        formatted_id = upper_id
    elif upper_id.startswith("HU-"):
        num_part = upper_id.replace("HU-", "")
        formatted_id = f"HU-{num_part}"
    elif "-" in upper_id:
        formatted_id = upper_id
    elif clean_id.isdigit():
        num = int(clean_id)
        formatted_id = f"HU-{num:03d}" if num < 1000 else f"HU-{clean_id}"
    else:
        formatted_id = upper_id

    hu_template_file = templates_dir / "hu-template.md"
    if not hu_template_file.exists():
        print(f"[ERROR] No se encontro la plantilla requerida: {hu_template_file}")
        return 1

    docs_base_dir = resolve_docs_directory(target_dir, docs_dir_name)
    hus_dir = docs_base_dir / "hus"
    hus_dir.mkdir(parents=True, exist_ok=True)

    target_hu_file = hus_dir / f"{formatted_id}.md"

    if target_hu_file.exists() and not force:
        print(f"[WARN] El archivo {target_hu_file} ya existe. Usa --force para sobrescribir.")
        return 1

    hu_content = (
        hu_template_file.read_text(encoding="utf-8")
        .replace("[HU-XXX]", formatted_id)
        .replace("HU-XXX", formatted_id)
        .replace("[Título Corto de la Historia]", title)
    )

    target_hu_file.write_text(hu_content, encoding="utf-8")
    update_docs_index_table(docs_base_dir, formatted_id, title)
    update_metrics_on_hu_created(docs_base_dir)

    print(f"[OK] Se genero exitosamente la Historia de Usuario para '{formatted_id} - {title}':")
    print(f"  - HU:           {target_hu_file}")
    print(f"  - Refinamiento: Pendiente (se creara en Fase 2 ejecutando '/refinar-hu {formatted_id}')")
    print(f"  - Bitacora Dev: Pendiente (se creara en Fase 5 ejecutando '/cerrar-hu {formatted_id}')")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Generador estandarizado de artefactos para Historias de Usuario (Scrum AI-First)."
    )
    parser.add_argument(
        "id",
        type=str,
        help="Identificador de la HU (ej. 001 o HU-001).",
    )
    parser.add_argument(
        "title",
        type=str,
        help="Título descriptivo de la Historia de Usuario.",
    )
    parser.add_argument(
        "--path",
        "--target-dir",
        "-p",
        "-t",
        dest="target_dir",
        type=Path,
        default=Path("."),
        help="Directorio raiz del proyecto donde se ubica la carpeta central de documentacion.",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=None,
        help="Ruta a la carpeta de plantillas (por defecto se busca templates/ relativa al script).",
    )
    parser.add_argument(
        "--docs-dir",
        "-d",
        type=str,
        default="automanagement_docs",
        help="Nombre de la carpeta central de documentacion (por defecto: automanagement_docs).",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Sobrescribe archivos si ya existen.",
    )
    parser.add_argument(
        "--raw-id",
        action="store_true",
        help="Conserva el ID exactamente como fue ingresado sin anteponer prefijo HU-.",
    )

    args = parser.parse_args()

    resolved_templates_dir = args.templates_dir
    if resolved_templates_dir is None:
        resolved_templates_dir = Path(__file__).resolve().parent.parent / "templates"

    return scaffold_hu(
        hu_id=args.id,
        title=args.title,
        target_dir=args.target_dir,
        templates_dir=resolved_templates_dir,
        docs_dir_name=args.docs_dir,
        force=args.force,
        force_raw=args.raw_id,
    )


if __name__ == "__main__":
    sys.exit(main())
