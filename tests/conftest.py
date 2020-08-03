import shutil
from pathlib import Path

import pytest
from cox_mod_manager.context import context


@pytest.fixture(scope="session")
def ctx(tmp_path_factory):
    # TODO: create test mods programmatically
    mods_dir = tmp_path_factory.mktemp("mods")
    install_dir = tmp_path_factory.mktemp("install")
    shutil.copy(Path("tests/mods/testmod.zip"), mods_dir)
    shutil.copy(Path("tests/mods/testmod2.zip"), mods_dir)
    with context(
        root=tmp_path_factory.getbasetemp(), mods_dir=mods_dir, install_dir=install_dir
    ) as ctx:
        yield ctx
    # TODO: delete temp files
