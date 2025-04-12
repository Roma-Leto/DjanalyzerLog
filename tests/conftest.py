"""
Модуль создания временных лог-файлов, которые используются в тестах.

Предоставляет фикстуры:
- `sample_log_file`: содержит несколько строк логов разных уровней.
- `sample_error_log_file`: содержит одну строку с ошибкой.
"""
import pytest

from pathlib import Path
from tempfile import NamedTemporaryFile


@pytest.fixture
def sample_log_file():
    """
    Создаёт временный лог-файл со строками разных уровней логирования:
    INFO и ERROR. Используется для тестирования логических обработчиков.

    :return:
        Path: путь к временно созданному файлу.
    """

    content = """
    2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]
    2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]
    2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected
    2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products' WHERE id = 4;
    2025-03-28 12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;
    2025-03-28 12:03:33,000 ERROR django.request: Internal Server Error: /api/v1/orders/ [192.168.1.22] - OSError: No space left on device
    """

    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        f.flush()
        yield Path(f.name)
    Path(f.name).unlink()


@pytest.fixture
def sample_error_log_file():
    """
    Создаёт временный лог-файл, содержащий одну строку ошибки уровня ERROR.

    :return:
        Path: путь к временно созданному файлу.
    """

    content = """
    2025-03-28 12:03:33,000 ERROR django.request: Internal Server Error: /api/v1/orders/ [192.168.1.22] - OSError: No space left on device
    """

    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        f.flush()
        yield Path(f.name)
    Path(f.name).unlink()


