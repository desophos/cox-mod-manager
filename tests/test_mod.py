from cox_mod_manager.mod import Mod


def test_install(ctx):
    for mod in ctx.mods.values():
        mod.install()
        for f in mod.files:
            assert mod.install_path(f).exists()


def test_uninstall(ctx):
    name = "Test Mod 1"  # arbitrary pick
    ctx.mods[name].uninstall()
    for path in ctx.mods[name].files:
        assert not path.exists()
    for modname, mod in ctx.mods.items():
        # all other mods should still be installed
        if modname != name:
            for f in mod.files:
                assert mod.install_path(f).exists()
