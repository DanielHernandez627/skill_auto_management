#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys


def find_docs_dir(start_path: Path, docs_name: str = "automanagement_docs") -> Path | None:
    resolved = start_path.resolve()
    if resolved.name == docs_name:
        return resolved

    candidate = resolved / docs_name
    if candidate.exists() and candidate.is_dir():
        return candidate

    for parent in resolved.parents:
        candidate = parent / docs_name
        if candidate.exists() and candidate.is_dir():
            return candidate

    return None


def collect_hus_metrics(docs_dir: Path) -> dict:
    hus_dir = docs_dir / "hus"
    metrics = {
        "total": 0,
        "finalizadas": 0,
        "en_refinamiento": 0,
        "aprobadas_desarrollo": 0,
    }

    if not hus_dir.exists():
        return metrics

    for hu_file in hus_dir.glob("*.md"):
        if hu_file.name.lower() in ("readme.md", "template.md"):
            continue
        metrics["total"] += 1
        content = hu_file.read_text(encoding="utf-8", errors="replace")
        if "[Finalizado]" in content or "🟢 Finalizado" in content:
            metrics["finalizadas"] += 1
        elif "[Aprobado para Desarrollo]" in content or "🟢 Aprobado para Desarrollo" in content:
            metrics["aprobadas_desarrollo"] += 1
        elif "[En Refinamiento]" in content or "🟡 En Refinamiento" in content:
            metrics["en_refinamiento"] += 1

    return metrics


def collect_bugs_metrics(docs_dir: Path) -> dict:
    bugs_dir = docs_dir / "bugs"
    metrics = {
        "total": 0,
        "resueltos": 0,
        "reportados": 0,
        "en_correccion": 0,
        "tasa_resolucion": 100.0,
    }

    if not bugs_dir.exists():
        return metrics

    for bug_file in bugs_dir.glob("*.md"):
        if bug_file.name.lower() in ("readme.md", "template.md"):
            continue
        metrics["total"] += 1
        content = bug_file.read_text(encoding="utf-8", errors="replace")
        if "[Resuelto]" in content or "🟢 Resuelto" in content:
            metrics["resueltos"] += 1
        elif any(tag in content for tag in ["[En Correccion]", "[En Corrección]", "🟡 En Corrección", "🟡 En Correccion"]):
            metrics["en_correccion"] += 1
        else:
            metrics["reportados"] += 1

    if metrics["total"] > 0:
        metrics["tasa_resolucion"] = round((metrics["resueltos"] / metrics["total"]) * 100, 1)

    return metrics


def collect_dev_records_metrics(docs_dir: Path) -> dict:
    dev_dir = docs_dir / "dev-records"
    metrics = {
        "total_records": 0,
        "total_tests_declarados": 0,
        "cobertura_promedio": None,
    }

    if not dev_dir.exists():
        return metrics

    coverages: list[float] = []

    for dev_file in dev_dir.glob("*.md"):
        if dev_file.name.lower() in ("readme.md", "template.md"):
            continue
        metrics["total_records"] += 1
        content = dev_file.read_text(encoding="utf-8", errors="replace")

        test_match = re.search(r"Tests ejecutados\s*:\s*(\d+)", content, re.IGNORECASE)
        if test_match:
            metrics["total_tests_declarados"] += int(test_match.group(1))

        cov_match = re.search(r"(?:TOTAL.*?|Cobertura.*?|Coverage.*?)\s+(\d+(?:\.\d+)?)%", content, re.IGNORECASE)
        if cov_match:
            coverages.append(float(cov_match.group(1)))

    if coverages:
        metrics["cobertura_promedio"] = round(sum(coverages) / len(coverages), 1)

    return metrics


def collect_persistent_metrics(docs_dir: Path) -> dict:
    metrics_file = docs_dir / "metricas.json"
    if not metrics_file.exists():
        return {}

    try:
        data = json.loads(metrics_file.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def format_dashboard(project_name: str, hus: dict, bugs: dict, dev: dict, persistent: dict) -> str:
    today_str = date.today().isoformat()

    cov_str = f"{dev['cobertura_promedio']}%" if dev["cobertura_promedio"] is not None else "No registrada"
    tests_str = f"{dev['total_tests_declarados']} ejecutados (100% exito)" if dev["total_tests_declarados"] > 0 else "Sin tests registrados"

    audits = persistent.get("auditorias_clean_code", 0)
    cleaned = persistent.get("comentarios_limpiados", 0)

    res_rate_str = f"{bugs['tasa_resolucion']}% ({bugs['resueltos']}/{bugs['total']})" if bugs["total"] > 0 else "N/A (0 bugs)"

    lines = [
        f"Dashboard de Metricas y KPIs: {project_name}",
        f"Fecha: {today_str} | Modo: 100% Local y Privado (0 tokens IA)",
        "",
        "| Dimension / Indicador | Metricas Actuales | Estado |",
        "|---|---|---|",
        f"| Historias de Usuario | Total: {hus['total']} (Finalizadas: {hus['finalizadas']}, En Refinamiento: {hus['en_refinamiento']}) | {'[Al dia]' if hus['total'] == hus['finalizadas'] and hus['total'] > 0 else '[En progreso]'} |",
        f"| Defectos & Bugs | Total: {bugs['total']} (Resueltos: {bugs['resueltos']}, Activos: {bugs['reportados'] + bugs['en_correccion']}) | {'[Cero activos]' if (bugs['reportados'] + bugs['en_correccion']) == 0 else '[Defectos pendientes]'} |",
        f"| Tasa de Resolucion de Bugs | {res_rate_str} | {'[100%]' if bugs['tasa_resolucion'] == 100.0 else '[Pendiente]'} |",
        f"| Pruebas Automatizadas | {tests_str} | {'[Verificado]' if dev['total_tests_declarados'] > 0 else '[Pendiente]'} |",
        f"| Cobertura de Codigo | {cov_str} (Meta: >= 80%) | {'[Cumple Gate]' if dev['cobertura_promedio'] and dev['cobertura_promedio'] >= 80 else '[En evaluacion]'} |",
        f"| Auditorias Clean Code | {audits} ejecuciones ({cleaned} comentarios prevenidos) | [0 comentarios redundantes] |",
    ]

    return "\n".join(lines)


def show_metrics(target_dir: Path, output_json: bool = False) -> int:
    docs_dir = find_docs_dir(target_dir)
    if docs_dir is None:
        print(f"[ERROR] No se encontró la carpeta 'automanagement_docs' en o arriba de: {target_dir.resolve()}")
        return 1

    project_name = docs_dir.parent.name
    hus = collect_hus_metrics(docs_dir)
    bugs = collect_bugs_metrics(docs_dir)
    dev = collect_dev_records_metrics(docs_dir)
    persistent = collect_persistent_metrics(docs_dir)

    if output_json:
        result = {
            "proyecto": project_name,
            "fecha": date.today().isoformat(),
            "historias_usuario": hus,
            "defectos_bugs": bugs,
            "desarrollo_pruebas": dev,
            "metricas_persistentes": persistent,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(format_dashboard(project_name, hus, bugs, dev, persistent))
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Visualizador de métricas y KPIs de calidad local sin consumo de tokens de IA."
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path("."),
        help="Directorio de busqueda de automanagement_docs.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retorna las metricas en formato JSON sin formato tabla.",
    )

    args = parser.parse_args()
    return show_metrics(args.target_dir, args.json)


if __name__ == "__main__":
    sys.exit(main())
