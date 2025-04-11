"""
Модуль для регистрации и получения отчётов.

Позволяет регистрировать классы-отчёты (наследники BaseReport) и 
получать их экземпляры по имени.
"""
from typing import Dict, Type, List
from reports.base import BaseReport
from reports.handlers import HandlersReport

# Внутренний реестр отчётов: имя -> класс отчёта
_registry: Dict[str, Type[BaseReport]] = {}


def register_report(report_class: Type[BaseReport], name: str = None):
    """Регистрирует отчёт в реестре."""
    instance = report_class(name=name)
    _registry[instance.name] = report_class


def get_report_by_name(name: str) -> BaseReport:
    """Возвращает экземпляр отчёта по его имени"""
    return _registry[name]()


def get_report_names() -> List[str]:
    """Возвращает список всех зарегистрированных имён отчётов."""
    return list(_registry.keys())


# Регистрируем все отчёты
register_report(HandlersReport, name='handlers')
