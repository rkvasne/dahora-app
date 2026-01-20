import os
from unittest.mock import MagicMock

import dahora_app.clipboard_manager as clipboard_module
from dahora_app.clipboard_manager import ClipboardManager


def test_load_history_legacy_migrates_and_sanitizes(
    monkeypatch, create_test_json_file
):
    raw_items = [
        {"text": " ok ", "timestamp": "t1", "app": "a1"},
        {"text": ""},  # inválido
        {"text": "   "},  # inválido
        {"text": 123},  # inválido
        "not-a-dict",  # inválido
        {"text": "ok2"},
    ]
    history_path = create_test_json_file("clipboard_history.json", raw_items)

    monkeypatch.setattr(clipboard_module, "HISTORY_FILE", history_path)

    manager = ClipboardManager()
    manager.save_history = MagicMock()
    manager.load_history()

    assert manager.clipboard_history == [
        {"text": " ok ", "timestamp": "t1", "app": "a1"},
        {"text": "ok2", "timestamp": "", "app": ""},
    ]
    manager.save_history.assert_called_once()


def test_load_history_uses_backup_when_primary_missing(
    monkeypatch, temp_data_dir
):
    history_path = os.path.join(temp_data_dir, "clipboard_history.json")
    backup_path = history_path + ".bak"

    with open(backup_path, "w", encoding="utf-8") as f:
        f.write('[{"text": "from-backup"}]')

    monkeypatch.setattr(clipboard_module, "HISTORY_FILE", history_path)

    manager = ClipboardManager()
    manager.save_history = MagicMock()
    manager.load_history()

    assert manager.clipboard_history == [
        {"text": "from-backup", "timestamp": "", "app": ""}
    ]
    manager.save_history.assert_called_once()


def test_load_history_empty_when_primary_corrupt_and_no_backup(
    monkeypatch, create_corrupted_json_file
):
    history_path = create_corrupted_json_file("clipboard_history.json")
    monkeypatch.setattr(clipboard_module, "HISTORY_FILE", history_path)

    manager = ClipboardManager()
    manager.load_history()

    assert manager.clipboard_history == []
    assert manager._history_write_disabled is False


def test_load_history_disables_writes_on_decrypt_error(
    monkeypatch, create_test_json_file
):
    raw = {"dpapi": 1, "blob": "invalid"}
    history_path = create_test_json_file("clipboard_history.json", raw)
    monkeypatch.setattr(clipboard_module, "HISTORY_FILE", history_path)

    manager = ClipboardManager()
    def raise_decrypt_failed(_blob: str):
        raise RuntimeError("decrypt failed")

    monkeypatch.setattr(manager, "_decrypt_data", raise_decrypt_failed)

    manager.load_history()

    assert manager.clipboard_history == []
    assert manager._history_write_disabled is True
    assert "decrypt failed" in (manager._history_write_disabled_reason or "")
