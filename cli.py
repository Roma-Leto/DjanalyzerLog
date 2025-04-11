"""
Логика обработки аргументов командной строки
"""

import argparse
from pathlib import Path
from typing import List, Optional


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
    args = parse_args()
    print(args)
