from pathlib import Path
from typing import Iterable
from zipfile import ZipFile

from cox_mod_manager.utility import remove_empty_dirs


class Mod:
    mods_dir = Path("./tmp/mods")
    install_dir = Path("./tmp/install")

    def __init__(self, filename: str, files: Iterable[Path], **info) -> None:
        self.filename = filename
        self.files = files
        self.name = info["name"]
        self.author = info.get("author")
        self.version = info.get("version")

    def install_path(self, path: Path = Path()) -> Path:
        return self.install_dir / self.name / path

    def install(self) -> None:
        # TODO: remove intermediate files on install failure
        # TODO: warn when overwriting/updating; check version
        with ZipFile(self.filename) as zf:
            zf.extractall(
                path=self.install_path(),
                members=filter(lambda f: f.startswith("data/"), zf.namelist()),
            )

    def uninstall(self) -> None:
        # TODO: warn on incomplete uninstall
        for f in self.files:
            self.install_path(f).unlink()
        remove_empty_dirs(self.install_path())
