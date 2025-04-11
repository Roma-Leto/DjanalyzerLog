"""
Реализация отчётов для анализа логов Django.
Отчёт группирует записи логов, по обработчику и уровню логирования.

Формат отчёта:
- Количество логов каждого уровня (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Для каждого обработчика
- С итоговым количеством по каждому уровню и общим числом запросов

"""
from pathlib import Path
from typing import Dict, Any, List, DefaultDict
from collections import defaultdict

from .base import BaseReport
from parsers.django_parser import parse_django_log_file


class HandlersReport(BaseReport):
    """
    Отчёт по логам логгера "django.request",
    сгруппированный по обработчику и уровню логирования.
    """

    @property
    def name(self) -> str:
        """Имя отчёта, используемое в CLI"""
        return super().name

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Обрабатывает один лог-файл и возвращает промежуточные результаты:
        словарь вида {handler: {level: count}}.

        :param file_path: Путь к лог-файлу
        :return: Словарь количества логов по обработчикам и уровням
        """
        counts: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_django_log_file(line)
                if parsed and parsed.logger == "django.request":
                    counts[parsed.handler][parsed.level] += 1

        return {handler: dict(levels) for handler, levels in counts.items()}

    def merge_result(self, result: List[Dict[str, Dict[str, int]]]) -> Dict[
        str, Dict[str, int]]:
        """
        Объединяет промежуточные результаты из нескольких файлов.

        :param result: Список промежуточных результатов
        :return: Объединённый результат
        """
        merged: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        for res in result:
            for handler, levels in res.items():
                for level, count in levels.items():
                    merged[handler][level] += count

        return {handler: dict(levels) for handler, levels in merged.items()}

    def format_result(self, merge_data: Dict[str,  Dict[str, int]]) -> str:
        """
        Форматирует объединённые данные в текстовый отчёт.

        :param merge_data: Словарь объединённых данных
        :return: Отформатированный строковый отчёт
        """

        sorted_handlers = sorted(merge_data.items())
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        rows = []
        total_counts = {level: 0 for level in levels}

        for handler, level_counts in sorted_handlers:
            row = [handler.ljust(25)]
            for level in levels:
                count = level_counts.get(level, 0)
                row.append(str(count).ljust(8))
                total_counts[level] += count
            rows.append("\t".join(row))

        total_row = [" " * 25] + [
            str(total_counts[level]).ljust(8) for level in levels
        ]
        total_requests = sum(total_counts.values())

        header = ["HANDLER".ljust(25)] + [level.ljust(8) for level in levels]

        return (
                f"Total requests: {total_requests}\n\n"
                + "\t".join(header) + "\n"
                + "\n".join(rows) + "\n"
                + "\t".join(total_row)
        )
