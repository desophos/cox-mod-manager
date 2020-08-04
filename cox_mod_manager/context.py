import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Set
from zipfile import ZipFile

from cox_mod_manager.json import ModEncoder, decode_mod
from cox_mod_manager.mod import Mod


class ModsContext:
    def __init__(
        self, root=".", mods_dir="tmp/mods", install_dir="tmp/install"
    ) -> None:
        self.root = Path(root)
        self.mods_dir = self.root / mods_dir
        self.install_dir = self.root / install_dir
        self.mods: Dict[str, Mod] = {}  # {name: Mod}
        self.installed: Set[str] = set()

        for path in [self.mods_dir, self.install_dir]:
            if not path.exists():
                path.mkdir(parents=True)

    def __enter__(self):
        try:
            with open(self.root / "mods.json") as f:
                data = json.load(f, object_hook=decode_mod)
                self.mods = data["mods"]
                self.installed = set(data["installed"])
        except FileNotFoundError:
            self.mods = self.discover()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with open(self.root / "mods.json", "w") as f:
            json.dump(
                {"mods": self.mods, "installed": list(self.installed)},
                f,
                cls=ModEncoder,
            )

    def discover(self) -> Dict[str, Mod]:
        # inspect zipfile for mod name and structure
        # TODO: handle zipfiles with improper structure
        mods: List[Mod] = []
        for zmod in filter(lambda f: f.suffix == ".zip", self.mods_dir.iterdir()):
            with ZipFile(zmod) as zf:
                with zf.open("info.json") as info:
                    assert zf.filename is not None
                    mods.append(
                        Mod(
                            zf.filename,
                            [
                                Path(f.filename)
                                for f in zf.infolist()
                                if not f.is_dir() and not f.filename == "info.json"
                            ],
                            self.install_dir,
                            json.load(info),
                        )
                    )

        return {mod.name: mod for mod in mods}


@lru_cache
def context(*args, **kwargs) -> ModsContext:
    return ModsContext(*args, **kwargs)
