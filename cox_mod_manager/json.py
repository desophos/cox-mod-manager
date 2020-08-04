from json import JSONEncoder
from pathlib import Path

from cox_mod_manager.mod import Mod


def encode_paths(it):
    if isinstance(it, Path):
        return str(it)  # do the actual encoding
    if isinstance(it, str):  # str is iterable, so it would recurse infinitely
        return it
    try:  # recurse into dict
        return {k: encode_paths(v) for k, v in it.items()}
    except AttributeError:  # not a dict
        try:  # recurse into iterable
            return list(map(encode_paths, it))
        except TypeError:  # not iterable
            return it


class ModEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Mod):
            return encode_paths(vars(o))
        return JSONEncoder.default(self, o)


def decode_mod(o):
    if all(key in o for key in ["filename", "files", "install_dir", "info"]):
        return Mod(
            o["filename"],
            list(map(Path, o["files"])),
            Path(o["install_dir"]),
            o["info"],
        )
    else:
        return o
