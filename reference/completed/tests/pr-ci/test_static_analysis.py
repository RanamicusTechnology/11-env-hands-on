# Copyright 2026 Ranamicus Technology LLC. All rights reserved.

import importlib.util
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts" / "pr-ci"
sys.path.insert(0, str(SCRIPT_DIR))
MODULE_PATH = SCRIPT_DIR / "static_analysis.py"
SPEC = importlib.util.spec_from_file_location("static_analysis", MODULE_PATH)
static_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(static_analysis)


def test_classify_gofmt_success_when_no_output():
    result, reasons = static_analysis.classify_gofmt(0, "")

    assert result == "success"
    assert reasons == []


def test_classify_gofmt_failure_when_files_are_listed():
    result, reasons = static_analysis.classify_gofmt(0, "main.go\n")

    assert result == "failure"
    assert "main.go" in reasons[0]
