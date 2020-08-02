from pathlib import Path

testmods = {
    "Test Mod 1": [Path("data/test/test.txt"), Path("data/test/test2.txt")],
    "Test Mod 2": [
        Path("data/test/test2/test2.txt"),
        Path("data/test/test3/test3.txt"),
    ],
}


def test_discover(mods):
    assert sorted(mods.keys()) == sorted(testmods.keys())
    for name, paths in testmods.items():
        mod = mods[name]
        for path in paths:
            assert path in mod.files
