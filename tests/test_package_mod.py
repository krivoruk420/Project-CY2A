from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from package_mod import PackagingError, package_mod  # noqa: E402


class PackageModTests(unittest.TestCase):
    def test_missing_game_files_fails_without_creating_archive(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temporary:
            root = Path(temporary)
            output = root / "dist"
            (root / "game/vehicles/hirochi_cuirassier").mkdir(parents=True)

            with self.assertRaisesRegex(PackagingError, "No vehicle files found"):
                package_mod(root, output)
            self.assertFalse((output / "hirochi_cuirassier.zip").exists())

    def test_packages_only_vehicle_tree_at_expected_archive_path(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temporary:
            root = Path(temporary)
            vehicle = root / "game/vehicles/hirochi_cuirassier"
            (vehicle / "subfolder").mkdir(parents=True)
            (vehicle / "info.json").write_text('{"Name":"Test"}', encoding="utf-8")
            (vehicle / "subfolder/test.jbeam").write_text("{}", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs/README.md").write_text("not packaged", encoding="utf-8")

            archive_path = package_mod(root, root / "dist")
            with ZipFile(archive_path) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {
                        "vehicles/hirochi_cuirassier/info.json",
                        "vehicles/hirochi_cuirassier/subfolder/test.jbeam",
                    },
                )


if __name__ == "__main__":
    unittest.main()
