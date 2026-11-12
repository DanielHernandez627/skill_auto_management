from dataclasses import dataclass, field
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.onboard_project import detect_stack, onboard_project, resolve_true_project_root
from scripts.scaffold_bug import scaffold_bug
from scripts.scaffold_hu import scaffold_hu
from scripts.show_metrics import collect_hus_metrics
from scripts.validate_clean_code import CleanCodeValidator

SUCCESS_EXIT_CODE = 0
SINGLE_ITEM_COUNT = 1
TWO_ITEMS_COUNT = 2
ZERO_FINDINGS_COUNT = 0
EXPECTED_COMMENT_LINE_NUMBER = 2
DOCS_DIR_NAME = "automanagement_docs"


@dataclass
class HuScenarioConfig:
    hu_id: str = "001"
    title: str = "Autenticacion Segura"
    status: str = "[En Refinamiento]"
    docs_dir_name: str = DOCS_DIR_NAME
    force: bool = True


class HuScenarioDataBuilder:
    def __init__(self) -> None:
        self._config = HuScenarioConfig()

    def with_id(self, hu_id: str) -> "HuScenarioDataBuilder":
        self._config.hu_id = hu_id
        return self

    def with_title(self, title: str) -> "HuScenarioDataBuilder":
        self._config.title = title
        return self

    def with_status(self, status: str) -> "HuScenarioDataBuilder":
        self._config.status = status
        return self

    def build(self) -> HuScenarioConfig:
        return self._config


@dataclass
class WorkspaceFixture:
    root_dir: Path
    templates_dir: Path
    docs_dir: Path
    created_files: list[Path] = field(default_factory=list)


class WorkspaceFixtureDataBuilder:
    def __init__(self, base_temp_dir: Path, templates_dir: Path) -> None:
        self._root_dir = base_temp_dir
        self._templates_dir = templates_dir
        self._files_to_create: dict[str, str] = {}
        self._dirs_to_create: list[str] = []
        self._hus_to_seed: list[HuScenarioConfig] = []

    def with_git_root(self) -> "WorkspaceFixtureDataBuilder":
        self._dirs_to_create.append(".git")
        return self

    def with_nested_git_repo(self, folder_name: str) -> "WorkspaceFixtureDataBuilder":
        self._dirs_to_create.append(f"{folder_name}/.git")
        return self

    def with_file(self, relative_path: str, content: str) -> "WorkspaceFixtureDataBuilder":
        self._files_to_create[relative_path] = content
        return self

    def with_multilanguage_descriptors(self) -> "WorkspaceFixtureDataBuilder":
        self._files_to_create["go.mod"] = "module example.com/app"
        self._files_to_create["Cargo.toml"] = "[package]\nname = 'app'"
        self._files_to_create["composer.json"] = "{}"
        self._files_to_create["App.csproj"] = "<Project></Project>"
        return self

    def with_seeded_hu(self, hu_config: HuScenarioConfig) -> "WorkspaceFixtureDataBuilder":
        self._hus_to_seed.append(hu_config)
        return self

    def build(self) -> WorkspaceFixture:
        for rel_dir in self._dirs_to_create:
            (self._root_dir / rel_dir).mkdir(parents=True, exist_ok=True)

        created_files: list[Path] = []
        for rel_file, content in self._files_to_create.items():
            file_path = self._root_dir / rel_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            created_files.append(file_path)

        docs_dir = self._root_dir / DOCS_DIR_NAME
        if self._hus_to_seed:
            hus_dir = docs_dir / "hus"
            hus_dir.mkdir(parents=True, exist_ok=True)
            for hu in self._hus_to_seed:
                hu_file = hus_dir / f"{hu.hu_id}.md"
                hu_file.write_text(f"**Estado:** {hu.status}\n", encoding="utf-8")
                created_files.append(hu_file)

        return WorkspaceFixture(
            root_dir=self._root_dir,
            templates_dir=self._templates_dir,
            docs_dir=docs_dir,
            created_files=created_files,
        )


class TestCliStandardizationAndScripts(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.repo_root = Path(os.path.abspath(__file__)).parent.parent
        self.templates_dir = self.repo_root / "templates"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_resolve_true_project_root_with_direct_git(self) -> None:
        fixture = WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir).with_git_root().build()

        resolved = resolve_true_project_root(fixture.root_dir)

        self.assertEqual(resolved, fixture.root_dir)

    def test_resolve_true_project_root_with_nested_git(self) -> None:
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_nested_git_repo("resource_monitor")
            .build()
        )

        resolved = resolve_true_project_root(fixture.root_dir)

        self.assertEqual(resolved, fixture.root_dir / "resource_monitor")

    def test_resolve_true_project_root_with_nested_descriptor(self) -> None:
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_file("backend_service/pom.xml", "<project></project>")
            .build()
        )

        resolved = resolve_true_project_root(fixture.root_dir)

        self.assertEqual(resolved, fixture.root_dir / "backend_service")

    def test_detect_stack_multilanguage(self) -> None:
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_multilanguage_descriptors()
            .build()
        )

        stack = detect_stack(fixture.root_dir)

        self.assertIn("Go", stack["languages"])
        self.assertIn("Rust", stack["languages"])
        self.assertIn("PHP", stack["languages"])
        self.assertIn("C# (.NET)", stack["languages"])

    def test_scaffold_hu_creates_hu_and_initializes_missing_readme_index(self) -> None:
        fixture = WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir).build()
        hu_scenario = HuScenarioDataBuilder().with_id("001").with_title("Autenticacion Segura").build()

        exit_code = scaffold_hu(
            hu_id=hu_scenario.hu_id,
            title=hu_scenario.title,
            target_dir=fixture.root_dir,
            templates_dir=fixture.templates_dir,
            docs_dir_name=hu_scenario.docs_dir_name,
            force=hu_scenario.force,
        )

        hu_path = fixture.docs_dir / "hus" / "HU-001.md"
        readme_path = fixture.docs_dir / "README.md"
        self.assertEqual(exit_code, SUCCESS_EXIT_CODE)
        self.assertTrue(hu_path.exists())
        self.assertTrue(readme_path.exists())
        self.assertIn("HU-001", hu_path.read_text(encoding="utf-8"))
        self.assertIn("[`HU-001`](hus/HU-001.md)", readme_path.read_text(encoding="utf-8"))

    def test_scaffold_bug_creates_structure(self) -> None:
        fixture = WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir).build()

        exit_code = scaffold_bug(
            bug_id="BUG-001-01",
            title="Fallo en inicio de sesion",
            hu_id="HU-001",
            severity="Alta",
            target_dir=fixture.root_dir,
            templates_dir=fixture.templates_dir,
            docs_dir_name=DOCS_DIR_NAME,
            force=True,
        )

        bug_path = fixture.docs_dir / "bugs" / "BUG-001-01.md"
        self.assertEqual(exit_code, SUCCESS_EXIT_CODE)
        self.assertTrue(bug_path.exists())

    def test_calculate_metrics_offline(self) -> None:
        first_hu = HuScenarioDataBuilder().with_id("HU-001").with_status("[Finalizado]").build()
        second_hu = HuScenarioDataBuilder().with_id("HU-002").with_status("[Aprobado para Desarrollo]").build()
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_seeded_hu(first_hu)
            .with_seeded_hu(second_hu)
            .build()
        )

        metrics = collect_hus_metrics(fixture.docs_dir)

        self.assertEqual(metrics["total"], TWO_ITEMS_COUNT)
        self.assertEqual(metrics["finalizadas"], SINGLE_ITEM_COUNT)
        self.assertEqual(metrics["aprobadas_desarrollo"], SINGLE_ITEM_COUNT)

    def test_validate_clean_code_detects_comments(self) -> None:
        commented_code = "first_value = 1\n" + chr(35) + " comentario explicativo\nsecond_value = 2\n"
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_file("sample.py", commented_code)
            .build()
        )
        validator = CleanCodeValidator(target_path=fixture.root_dir, allowed_extensions={".py"})

        files_scanned, findings = validator.execute()

        self.assertEqual(files_scanned, SINGLE_ITEM_COUNT)
        self.assertEqual(len(findings), SINGLE_ITEM_COUNT)
        self.assertEqual(findings[0].line_number, EXPECTED_COMMENT_LINE_NUMBER)

    def test_validate_clean_code_clean_file(self) -> None:
        fixture = (
            WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir)
            .with_file("clean.py", "first_value = 1\nsecond_value = 2\n")
            .build()
        )
        validator = CleanCodeValidator(target_path=fixture.root_dir, allowed_extensions={".py"})

        files_scanned, findings = validator.execute()

        self.assertEqual(files_scanned, SINGLE_ITEM_COUNT)
        self.assertEqual(len(findings), ZERO_FINDINGS_COUNT)

    def test_onboard_project_generates_knowledge_base_with_magic_numbers_and_aaa_databuilder_rules(self) -> None:
        fixture = WorkspaceFixtureDataBuilder(self.temp_dir, self.templates_dir).with_git_root().build()

        exit_code = onboard_project(
            project_dir=fixture.root_dir,
            templates_dir=fixture.templates_dir,
            project_name="SistemaPruebaTecnica",
            docs_dir=DOCS_DIR_NAME,
            force=True,
        )

        dev_standards = (fixture.docs_dir / "base-conocimiento" / "02-estandares-desarrollo.md").read_text(
            encoding="utf-8"
        )
        test_standards = (fixture.docs_dir / "base-conocimiento" / "03-estandares-pruebas.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(exit_code, SUCCESS_EXIT_CODE)
        self.assertIn("Números Mágicos", dev_standards)
        self.assertIn("Patrón AAA", test_standards)
        self.assertIn("Data Builder", test_standards)

    def test_iniciarproyecto_commands_enforce_guardrails_backlog_hu_split_and_standards_alignment(self) -> None:
        claude_cmd_path = self.repo_root / ".claude" / "commands" / "iniciarproyecto.md"
        copilot_prompt_path = self.repo_root / ".github" / "prompts" / "iniciarproyecto.prompt.md"
        skill_path = self.repo_root / "SKILL.md"

        claude_cmd_content = claude_cmd_path.read_text(encoding="utf-8")
        copilot_prompt_content = copilot_prompt_path.read_text(encoding="utf-8")
        skill_content = skill_path.read_text(encoding="utf-8")

        for document_content in (claude_cmd_content, copilot_prompt_content, skill_content):
            self.assertIn("PROHIBIDO", document_content)
            self.assertIn("Números Mágicos", document_content)
            self.assertIn("AAA", document_content)
            self.assertIn("Data Builder", document_content)
            self.assertIn("Backlog", document_content)


if __name__ == "__main__":
    unittest.main()
