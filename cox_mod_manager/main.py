import json
from pathlib import Path
from typing import Dict, Iterable, Set
from zipfile import ZipFile

from cox_mod_manager.mod import Mod

mods: Dict[str, Mod] = {}  # {name: Mod}
installed: Set[str] = set()


def discover() -> Dict[str, Mod]:
    # inspect zipfile for mod name and structure
    # TODO: handle zipfiles with improper structure
    mods: Set[Mod] = set()
    for zmod in filter(lambda f: f.suffix == ".zip", Mod.mods_dir.iterdir()):
        with ZipFile(zmod) as zf:
            with zf.open("info.json") as info:
                assert zf.filename is not None
                mods.add(
                    Mod(
                        zf.filename,
                        [
                            Path(f.filename)
                            for f in zf.infolist()
                            if not f.is_dir() and not f.filename == "info.json"
                        ],
                        **json.load(info)
                    )
                )

    return {mod.name: mod for mod in mods}


def install(mods: Dict[str, Mod], names: Iterable[str]) -> None:
    for name in names:
        mods[name].install()
        installed.add(name)


def uninstall(mods: Dict[str, Mod], names: Iterable[str]) -> None:
    for name in names:
        if name in installed:
            mods[name].uninstall()
            installed.remove(name)
