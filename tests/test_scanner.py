from app.scanner import available_checks, run_scan


def test_all_checks_are_registered():
    assert len(available_checks()) == 5


def test_scan_can_run_a_selected_check(tmp_path, monkeypatch):
    from app import reporting

    monkeypatch.setattr(reporting, "REPORTS_DIR", tmp_path)
    result = run_scan("test-target", ["robustness"])
    assert result["status"] == "PASS"
    assert result["totals"] == {"checks": 1, "passed": 1, "failed": 0}
