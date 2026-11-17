"""Exercise export and archive refresh using disposable repositories only."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


class Export(unittest.TestCase):
    def test_readme_survives_and_archives_match(self):
        here = pathlib.Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source, alto, icons = (root / name for name in ("source", "alto", "icons"))
            source.mkdir()
            for repo in (alto, icons):
                subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            for name in ("export_repos.py", "package.py", ".gitattributes", "LICENSE", "NOTICE.md",
                         "fonts/OFL-EBGaramond.txt", "fonts/archivo/OFL-Archivo.txt", "fonts/nimbus/COPYING", "fonts/nimbus/LICENSE"):
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(here / name, target)
            for folder, name in ((source, "Plectics Alto"), (source / "themes/Plectics Alto Icons", "Plectics Alto Icons")):
                folder.mkdir(parents=True, exist_ok=True)
                (folder / "manifest.json").write_text(json.dumps({"name": name}), encoding="utf-8")
                (folder / "theme.css").write_text("body { color: red; }", encoding="utf-8")
            (source / "themes/Plectics Alto Icons/README.md").write_text("nested pointer", encoding="utf-8")
            (icons / "README.md").write_text("Detailed installation guide", encoding="utf-8")
            subprocess.run([sys.executable, "-I", str(source / "export_repos.py"), str(alto), str(icons)], check=True, capture_output=True)
            self.assertEqual((icons / "README.md").read_text(encoding="utf-8"), "Detailed installation guide")
            for repo, name in ((alto, "Plectics Alto"), (icons, "Plectics Alto Icons")):
                archive = repo / "downloads" / (name.lower().replace(" ", "-") + ".zip")
                with zipfile.ZipFile(archive) as package:
                    self.assertIsNone(package.testzip())
                    self.assertEqual(package.read(name + "/theme.css"), (repo / "theme.css").read_bytes())


if __name__ == "__main__":
    unittest.main()
