"""
Тесты реестра отчетов
"""
from reports.registry import (
    get_report_names,
    get_report_by_name,
    register_report
)
from reports.base import BaseReport


class SampleReport(BaseReport):
    @property
    def name(self):
        return "test_report"

    def process_file(self, file_path):
        return {}

    def merge_result(self, results):
        return {}

    def format_result(self, merged_data):
        return ""


def test_report_registry():
    # Сохраняем начальное состояние
    initial_reports = get_report_names()

    # Регистрируем новый отчет
    register_report(SampleReport)

    # Проверяем, что отчет добавился
    assert "test_report" in get_report_names()
    assert isinstance(get_report_by_name("test_report"), SampleReport)

    # Проверяем, что старые отчеты остались
    for report in initial_reports:
        assert report in get_report_names()
