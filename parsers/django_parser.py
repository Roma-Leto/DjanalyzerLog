"""
Модуль для парсинга строк логов Django.

Позволяет извлекать основные поля из строки лога (время, уровень, логгер, сообщение)
"""
import re

from dataclasses import dataclass
from typing import Pattern, Optional


@dataclass
class DjangoLogEntry:
    """
    Представляет собой структуру лог-записи Django.

    Атрибуты:
        timestamp (str): Временная метка события.
        level (str): Уровень логирования (INFO, ERROR и т.д.).
        logger (str): Название логгера (например, 'django.request').
        handler (str): Обработчик запроса (если применимо).
        message (str): Полный текст сообщения лога.
    """
    timestamp: str
    level: str
    logger: str
    handler: str
    message: str


LOG_PATTERN: Pattern = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+"
    r"(?P<level>\w+)\s+"
    r"(?P<logger>[a-z._]+):\s+"
    r"(?P<message>.+)$"
)

REQUEST_PATTERN: Pattern = re.compile(
    r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(?P<handler>/[^\s]+)"
)

ERROR_REQUEST_PATTERN: Pattern = re.compile(
    r"Internal Server Error:\s+(?P<handler>/[^\s]+)"
)


def parse_django_log_file(line: str) -> Optional[DjangoLogEntry]:
    """
    Парсит строку лога Django и возвращает объект DjangoLogEntry.

    Пытается распарсить строку с помощью LOG_PATTERN.
    Если логгер — 'django.request', дополнительно пытается извлечь путь запроса (handler).

    Args:
        line (str): Строка из лог-файла Django.

    Returns:
        Optional[DjangoLogEntry]: Объект DjangoLogEntry или None
    """

    # Удаляем пробелы по краям и сопоставляем с шаблоном LOG_PATTERN
    match = LOG_PATTERN.match(line.strip())

    if not match:  # Если строка не соответствует формату
        return None

    data = match.groupdict()

    # Для запросов извлекаем обработчик
    handler = ""

    if data["logger"] == "django.request" and data["level"] != "ERROR":
        request_match = REQUEST_PATTERN.search(data["message"])
        if request_match:
            handler = request_match.group("handler")

    elif data["logger"] == "django.request" and data["level"] == "ERROR":
        error_match = ERROR_REQUEST_PATTERN.search(data["message"])
        if error_match:
            handler = error_match.group("handler")

    return DjangoLogEntry(
        timestamp=data["timestamp"],
        level=data["level"],
        logger=data["logger"],
        handler=handler,
        message=data["message"]
    )
