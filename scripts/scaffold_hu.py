#!/usr/bin/env python3
"""Generador de Artefactos de Historias de Usuario (Scaffolding).

Crea de forma estandarizada los 3 documentos Markdown para una nueva HU:
1. hus/HU-XXX.md
2. refinamientos/REF-XXX.md
3. dev-records/DEV-RECORD-HU-XXX.md
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys


def scaffold_hu(
    hu_id: str,
    title: str,
    target_dir: Path,
    templates_dir: Path,
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
            print(f"❌ Error: No se encontro la plantilla requerida en '{tpl}'.")
            return 1

    hus_dir = target_dir / "hus"
    refinamientos_dir = target_dir / "refinamientos"
    dev_records_dir = target_dir / "dev-records"

    hus_dir.mkdir(parents=True, exist_ok=True)
    refinamientos_dir.mkdir(parents=True, exist_ok=True)
    dev_records_dir.mkdir(parents=True, exist_ok=True)

    target_hu_file = hus_dir / f"{formatted_id}.md"
    target_ref_file = refinamientos_dir / f"{ref_id}.md"
    target_dev_file = dev_records_dir / dev_record_name

    existing_files = [f for f in (target_hu_file, target_ref_file, target_dev_file) if f.exists()]
    if existing_files and not force:
        print("⚠️ Los siguientes archivos ya existen. Usa --force para sobrescribir:")
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
        help="Directorio raiz donde se crearan las carpetas hus/, refinamientos/ y dev-records/.",
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=None,
        help="Ruta a la carpeta de plantillas (por defecto se busca templates/ relativa al script).",
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
        force=args.force,
    )


if __name__ == "__main__":
    sys.exit(main())
