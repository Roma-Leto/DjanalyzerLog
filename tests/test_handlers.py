"""
Тесты отчета handlers
"""
from reports.handlers import HandlersReport


def test_process_file(sample_log_file):
    report = HandlersReport()
    result = report.process_file(sample_log_file)

    assert result == {
        "/api/v1/reviews/": {"INFO": 1},
        "/admin/dashboard/": {"INFO": 1},
        "/api/v1/orders/": {"ERROR": 1},
    }


def test_merge_results():
    report = HandlersReport()
    results = [
        {"/handler1": {"INFO": 2, "ERROR": 1}},
        {"/handler1": {"INFO": 1}, "/handler2": {"DEBUG": 1}},
    ]

    merged = report.merge_result(results)

    assert merged == {
        "/handler1": {"INFO": 3, "ERROR": 1},
        "/handler2": {"DEBUG": 1},
    }


def test_format_results():
    report = HandlersReport()
    data = {
        "/handler2": {"DEBUG": 1, "INFO": 2},
        "/handler1": {"INFO": 3, "ERROR": 1},
    }

    formatted = report.format_result(data)
    lines = formatted.split('\n')

    assert "Total requests: 7" in lines[0]
    assert "HANDLER" in lines[2]
    assert "/handler1" in lines[3]
    assert "/handler2" in lines[4]
    assert "3" in lines[3]  # INFO для handler1
    assert "1" in lines[3]  # ERROR для handler1
    assert "2" in lines[4]  # INFO для handler2
