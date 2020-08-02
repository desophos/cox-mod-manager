from cox_mod_manager.mod import Mod


def test_install(mods):
    for mod in mods.values():
        mod.install()
        for path in mod.files:
            assert (Mod.install_dir / mod.name / path).exists()


def test_uninstall(mods):
    name = "Test Mod 1"  # arbitrary pick
    mods[name].uninstall()
    for path in mods[name].files:
        assert not path.exists()
    for modname, mod in mods.items():
        # all other mods should still be installed
        if modname != name:
            for f in mod.files:
                assert mod.install_path(f).exists()
