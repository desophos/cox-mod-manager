import json
from pathlib import Path
from typing import Dict

import pytest
from cox_mod_manager.json import ModEncoder, decode_mod, encode_paths
from cox_mod_manager.mod import Mod


@pytest.fixture(scope="module")
def decoded() -> Dict[str, Dict[str, Mod]]:
    return {
        "mods": {"a": Mod("a.zip", [Path("a"), Path("b/c")], Path("."), {"name": "a"})}
    }


@pytest.fixture(scope="module")
def encoded() -> str:
    return json.dumps(
        {
            "mods": {
                "a": {
                    "filename": "a.zip",
                    "files": ["a", str(Path("b/c"))],
                    "install_dir": ".",
                    "info": {"name": "a"},
                }
            }
        }
    )


@pytest.fixture(scope="module")
def root(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("json")


@pytest.mark.parametrize(
    "testinput,expected",
    [
        (Path("a"), "a"),
        ([Path("a"), Path("b")], ["a", "b"]),
        ([1, Path("b")], [1, "b"]),
        ({"a": Path("b"), "c": 1}, {"a": "b", "c": 1}),
        (
            {"a": [Path("1"), Path("2")], "b": 3, "c": Path("d")},
            {"a": ["1", "2"], "b": 3, "c": "d"},
        ),
    ],
)
def test_encode_paths(testinput, expected):
    assert encode_paths(testinput) == expected


def test_encode(root, decoded, encoded):
    assert encoded == json.dumps(decoded, cls=ModEncoder)


def test_decode(root, decoded, encoded):
    data = json.loads(encoded, object_hook=decode_mod)
    for k, v in decoded["mods"].items():
        assert data["mods"][k] == v  # Mod.__eq__
