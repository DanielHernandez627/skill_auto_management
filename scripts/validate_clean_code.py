#!/usr/bin/env python3
"""Auditor de Clean Code Multilenguaje.

Verifica la ausencia de comentarios redundantes o explicativos dentro de
archivos de codigo fuente para C# (.cs), Java (.java), TypeScript (.ts),
JavaScript (.js), Python (.py), Go (.go), Rust (.rs), C/C++ (.cpp, .c) y mas.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass
class CommentFinding:
    file_path: Path
    line_number: int
    content: str
    comment_type: str


def find_git_root(target: Path) -> Path | None:
    current = target if target.is_dir() else target.parent
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=current,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return Path(res.stdout.strip()).resolve()
    except Exception:
        pass
    return None


def get_git_diff_info(git_root: Path, base: str | None = None) -> tuple[dict[Path, set[int]], set[Path]]:
    modified_lines: dict[Path, set[int]] = {}
    untracked_files: set[Path] = set()

    diff_cmd = ["git", "diff", "-U0"]
    if base:
        diff_cmd.append(base)
    else:
        diff_cmd.append("HEAD")

    try:
        res = subprocess.run(
            diff_cmd,
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        diff_output = res.stdout
        if res.returncode != 0 and not base:
            res_fallback = subprocess.run(
                ["git", "diff", "-U0"],
                cwd=git_root,
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
            diff_output = res_fallback.stdout

        current_file: Path | None = None
        for line in diff_output.splitlines():
            if line.startswith("+++ b/"):
                rel_path = line[6:].strip()
                current_file = (git_root / rel_path).resolve()
                if current_file not in modified_lines:
                    modified_lines[current_file] = set()
            elif line.startswith("@@ ") and current_file is not None:
                match = re.search(r"\+([0-9]+)(?:,([0-9]+))?", line)
                if match:
                    start = int(match.group(1))
                    count = int(match.group(2)) if match.group(2) is not None else 1
                    for lno in range(start, start + count):
                        modified_lines[current_file].add(lno)

        if not modified_lines and not base:
            res_parent = subprocess.run(
                ["git", "diff", "-U0", "HEAD~1"],
                cwd=git_root,
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
            if res_parent.returncode == 0 and res_parent.stdout.strip():
                diff_output = res_parent.stdout
                current_file = None
                for line in diff_output.splitlines():
                    if line.startswith("+++ b/"):
                        rel_path = line[6:].strip()
                        current_file = (git_root / rel_path).resolve()
                        if current_file not in modified_lines:
                            modified_lines[current_file] = set()
                    elif line.startswith("@@ ") and current_file is not None:
                        match = re.search(r"\+([0-9]+)(?:,([0-9]+))?", line)
                        if match:
                            start = int(match.group(1))
                            count = int(match.group(2)) if match.group(2) is not None else 1
                            for lno in range(start, start + count):
                                modified_lines[current_file].add(lno)
    except Exception:
        pass

    try:
        res_status = subprocess.run(
            ["git", "status", "--porcelain", "-u"],
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        if res_status.returncode == 0:
            for line in res_status.stdout.splitlines():
                if line.startswith("?? "):
                    entry = line[3:].strip().strip('"')
                    entry_path = (git_root / entry).resolve()
                    if entry_path.is_file():
                        untracked_files.add(entry_path)
                    elif entry_path.is_dir():
                        for p in entry_path.rglob("*"):
                            if p.is_file():
                                untracked_files.add(p.resolve())
    except Exception:
        pass

    return modified_lines, untracked_files


class CleanCodeValidator:
    DEFAULT_IGNORED_DIRS: ClassVar[set[str]] = {
        ".git",
        "bin",
        "obj",
        "node_modules",
        "dist",
        "target",
        "build",
        ".angular",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        ".vs",
        "packages",
    }

    C_STYLE_EXTENSIONS: ClassVar[set[str]] = {
        ".cs",
        ".java",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".go",
        ".rs",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".kt",
        ".swift",
        ".dart",
        ".php",
    }

    HASH_STYLE_EXTENSIONS: ClassVar[set[str]] = {
        ".py",
        ".rb",
        ".sh",
        ".bash",
        ".ps1",
        ".r",
        ".yaml",
        ".yml",
    }

    DASH_STYLE_EXTENSIONS: ClassVar[set[str]] = {
        ".sql",
        ".lua",
    }

    def __init__(
        self,
        target_path: Path,
        allowed_extensions: set[str] | None = None,
        extra_ignored_dirs: set[str] | None = None,
        only_diff: bool = False,
        diff_base: str | None = None,
    ):
        self.target_path = target_path.resolve()
        self.ignored_dirs = self.DEFAULT_IGNORED_DIRS | (extra_ignored_dirs or set())
        self.only_diff = only_diff
        self.diff_base = diff_base
        self.modified_lines: dict[Path, set[int]] = {}
        self.untracked_files: set[Path] = set()
        self.diff_initialized = False

        if allowed_extensions:
            self.allowed_extensions = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in allowed_extensions}
        else:
            self.allowed_extensions = self.C_STYLE_EXTENSIONS | self.HASH_STYLE_EXTENSIONS | self.DASH_STYLE_EXTENSIONS

    def init_git_diff(self) -> None:
        if not self.only_diff:
            return
        git_root = find_git_root(self.target_path)
        if git_root is None:
            print("[WARN] Modo --only-diff requiere un repositorio Git. Continuando con escaneo completo.")
            return
        self.modified_lines, self.untracked_files = get_git_diff_info(git_root, self.diff_base)
        self.diff_initialized = True

    def should_skip_directory(self, dir_path: Path) -> bool:
        return any(part in self.ignored_dirs for part in dir_path.parts)

    def scan_file(self, file_path: Path) -> list[CommentFinding]:
        findings: list[CommentFinding] = []
        ext = file_path.suffix.lower()

        try:
            with file_path.open("r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception:
            return findings

        if ext in self.C_STYLE_EXTENSIONS:
            findings.extend(self._scan_c_style(file_path, lines))
        elif ext in self.HASH_STYLE_EXTENSIONS:
            findings.extend(self._scan_hash_style(file_path, lines))
        elif ext in self.DASH_STYLE_EXTENSIONS:
            findings.extend(self._scan_dash_style(file_path, lines))

        return findings

    def _scan_c_style(self, file_path: Path, lines: list[str]) -> list[CommentFinding]:
        findings: list[CommentFinding] = []
        in_multiline_comment = False

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            if in_multiline_comment:
                findings.append(CommentFinding(file_path, idx, stripped, "Bloque multilínea (/* ... */)"))
                if "*/" in line:
                    in_multiline_comment = False
                continue

            if "/*" in line:
                cleaned_before = line.split("/*")[0]
                if cleaned_before.count('"') % 2 == 0 and cleaned_before.count("'") % 2 == 0:
                    findings.append(CommentFinding(file_path, idx, stripped, "Inicio de bloque (/*)"))
                    if "*/" not in line or line.find("*/") < line.find("/*"):
                        in_multiline_comment = True
                    continue

            if "//" in line:
                cleaned_before = line.split("//")[0]
                if cleaned_before.count('"') % 2 == 0 and cleaned_before.count("'") % 2 == 0 and cleaned_before.count("`") % 2 == 0:
                    findings.append(CommentFinding(file_path, idx, stripped, "Línea simple (//)"))

        return findings

    def _scan_hash_style(self, file_path: Path, lines: list[str]) -> list[CommentFinding]:
        findings: list[CommentFinding] = []

        if file_path.suffix.lower() == ".py":
            import tokenize

            try:
                with file_path.open("rb") as f:
                    tokens = tokenize.tokenize(f.readline)
                    for token in tokens:
                        if token.type == tokenize.COMMENT:
                            line_no = token.start[0]
                            content = token.string.strip()
                            if line_no == 1 and content.startswith("#!"):
                                continue
                            findings.append(CommentFinding(file_path, line_no, content, "Comentario Python (#)"))
                return findings
            except Exception:
                pass

        in_multiline_str = False
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if idx == 1 and stripped.startswith("#!"):
                continue

            if '"""' in line or "'''" in line:
                in_multiline_str = not in_multiline_str

            if in_multiline_str:
                continue

            if "#" in line:
                cleaned_before = line.split("#")[0]
                if cleaned_before.count('"') % 2 == 0 and cleaned_before.count("'") % 2 == 0:
                    findings.append(CommentFinding(file_path, idx, stripped, "Comentario hash (#)"))

        return findings

    def _scan_dash_style(self, file_path: Path, lines: list[str]) -> list[CommentFinding]:
        findings: list[CommentFinding] = []

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if "--" in line:
                cleaned_before = line.split("--")[0]
                if cleaned_before.count("'") % 2 == 0:
                    findings.append(CommentFinding(file_path, idx, stripped, "Comentario SQL (--)"))

        return findings

    def execute(self) -> tuple[int, list[CommentFinding]]:
        self.init_git_diff()
        findings: list[CommentFinding] = []
        files_scanned = 0

        if self.target_path.is_file():
            if self.target_path.suffix.lower() in self.allowed_extensions:
                if self.only_diff and self.diff_initialized:
                    if self.target_path in self.untracked_files:
                        files_scanned += 1
                        findings.extend(self.scan_file(self.target_path))
                    elif self.target_path in self.modified_lines:
                        files_scanned += 1
                        raw_findings = self.scan_file(self.target_path)
                        findings.extend(
                            [f for f in raw_findings if f.line_number in self.modified_lines[self.target_path]]
                        )
                else:
                    files_scanned += 1
                    findings.extend(self.scan_file(self.target_path))
            return files_scanned, findings

        for path in self.target_path.rglob("*"):
            if path.is_file():
                if self.should_skip_directory(path.parent):
                    continue
                if path.suffix.lower() in self.allowed_extensions:
                    resolved_file = path.resolve()
                    if self.only_diff and self.diff_initialized:
                        if resolved_file in self.untracked_files:
                            files_scanned += 1
                            findings.extend(self.scan_file(resolved_file))
                        elif resolved_file in self.modified_lines:
                            files_scanned += 1
                            raw_findings = self.scan_file(resolved_file)
                            findings.extend(
                                [
                                    f
                                    for f in raw_findings
                                    if f.line_number in self.modified_lines[resolved_file]
                                ]
                            )
                    else:
                        files_scanned += 1
                        findings.extend(self.scan_file(resolved_file))

        return files_scanned, findings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Audita codigo fuente para validar ausencia de comentarios explicativos redundantes (Clean Code)."
    )
    parser.add_argument(
        "--path",
        "--target-dir",
        "-p",
        "-t",
        dest="target_dir",
        type=Path,
        default=Path("."),
        help="Ruta al archivo o directorio a escanear (por defecto: directorio actual).",
    )
    parser.add_argument(
        "--ext",
        "-e",
        nargs="+",
        help="Extensiones especificas a auditar (ej. --ext .cs .ts .java .py).",
    )
    parser.add_argument(
        "--ignore-dirs",
        "-i",
        nargs="+",
        help="Carpetas adicionales a ignorar (ej. --ignore-dirs vendor generated).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Retorna codigo de salida 1 si se detecta cualquier comentario.",
    )
    parser.add_argument(
        "--only-diff",
        "--git-diff",
        action="store_true",
        dest="only_diff",
        help="Audita unicamente las lineas agregadas o modificadas en Git y archivos nuevos sin commitear.",
    )
    parser.add_argument(
        "--diff-base",
        type=str,
        default=None,
        help="Rama o commit base para comparar en Git diff (por defecto: HEAD o cambios en working tree).",
    )

    args = parser.parse_args()
    validator = CleanCodeValidator(
        target_path=args.target_dir,
        allowed_extensions=set(args.ext) if args.ext else None,
        extra_ignored_dirs=set(args.ignore_dirs) if args.ignore_dirs else None,
        only_diff=args.only_diff,
        diff_base=args.diff_base,
    )

    print(f"[SCAN] Escaneando Clean Code en: {validator.target_path}")
    print(f"[INFO] Extensiones admitidas: {', '.join(sorted(validator.allowed_extensions))}")
    if args.only_diff:
        print("[INFO] Modo incremental activado (--only-diff).")

    files_scanned, findings = validator.execute()
    print(f"[INFO] Archivos auditados: {files_scanned}")

    if not findings:
        print("[OK] Codigo limpio: 0 comentarios redundantes encontrados.")
        return 0

    print(f"\n[ALERTA] Se encontraron {len(findings)} comentarios en el codigo fuente:")
    print("-" * 80)
    for finding in findings:
        rel_path = finding.file_path.relative_to(validator.target_path) if validator.target_path.is_dir() else finding.file_path.name
        print(f"[{finding.comment_type}] {rel_path}:{finding.line_number}")
        print(f"    > {finding.content}")
    print("-" * 80)

    if args.strict:
        print("[FAIL] Fallo de validacion estricta de Clean Code.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
