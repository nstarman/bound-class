##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
import os
import sys
from pathlib import Path

# THIRD PARTY
from setuptools import setup

##############################################################################
# PARAMETERS

CURRENT_DIR = Path(__file__).parent
SRC = CURRENT_DIR / "src"
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta

# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
USE_MYPYC = True
if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    USE_MYPYC = True
if os.getenv("BOUNDCLASS_USE_MYPYC", None) == "1":
    USE_MYPYC = True


##############################################################################
# BUILD

if not USE_MYPYC:
    ext_modules = []

else:
    # THIRD PARTY
    from mypyc.build import mypycify

    def find_python_files(base: Path, exclude: tuple[str, ...] = ("test_",)) -> list[Path]:
        files: list[Path] = []

        for entry in base.iterdir():
            if entry.name.startswith(exclude):
                continue
            if entry.is_file() and entry.suffix == ".py":
                files.append(entry)
            elif entry.is_dir():
                files.extend(find_python_files(entry))

        return files

    blocklist: list[str] = []
    discovered: list[Path] = []
    discovered.extend(find_python_files(SRC / "bound_class"))
    mypyc_targets = [str(p) for p in discovered if p.relative_to(SRC).as_posix() not in blocklist]

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    ext_modules = mypycify(mypyc_targets, opt_level=opt_level, verbose=True)

setup(name="bound_class", packages=["bound_class"], ext_modules=ext_modules)
