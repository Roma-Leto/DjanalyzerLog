"""
Модуль тестирования функция парсинга (django_parser.py)
"""

from parsers.django_parser import parse_django_log_file, DjangoLogEntry


def test_parse_successful_request():
    line = ("2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK "
            "[192.168.1.59]")
    result = parse_django_log_file(line)

    assert result == DjangoLogEntry(
        timestamp="2025-03-28 12:44:46,000",
        level="INFO",
        logger="django.request",
        handler="/api/v1/reviews/",
        message="GET /api/v1/reviews/ 204 OK [192.168.1.59]"
    )


def test_parse_error_request():
    line = ("2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: "
            "/admin/dashboard/ [192.168.1.29]")
    result = parse_django_log_file(line)

    assert result == DjangoLogEntry(
        timestamp="2025-03-28 12:11:57,000",
        level="ERROR",
        logger="django.request",
        handler="/admin/dashboard/",
        message="Internal Server Error: /admin/dashboard/ [192.168.1.29]"
    )


def test_parse_non_request_log():
    line = ("2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: "
            "Deadlock detected")
    result = parse_django_log_file(line)

    assert result == DjangoLogEntry(
        timestamp="2025-03-28 12:40:47,000",
        level="CRITICAL",
        logger="django.core.management",
        handler="",
        message="DatabaseError: Deadlock detected"
    )


def test_parse_invalid_line():
    line = "invalid log line"
    assert parse_django_log_file(line) is None
