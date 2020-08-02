from pathlib import Path


def remove_empty_dirs(path: Path) -> None:
    if path.is_dir():
        if path.iterdir():
            # it contains dirs/files, so remove empty children
            for child in path.iterdir():
                remove_empty_dirs(child)
        try:
            path.rmdir()  # it's as empty as it's gonna get
        except OSError:
            pass  # it's not empty after all, so leave it alone
