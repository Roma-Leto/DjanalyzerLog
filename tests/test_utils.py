"""
Тесты утилит
"""
import pytest

from utils.utilities import validate_files, LogFileNotFoundError


def test_validate_files_existing(tmp_path):
    # Создаем временный файл
    test_file = tmp_path / "test.log"
    test_file.touch()

    # Должно пройти без исключений
    validate_files([test_file])


def test_validate_files_not_existing(tmp_path):
    test_file = tmp_path / "nonexistent.log"

    with pytest.raises(LogFileNotFoundError):
        validate_files([test_file])
