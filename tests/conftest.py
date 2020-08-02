import shutil
from pathlib import Path

import pytest
from cox_mod_manager.main import discover
from cox_mod_manager.mod import Mod


@pytest.fixture(scope="session")
def mods(tmp_path_factory):
    # TODO: create test mods programmatically
    Mod.mods_dir = tmp_path_factory.mktemp("mods")
    Mod.install_dir = tmp_path_factory.mktemp("install")
    shutil.copy(Path("tests/mods/testmod.zip"), Mod.mods_dir)
    shutil.copy(Path("tests/mods/testmod2.zip"), Mod.mods_dir)
    yield discover()
    # TODO: delete temp files
