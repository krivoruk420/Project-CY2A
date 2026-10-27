from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_documentation_exists(self):
        for relative in (
            "README.md",
            "docs/PROJECT_SPEC.md",
            "docs/ROADMAP.md",
            "docs/VEHICLE_DATA.md",
            "docs/DEVELOPMENT_GUIDE.md",
            "docs/THIRD_PARTY_MATERIALS.md",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_required_project_directories_exist(self):
        for relative in (
            "references/drawings",
            "references/dimensions",
            "references/photos",
            "references/technical_data",
            "source/blender/body",
            "source/blender/interior",
            "source/blender/mechanical",
            "source/textures",
            "game/vehicles/hirochi_cuirassier",
            "tools",
            "tests",
            "dist",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_dir())


if __name__ == "__main__":
    unittest.main()
