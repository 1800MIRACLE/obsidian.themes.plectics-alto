"""Build destination regression checks for buildalto.py. All writes stay in a temporary directory."""
import contextlib
import io
import pathlib
import sys
import tempfile
import struct
import zlib

import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import buildalto
import buildvariants
import gen_farmfresh


class BuildTargets(unittest.TestCase):
    """buildalto writes dist/ and hands the install targets to buildvariants.make."""
    def run_build(self, flags, expected=None, vaults=("test", "real")):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            paths = {"DIST": root / "dist", "PARTS": [],
                     "TEST_VAULT": root / "test" if "test" in vaults else None,
                     "REAL_VAULT": root / "real" if "real" in vaults else None}
            args = [str(root / "custom") if flag == "CUSTOM" else flag for flag in flags]
            seen = []
            with patch.multiple(buildalto, **paths), patch.object(sys, "argv", ["buildalto.py", *args]), \
                 patch.object(buildvariants, "make", lambda css, targets: seen.append(list(targets))), \
                 patch.object(buildalto, "HERE", root), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                if expected is None:
                    with self.assertRaises(SystemExit) as failure:
                        buildalto.main()
                    self.assertEqual(failure.exception.code, 2)
                    self.assertEqual(list(root.iterdir()), [])
                else:
                    buildalto.main()
                    self.assertTrue((root / "dist/theme.css").exists())
                    self.assertEqual(seen, [[root / n for n in expected]])

    def test_bad_arguments_write_nothing(self):
        for flags in (["--dist-onyl"], ["--dist-only", "--test-only"], ["--dist-only", "--to", "CUSTOM"], ["--to"]):
            with self.subTest(flags=flags): self.run_build(flags)

    def test_destinations(self):
        for flags, expected in (([], ["test", "real"]), (["--dist-only"], []), (["--test-only"], ["test"]), (["--to", "CUSTOM"], ["custom"])):
            with self.subTest(flags=flags): self.run_build(flags, expected)

    def test_no_local_vaults(self):
        """A fresh clone has no vaults.local.json: a plain build installs nowhere, --test-only refuses."""
        self.run_build([], [], vaults=())
        self.run_build(["--test-only"], None, vaults=())

    def test_theme_name(self):
        self.assertEqual(buildalto.THEME, "Plectics Alto")
        self.assertEqual(buildalto.MANIFEST["name"], "Plectics Alto")


class SourceChecks(unittest.TestCase):
    """The real sources: braces balance, no control characters."""
    def test_sources_balance(self):
        for part in buildalto.PARTS:
            for f in sorted(part.glob("*.css")):
                text = f.read_text(encoding="utf-8")
                with self.subTest(file=f.name):
                    self.assertEqual(buildalto.balance(text), 0)
                    self.assertFalse(any(ord(ch) < 32 and ch not in "\t\n\r" for ch in text))

    def test_png_text_removal_preserves_rendering_chunks(self):
        def chunk(kind, content):
            return struct.pack(">I", len(content)) + kind + content + struct.pack(">I", zlib.crc32(kind + content))
        for path in (buildalto.HERE / "icons" / "farm-fresh").rglob("*.png"):
            original = path.read_bytes()
            with self.subTest(icon=path.name):
                clean = gen_farmfresh.without_text(original)
                text = b"".join(chunk(kind, b"editor\0metadata") for kind in (b"tEXt", b"iTXt", b"zTXt"))
                self.assertEqual(gen_farmfresh.without_text(clean[:8] + text + clean[8:]), clean)
                self.assertEqual(gen_farmfresh.without_text(clean), clean)
                # Every non-text chunk, including its CRC, stays identical and ordered.
                offset = 8
                kept = [original[:8]]
                while offset < len(original):
                    size, kind = struct.unpack(">I4s", original[offset:offset + 8])
                    raw = original[offset:offset + size + 12]
                    if kind not in (b"tEXt", b"iTXt", b"zTXt"):
                        kept.append(raw)
                    offset += size + 12
                self.assertEqual(clean, b"".join(kept))
        for invalid in (b"not png", b"\x89PNG\r\n\x1a\n\0", b"\x89PNG\r\n\x1a\n\0\0\0\x20IDAT"):
            with self.assertRaises(ValueError):
                gen_farmfresh.without_text(invalid)


class Variants(unittest.TestCase):
    """The two shipped themes, made from the real sources."""
    @classmethod
    def setUpClass(cls):
        parts = [f"/* ---- {d.name}/{f.name} ---- */\n{f.read_text(encoding='utf-8')}\n"
                 for d in buildalto.PARTS for f in sorted(d.glob("*.css"))]
        cls.src = "\n".join(parts)
        cls.plain, cls.icons = buildvariants.plain(cls.src), buildvariants.icons(cls.src)

    def test_plain_has_no_icons(self):
        self.assertNotIn("63-farmfresh.css", self.plain)
        for row in buildvariants.ICON_ROWS:
            self.assertNotIn(f"\n    id: {row}\n", self.plain)

    def test_icons_are_on_by_default(self):
        self.assertNotRegex(self.icons, r"body\.plx-ff(?![-\w])")
        self.assertNotIn("plx-ff-off)-", self.icons)
        self.assertIn("\n    id: plx-ff-off\n", self.icons)
        self.assertNotIn("\n    id: plx-ff\n", self.icons)

    def test_braces(self):
        self.assertEqual(buildalto.balance(self.plain), 0)
        self.assertEqual(buildalto.balance(self.icons), 0)


if __name__ == "__main__":
    unittest.main()
