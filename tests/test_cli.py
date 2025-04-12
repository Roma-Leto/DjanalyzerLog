"""
Тесты CLI
"""

import argparse
from unittest.mock import patch, MagicMock
from pathlib import Path

from cli import parse_args, run_cli


def test_parse_args():
    args = parse_args(["file1.log", "file2.log", "--report", "handlers"])
    assert args.log_files == [Path("file1.log"), Path("file2.log")]
    assert args.report == "handlers"


@patch("cli.get_report_by_name")
@patch("cli.validate_files")
def test_run_cli(mock_validate, mock_get_report):
    # Настраиваем моки
    mock_report = MagicMock()
    mock_report.generate.return_value = "test report output"
    mock_get_report.return_value = mock_report

    # Запускаем тестируемую функцию
    with patch("sys.argv", ["main.py", "file1.log", "--report", "handlers"]):
        with patch("builtins.print") as mock_print:
            run_cli()

    # Проверяем вызовы
    mock_validate.assert_called_once()
    mock_get_report.assert_called_once_with("handlers")
    mock_print.assert_called_once_with("test report output")
