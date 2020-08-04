import json
import shutil
from pathlib import Path
from typing import Dict, Iterator
from zipfile import ZipFile

import pytest
from cox_mod_manager.context import ModsContext, context
from cox_mod_manager.mod import Mod


@pytest.fixture(scope="session")
def mods_dir(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("mods")


@pytest.fixture(scope="session")
def install_dir(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("install")


@pytest.fixture(scope="session")
def testmods(mods_dir, install_dir) -> Dict[str, Mod]:
    mods = {
        "Test Mod 1": Mod(
            "testmod.zip",
            [Path("data/test/test.txt"), Path("data/test/test2.txt")],
            install_dir,
            {"name": "Test Mod 1"},
        ),
        "Test Mod 2": Mod(
            "testmod2.zip",
            [Path("data/test/test2/test2.txt"), Path("data/test/test3/test3.txt")],
            install_dir,
            {"name": "Test Mod 2"},
        ),
    }

    for mod in mods.values():
        with ZipFile(mods_dir / mod.filename, "w") as zf:
            for f in mod.files:
                # f.parent.mkdir(parents=True)
                zf.writestr(str(f), "")
            zf.writestr("info.json", json.dumps(mod.info))

    return mods


@pytest.fixture(scope="session")
def ctx(testmods, tmp_path_factory, mods_dir, install_dir) -> ModsContext:
    with context(
        root=tmp_path_factory.getbasetemp(), mods_dir=mods_dir, install_dir=install_dir
    ) as ctx:
        return ctx
