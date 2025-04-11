"""
Логика обработки аргументов командной строки
"""

import argparse
from pathlib import Path
from typing import List, Optional

from reports.registry import get_report_by_name
from utils.utilities import LogFileNotFoundError, validate_files


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Функция разбора аргументов командной строки.
    :param args: Список строк
    :return: Namespace(log_files=[WindowsPath(''), WindowsPath('')], report='')
    """
    parser = argparse.ArgumentParser(description="Django logs analyzer")

    parser.add_argument(
        "log_files",
        nargs="+",
        type=Path,
        help="Paths to log files"
    )

    parser.add_argument(
        "--report",
        required=True,
        choices=None,
        help="Report type to generate"
    )

    return parser.parse_args(args)


def run_cli():
    """
    Входная функция приложения
    """
    try:
        args = parse_args()
        validate_files(args.log_files)
        report = get_report_by_name(args.report)
        result = report.generate(args.log_files)
        print(result)
    except LogFileNotFoundError as e:
        print(f"[ERROR] {e}")
