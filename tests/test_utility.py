from cox_mod_manager.utility import remove_empty_dirs


def test_remove_empty_dirs(tmp_path):
    root = tmp_path / "test_remove_empty_dirs"

    (root / "empty" / "empty2").mkdir(parents=True)
    (root / "empty" / "empty3").mkdir(parents=True)
    (root / "notempty" / "notempty2").mkdir(parents=True)
    (root / "notempty" / "notempty2" / "file.txt").touch()
    (root / "notempty" / "empty" / "empty2").mkdir(parents=True)

    remove_empty_dirs(root / "empty")
    assert not (root / "empty").exists()
    remove_empty_dirs(root / "notempty")
    assert (root / "notempty").exists()
    assert not (root / "notempty" / "empty").exists()
