"""Copy a fresh build into local clones of the two GitHub repositories (no commit, no push).

    python -I export_repos.py <clone of obsidian.themes.plectics-alto> <clone of obsidian.themes.plectics-alto-icons>

Plectics Alto: every file of this folder that .gitignore does not exclude
(git decides, via --work-tree). Plectics Alto Icons: the built theme, its
README, LICENSE, NOTICE.md and the licence texts of the embedded fonts.
Run `python -I buildalto.py --dist-only` first.
"""
import pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
alto, icons = (pathlib.Path(a).resolve() for a in sys.argv[1:3])


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


# 1. Plectics Alto: stage this folder into the clone's index, then write those files into the clone
git(alto, f"--work-tree={HERE}", "add", "-A")
git(alto, "checkout", "--", ".")
print("plectics-alto:", len(git(alto, "ls-files").split()), "files staged")
print(git(alto, "status", "--short", "--untracked-files=no")[:2000])

# 2. Plectics Alto Icons: release files plus licence texts
src = HERE / "themes" / "Plectics Alto Icons"
for f in ("theme.css", "manifest.json", "README.md"):
    shutil.copy(src / f, icons / f)
for f in ("LICENSE", "NOTICE.md", ".gitattributes"):
    shutil.copy(HERE / f, icons / f)
lic = icons / "licences"
lic.mkdir(exist_ok=True)
shutil.copy(HERE / "fonts" / "OFL-EBGaramond.txt", lic / "OFL-EBGaramond.txt")
shutil.copy(HERE / "fonts" / "archivo" / "OFL-Archivo.txt", lic / "OFL-Archivo.txt")
shutil.copy(HERE / "fonts" / "nimbus" / "COPYING", lic / "NimbusSans-COPYING.txt")
shutil.copy(HERE / "fonts" / "nimbus" / "LICENSE", lic / "NimbusSans-LICENSE.txt")
git(icons, "add", "-A")
print("plectics-alto-icons:")
print(git(icons, "status", "--short"))
