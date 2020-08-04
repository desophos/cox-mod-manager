


def test_discover(ctx, testmods):
    assert sorted(ctx.mods.keys()) == sorted(testmods.keys())
    for name, mod in testmods.items():
        for path in mod.files:
            assert path in ctx.mods[name].files


# TODO: enter/exit tests
