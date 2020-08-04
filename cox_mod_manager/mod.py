from pathlib import Path
from typing import Iterable
from zipfile import ZipFile

from cox_mod_manager.utility import remove_empty_dirs


class Mod:
    def __init__(
        self, filename: str, files: Iterable[Path], install_dir: Path, info
    ) -> None:
        self.filename = filename
        self.files = files
        self.install_dir = install_dir
        if "name" not in info:
            raise KeyError("info must include name")
        self.info = info

    @property
    def name(self):
        return self.info["name"]

    def __eq__(self, other):
        return vars(self) == vars(other)

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
