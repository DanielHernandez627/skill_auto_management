import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.onboard_project import resolve_true_project_root, detect_stack
from scripts.scaffold_hu import scaffold_hu
from scripts.scaffold_bug import scaffold_bug
from scripts.show_metrics import collect_hus_metrics
from scripts.validate_clean_code import CleanCodeValidator, CommentFinding


class TestCliStandardizationAndScripts(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_resolve_true_project_root_with_direct_git(self):
        (self.temp_dir / ".git").mkdir()
        resolved = resolve_true_project_root(self.temp_dir)
        self.assertEqual(resolved, self.temp_dir)

    def test_resolve_true_project_root_with_nested_git(self):
        nested = self.temp_dir / "resource_monitor"
        nested.mkdir()
        (nested / ".git").mkdir()
        resolved = resolve_true_project_root(self.temp_dir)
        self.assertEqual(resolved, nested)

    def test_resolve_true_project_root_with_nested_descriptor(self):
        nested = self.temp_dir / "backend_service"
        nested.mkdir()
        (nested / "pom.xml").write_text("<project></project>", encoding="utf-8")
        resolved = resolve_true_project_root(self.temp_dir)
        self.assertEqual(resolved, nested)

    def test_detect_stack_multilanguage(self):
        (self.temp_dir / "go.mod").write_text("module example.com/app", encoding="utf-8")
        (self.temp_dir / "Cargo.toml").write_text("[package]\nname = 'app'", encoding="utf-8")
        (self.temp_dir / "composer.json").write_text("{}", encoding="utf-8")
        (self.temp_dir / "App.csproj").write_text("<Project></Project>", encoding="utf-8")

        stack = detect_stack(self.temp_dir)
        self.assertIn("Go", stack["languages"])
        self.assertIn("Rust", stack["languages"])
        self.assertIn("PHP", stack["languages"])
        self.assertIn("C# (.NET)", stack["languages"])

    def test_scaffold_hu_formats_and_creates_structure(self):
        templates_dir = Path(__file__).resolve().parent.parent / "templates"
        res = scaffold_hu(
            hu_id="001",
            title="Autenticacion Segura",
            target_dir=self.temp_dir,
            templates_dir=templates_dir,
            docs_dir_name="automanagement_docs",
            force=True,
        )
        self.assertEqual(res, 0)
        hu_path = self.temp_dir / "automanagement_docs" / "hus" / "HU-001.md"
        self.assertTrue(hu_path.exists())
        content = hu_path.read_text(encoding="utf-8")
        self.assertIn("HU-001", content)
        self.assertIn("Autenticacion Segura", content)

    def test_scaffold_bug_creates_structure(self):
        templates_dir = Path(__file__).resolve().parent.parent / "templates"
        res = scaffold_bug(
            bug_id="BUG-001-01",
            title="Fallo en inicio de sesion",
            hu_id="HU-001",
            severity="Alta",
            target_dir=self.temp_dir,
            templates_dir=templates_dir,
            docs_dir_name="automanagement_docs",
            force=True,
        )
        self.assertEqual(res, 0)
        bug_path = self.temp_dir / "automanagement_docs" / "bugs" / "BUG-001-01.md"
        self.assertTrue(bug_path.exists())

    def test_calculate_metrics_offline(self):
        docs_dir = self.temp_dir / "automanagement_docs"
        docs_dir.mkdir(parents=True)
        hus_dir = docs_dir / "hus"
        hus_dir.mkdir()
        (hus_dir / "HU-001.md").write_text("**Estado:** [Finalizado]\n", encoding="utf-8")
        (hus_dir / "HU-002.md").write_text("**Estado:** [Aprobado para Desarrollo]\n", encoding="utf-8")

        metrics = collect_hus_metrics(docs_dir)
        self.assertEqual(metrics["total"], 2)
        self.assertEqual(metrics["finalizadas"], 1)
        self.assertEqual(metrics["aprobadas_desarrollo"], 1)

    def test_validate_clean_code_detects_comments(self):
        code_file = self.temp_dir / "sample.py"
        code_file.write_text("x = 1\n# comentario explicativo\ny = 2\n", encoding="utf-8")

        validator = CleanCodeValidator(target_path=self.temp_dir, allowed_extensions={".py"})
        files_scanned, findings = validator.execute()
        self.assertEqual(files_scanned, 1)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line_number, 2)

    def test_validate_clean_code_clean_file(self):
        code_file = self.temp_dir / "clean.py"
        code_file.write_text("x = 1\ny = 2\n", encoding="utf-8")

        validator = CleanCodeValidator(target_path=self.temp_dir, allowed_extensions={".py"})
        files_scanned, findings = validator.execute()
        self.assertEqual(files_scanned, 1)
        self.assertEqual(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
