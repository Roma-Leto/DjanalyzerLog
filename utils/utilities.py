"""
Вспомогательные функции приложения
"""
from typing import List
from pathlib import Path


class LogFileNotFoundError(Exception):
    """Исключение для недоступных лог-файлов."""
    pass


def validate_files(file_paths: List[Path]) -> None:
    """
    Проверка файлов на существование
    raise: Если хотя бы один файл не существует
    """
    for file in file_paths:
        if not file.exists():
            raise LogFileNotFoundError(f"Log file not found: {file}")
