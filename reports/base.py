"""
Содержит абстрактный класс BaseReport, определяющий интерфейс для генерации отчётов на
основе логов.

Класс включает в себя:
- process_file(): обработка одного файла
- merge_result(): объединение результатов
- format_result(): форматирование данных
- generate(): полный pipeline
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any


class BaseReport(ABC):
    """
    Абстрактный базовый класс для всех типов отчётов
    """

    def __init__(self, name: str = None):
        self._custom_name = name

    @property
    @abstractmethod
    def name(self):
        """
        Уникальное имя отчёта используемое в CLI.
        Возвращает имя класса по умолчанию или кастомное имя, если оно задано.
        """
        if self._custom_name:
            return self._custom_name
        return self.__class__.__name__.lower()

    @abstractmethod
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Обработка лога и возврат промежуточных данных"""
        pass

    @abstractmethod
    def merge_result(self, result: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Объединение результатов из нескольких файлов в один лог"""
        pass

    @abstractmethod
    def format_result(self, merge_data: Dict[str, Any]) -> str:
        """Функция форматирования результата для вывода пользователю"""
        pass

    def generate(self, file_path: List[Path]) -> str:
        """Генерация польного отчёта"""
        result = [self.process_file(fp) for fp in file_path]
        merged_data = self.merge_result(result)
        return self.format_result(merged_data)
