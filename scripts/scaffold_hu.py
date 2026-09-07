#!/usr/bin/env python3
"""Generador de Artefactos de Historias de Usuario (Scaffolding).

Crea de forma estandarizada los documentos Markdown para una nueva HU en automanagement_docs/:
1. automanagement_docs/hus/HU-XXX.md
2. automanagement_docs/refinamientos/REF-XXX.md
3. automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md
4. automanagement_docs/README.md (registro y estado)
"""

from __future__ import annotations

import argparse
from datetime import date
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
    ref_id: str,
    dev_record_name: str,
) -> None:
    readme_file = docs_dir / "README.md"
    if not readme_file.exists():
        return

    content = readme_file.read_text(encoding="utf-8")
    if f"[`{hu_id}`]" in content:
        return

    row_entry = (
        f"| [`{hu_id}`](hus/{hu_id}.md) | {title} | 🟡 En Refinamiento | "
        f"[`{ref_id}`](refinamientos/{ref_id}.md) | "
        f"[`{dev_record_name}`](dev-records/{dev_record_name}) |"
    )

    placeholder = "| *(Las nuevas HUs creadas con `/nueva-hu` se registrarán en esta sección)* | | | | |"
    if placeholder in content:
        content = content.replace(placeholder, row_entry)
    elif "| ID | Título | Estado | Refinamiento | Registro Dev / QA |" in content:
        content = content.rstrip() + "\n" + row_entry + "\n"

    readme_file.write_text(content, encoding="utf-8")


def scaffold_hu(
    hu_id: str,
    title: str,
    target_dir: Path,
    templates_dir: Path,
    docs_dir_name: str = "automanagement_docs",
    force: bool = False,
) -> int:
    formatted_id = hu_id.upper().strip()
    if not formatted_id.startswith("HU-"):
        formatted_id = f"HU-{formatted_id}"

    ref_id = formatted_id.replace("HU-", "REF-")
    dev_record_name = f"DEV-RECORD-{formatted_id}.md"
    today_str = date.today().isoformat()

    hu_template_file = templates_dir / "hu-template.md"
    ref_template_file = templates_dir / "refinamiento-template.md"
    dev_template_file = templates_dir / "dev-record-template.md"

    for tpl in (hu_template_file, ref_template_file, dev_template_file):
        if not tpl.is_file():
            print(f"[ERROR] No se encontro la plantilla requerida en '{tpl}'.")
            return 1

    docs_base_dir = resolve_docs_directory(target_dir, docs_dir_name)
    hus_dir = docs_base_dir / "hus"
    refinamientos_dir = docs_base_dir / "refinamientos"
    dev_records_dir = docs_base_dir / "dev-records"

    hus_dir.mkdir(parents=True, exist_ok=True)
    refinamientos_dir.mkdir(parents=True, exist_ok=True)
    dev_records_dir.mkdir(parents=True, exist_ok=True)

    target_hu_file = hus_dir / f"{formatted_id}.md"
    target_ref_file = refinamientos_dir / f"{ref_id}.md"
    target_dev_file = dev_records_dir / dev_record_name

    existing_files = [f for f in (target_hu_file, target_ref_file, target_dev_file) if f.exists()]
    if existing_files and not force:
        print("[WARN] Los siguientes archivos ya existen. Usa --force para sobrescribir:")
        for ef in existing_files:
            print(f"  - {ef}")
        return 1

    hu_content = (
        hu_template_file.read_text(encoding="utf-8")
        .replace("[HU-XXX]", formatted_id)
        .replace("HU-XXX", formatted_id)
        .replace("[Título Corto de la Historia]", title)
        .replace("REF-XXX.md", f"{ref_id}.md")
        .replace("DEV-RECORD-HU-XXX.md", dev_record_name)
    )

    ref_content = (
        ref_template_file.read_text(encoding="utf-8")
        .replace("[REF-XXX]", ref_id)
        .replace("REF-XXX", ref_id)
        .replace("[Título de la HU]", title)
        .replace("HU-XXX.md", f"{formatted_id}.md")
        .replace("HU-XXX", formatted_id)
        .replace("YYYY-MM-DD", today_str)
        .replace("DEV-RECORD-HU-XXX.md", dev_record_name)
    )

    dev_content = (
        dev_template_file.read_text(encoding="utf-8")
        .replace("[DEV-RECORD-HU-XXX]", f"DEV-RECORD-{formatted_id}")
        .replace("DEV-RECORD-HU-XXX", f"DEV-RECORD-{formatted_id}")
        .replace("[Título de la HU]", title)
        .replace("HU-XXX.md", f"{formatted_id}.md")
        .replace("HU-XXX", formatted_id)
        .replace("REF-XXX.md", f"{ref_id}.md")
        .replace("REF-XXX", ref_id)
        .replace("YYYY-MM-DD", today_str)
    )

    target_hu_file.write_text(hu_content, encoding="utf-8")
    target_ref_file.write_text(ref_content, encoding="utf-8")
    target_dev_file.write_text(dev_content, encoding="utf-8")

    update_docs_index_table(docs_base_dir, formatted_id, title, ref_id, dev_record_name)

    print(f"[OK] Se generaron exitosamente los 3 artefactos para '{formatted_id} - {title}':")
    print(f"  - HU:           {target_hu_file}")
    print(f"  - Refinamiento: {target_ref_file}")
    print(f"  - Bitácora Dev: {target_dev_file}")
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
        "--target-dir",
        "-t",
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
    )


if __name__ == "__main__":
    sys.exit(main())
