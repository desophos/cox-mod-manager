from json import JSONDecoder, JSONEncoder
from pathlib import Path

from cox_mod_manager.mod import Mod


def encode_paths(it):
    if isinstance(it, str):  # str is iterable, so it would recurse infinitely
        return it
    try:
        return {k: encode_paths(v) for k, v in it.items()}
    except AttributeError:  # not a dict
        try:
            return list(map(encode_paths, it))
        except TypeError:  # not iterable
            if isinstance(it, Path):
                return str(it)
            else:
                return it


class ModEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Mod):
            return encode_paths(vars(o))
        return JSONEncoder.default(self, o)


class ModDecoder(JSONDecoder):
    def object_hook(self, o):
        if all(key in o for key in ["filename", "files", "install_dir", "name"]):
            info = {k: v for k, v in o.items() if k in ("name", "author", "version")}
            return Mod(
                o["filename"], map(Path, o["files"]), Path(o["install_dir"]), info
            )
        else:
            return JSONDecoder.decode(self, o)
