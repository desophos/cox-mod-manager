import json

from cox_mod_manager.context import context
from cox_mod_manager.json import ModEncoder, decode_mod


def test_discover(ctx, testmods):
    assert sorted(ctx.mods.keys()) == sorted(testmods.keys())
    for name, mod in testmods.items():
        for path in mod.files:
            assert path in ctx.mods[name].files


def test_enter(tmp_path_factory, testmods):
    root = tmp_path_factory.mktemp("ctx_enter")

    with open(root / "mods.json", "w") as f:
        json.dump({"mods": testmods, "installed": ["Test Mod 2"]}, f, cls=ModEncoder)

    with context(root=root, mods_dir="mods", install_dir="install") as ctx:
        assert ctx.mods == testmods
        assert ctx.installed == set(["Test Mod 2"])


def test_exit(tmp_path_factory, testmods):
    root = tmp_path_factory.mktemp("ctx_exit")
    installed = set(["Test Mod 1"])

    with context(root=root, mods_dir="mods", install_dir="install") as ctx:
        ctx.mods = testmods
        ctx.installed = installed

    with open(root / "mods.json") as f:
        data = json.load(f, object_hook=decode_mod)
        assert data["mods"] == testmods
        assert set(data["installed"]) == installed
