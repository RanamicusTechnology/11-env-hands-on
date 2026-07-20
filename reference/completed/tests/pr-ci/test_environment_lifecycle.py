# Copyright 2026 Ranamicus Technology LLC. All rights reserved.

import importlib.util
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts" / "pr-ci"
sys.path.insert(0, str(SCRIPT_DIR))
MODULE_PATH = SCRIPT_DIR / "environment_lifecycle.py"
SPEC = importlib.util.spec_from_file_location("environment_lifecycle", MODULE_PATH)
environment_lifecycle = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = environment_lifecycle
SPEC.loader.exec_module(environment_lifecycle)


def write_build_artifact(build_dir, version="v0.0.0+b.1.a.1"):
    build_dir.mkdir()
    binary = build_dir / "go-app-linux-amd64"
    binary.write_bytes(b"fake-linux-amd64-binary")
    checksum = hashlib.sha256(binary.read_bytes()).hexdigest()
    (build_dir / "go-app-linux-amd64.sha256").write_text(
        f"{checksum}  go-app-linux-amd64\n",
        encoding="utf-8",
    )
    (build_dir / "manifest.json").write_text(
        json.dumps({"build_artifact_version": version}),
        encoding="utf-8",
    )
    return checksum


def test_environment_face_id_uses_issue_run_and_attempt():
    assert environment_lifecycle.environment_face_id("7", "123456", "2") == "UT-7-123456-A2"


def test_pytest_suite_writes_failure_placeholder_when_junit_is_missing(tmp_path):
    output_dir = tmp_path / "evidence"
    state = environment_lifecycle.LifecycleState()
    original_run_command = environment_lifecycle.run_command

    def fake_run_command(args, *, cwd, log_path, append=False, check=False, env=None):
        environment_lifecycle.write_log(log_path, "$ pytest\npytest crashed before junit\n")
        return environment_lifecycle.CommandResult(args, 2, "pytest crashed before junit\n")

    environment_lifecycle.run_command = fake_run_command
    try:
        execution_state, result = environment_lifecycle.run_pytest_suite(
            state=state,
            test_key="infrastructure",
            title="infrastructure-test",
            command=[
                "pytest",
                "--junitxml",
                str(output_dir / "test-results" / "infrastructure-test-junit.xml"),
            ],
            env={},
            root=tmp_path,
            output_dir=output_dir,
        )
    finally:
        environment_lifecycle.run_command = original_run_command

    assert execution_state == "Failed"
    assert result == "Failed"
    assert state.detected_missing_evidence == ["test-results/infrastructure-test-junit.xml"]
    assert state.evidence_missing_reasons == [
        "test-results/infrastructure-test-junit.xml: "
        "JUnit XML was not created at test-results/infrastructure-test-junit.xml"
    ]
    junit_path = output_dir / "test-results" / "infrastructure-test-junit.xml"
    payload = json.loads(
        (output_dir / "test-results" / "infrastructure-test-result.json").read_text(encoding="utf-8")
    )
    assert payload["junit_xml"] == "test-results/infrastructure-test-junit.xml"
    suite = ET.parse(junit_path).getroot()
    assert suite.attrib["failures"] == "1"
    assert suite.find("testcase/failure") is not None

    for relative_path in environment_lifecycle.EXPECTED_EVIDENCE:
        path = output_dir / relative_path
        if not path.exists():
            environment_lifecycle.write_log(path, "synthetic evidence\n")

    args = environment_lifecycle.argparse.Namespace(
        test_run_id="TR-UT-ISSUE-7-100-A1",
        workflow_run_id="100",
        workflow_run_attempt="1",
        job_name="environment-lifecycle",
        pr_number="8",
        issue_number="7",
        pr_head_sha="abc123",
        repository="RanamicusTechnology/11-env-hands-on",
        created_at="2026-07-05T00:00:00Z",
        target_version="0.0.0",
        required_final_stage="UT",
        build_artifact_name="build-go-app_TR-UT-ISSUE-7-100-A1",
        build_artifact_id="5",
        build_artifact_version="v0.0.0+b.1.a.1",
        build_artifact_checksum="abc",
    )
    manifest, result_payload, _summary = environment_lifecycle.finalize_result(
        args,
        state,
        output_dir,
    )
    assert manifest["missing_evidence"] == ["test-results/infrastructure-test-junit.xml"]
    assert manifest["missing_evidence_count"] == 1
    assert manifest["environment_evidence_complete"] is False
    assert result_payload["evidence"]["missing_evidence_count"] == 1
    assert result_payload["evidence"]["environment_evidence_complete"] is False


def test_early_failure_finalizes_environment_evidence_without_docker(tmp_path):
    output_dir = tmp_path / "evidence"
    missing_build_dir = tmp_path / "missing-build-artifact"

    rc = environment_lifecycle.main(
        [
            "--output-dir",
            str(output_dir),
            "--build-artifact-dir",
            str(missing_build_dir),
            "--repository",
            "RanamicusTechnology/11-env-hands-on",
            "--workflow-run-id",
            "100",
            "--workflow-run-attempt",
            "1",
            "--test-run-id",
            "TR-UT-ISSUE-7-100-A1",
            "--issue-number",
            "7",
            "--target-version",
            "0.0.0",
            "--required-final-stage",
            "UT",
            "--pr-number",
            "8",
            "--pr-head-sha",
            "abc123",
            "--governance-job-result",
            "failure",
            "--governance-result",
            "failure",
            "--static-analysis-job-result",
            "skipped",
            "--static-analysis-result",
            "",
            "--unit-test-job-result",
            "skipped",
            "--unit-test-result",
            "",
            "--build-package-job-result",
            "skipped",
            "--build-package-result",
            "",
            "--build-artifact-name",
            "",
            "--build-artifact-id",
            "",
            "--build-artifact-version",
            "",
            "--build-artifact-checksum",
            "",
            "--build-artifact-uploaded",
            "false",
            "--created-at",
            "2026-07-05T00:00:00Z",
        ]
    )

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    result = json.loads(
        (output_dir / "environment-lifecycle-result.json").read_text(encoding="utf-8")
    )
    assert result["environment_lifecycle_result"] == "skipped_prerequisites"
    assert manifest["environment_face_id_or_not_created"] == "NOT_CREATED"
    assert manifest["environment_creation_state"] == "NotStarted"
    assert manifest["test_result"] == "FailedBeforeTest"
    assert manifest["infrastructure_test_execution_state"] == "Skipped"
    assert manifest["infrastructure_test_result"] == "FailedBeforeTest"
    assert manifest["api_test_execution_state"] == "Skipped"
    assert manifest["api_test_result"] == "FailedBeforeTest"
    assert manifest["cleanup_state"] == "Completed"
    assert manifest["cleanup_target_count"] == 0
    assert manifest["remaining_resource_count"] == 0
    assert "NotRequired" not in json.dumps(manifest)
    assert (output_dir / "test-results" / "infrastructure-test-junit.xml").exists()
    assert (output_dir / "test-results" / "api-test-result.json").exists()
    assert result["tests"]["infrastructure"]["result"] == "FailedBeforeTest"
    assert result["tests"]["api"]["result"] == "FailedBeforeTest"


def test_residue_verification_preserves_cleanup_not_attempted(tmp_path):
    state = environment_lifecycle.LifecycleState(
        prerequisites_met=True,
        cleanup_state="NotAttempted",
    )
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()

    environment_lifecycle.verify_residue(
        state,
        root=tmp_path,
        logs_dir=logs_dir,
        label_filter="label=test_run_id=TR-UT-ISSUE-7-100-A1",
    )

    assert state.cleanup_state == "NotAttempted"
    assert state.residue_verification_result == "NotAttempted"


def test_terraform_fmt_failure_before_apply_records_completed_cleanup(tmp_path):
    output_dir = tmp_path / "evidence"
    build_dir = tmp_path / "build-artifact"
    version = "v0.0.0+b.1.a.1"
    checksum = write_build_artifact(build_dir, version)
    original_run_command = environment_lifecycle.run_command

    def fake_run_command(args, *, cwd, log_path, append=False, check=False, env=None):
        command = " ".join(args)
        if args[:2] == ["docker", "build"]:
            result = environment_lifecycle.CommandResult(args, 0, "image built\n")
        elif args == ["terraform", "fmt", "-check"]:
            result = environment_lifecycle.CommandResult(args, 1, "main.tf\n")
        elif args[0] == "docker":
            result = environment_lifecycle.CommandResult(args, 0, "")
        else:
            result = environment_lifecycle.CommandResult(args, 0, "")

        message = f"$ {command}\n{result.stdout}"
        if append:
            environment_lifecycle.append_log(log_path, message)
        else:
            environment_lifecycle.write_log(log_path, message)
        return result

    environment_lifecycle.run_command = fake_run_command
    try:
        rc = environment_lifecycle.main(
            [
                "--output-dir",
                str(output_dir),
                "--build-artifact-dir",
                str(build_dir),
                "--repository",
                "RanamicusTechnology/11-env-hands-on",
                "--workflow-run-id",
                "28729279045",
                "--workflow-run-attempt",
                "1",
                "--test-run-id",
                "TR-UT-ISSUE-7-28729279045-A1",
                "--issue-number",
                "7",
                "--target-version",
                "0.0.0",
                "--required-final-stage",
                "UT",
                "--pr-number",
                "8",
                "--pr-head-sha",
                "6780c750712f373187be0654642548eb6e93f841",
                "--governance-job-result",
                "success",
                "--governance-result",
                "success",
                "--static-analysis-job-result",
                "success",
                "--static-analysis-result",
                "success",
                "--unit-test-job-result",
                "success",
                "--unit-test-result",
                "success",
                "--build-package-job-result",
                "success",
                "--build-package-result",
                "success",
                "--build-artifact-name",
                "build-go-app_TR-UT-ISSUE-7-28729279045-A1",
                "--build-artifact-id",
                "8088230457",
                "--build-artifact-version",
                version,
                "--build-artifact-checksum",
                checksum,
                "--build-artifact-uploaded",
                "true",
                "--created-at",
                "2026-07-05T00:00:00Z",
            ]
        )
    finally:
        environment_lifecycle.run_command = original_run_command

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    result = json.loads(
        (output_dir / "environment-lifecycle-result.json").read_text(encoding="utf-8")
    )
    assert result["environment_lifecycle_result"] == "failure"
    assert result["failure_reasons"] == ["terraform fmt -check failed"]
    assert result["cleanup"]["environment_resources_may_exist"] is False
    assert result["cleanup"]["cleanup_attempted"] is True
    assert manifest["environment_creation_state"] == "Failed"
    assert manifest["infrastructure_test_execution_state"] == "Skipped"
    assert manifest["infrastructure_test_result"] == "FailedBeforeTest"
    assert manifest["api_test_execution_state"] == "Skipped"
    assert manifest["api_test_result"] == "FailedBeforeTest"
    assert manifest["cleanup_state"] == "Completed"
    assert manifest["cleanup_target_count"] == 0
    assert manifest["remaining_resource_count"] == 0
    assert manifest["residue_verification_result"] == "Passed"
    assert manifest["cleanup_warning"] is False
    assert result["tests"]["infrastructure"]["result"] == "FailedBeforeTest"
    assert result["tests"]["api"]["result"] == "FailedBeforeTest"


def test_successful_lifecycle_records_formal_test_results(tmp_path):
    output_dir = tmp_path / "evidence"
    build_dir = tmp_path / "build-artifact"
    github_output = tmp_path / "github-output.txt"
    version = "v0.0.0+b.1.a.1"
    checksum = write_build_artifact(build_dir, version)
    original_run_command = environment_lifecycle.run_command
    original_urlopen = environment_lifecycle.urlopen

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self):
            return json.dumps({"status": "ok", "version": version}).encode("utf-8")

    def fake_urlopen(url, timeout):
        return FakeResponse()

    def fake_run_command(args, *, cwd, log_path, append=False, check=False, env=None):
        command = " ".join(args)
        if args[:2] == ["docker", "build"]:
            result = environment_lifecycle.CommandResult(args, 0, "image built\n")
        elif args[:2] == ["terraform", "output"]:
            output_name = args[-1]
            outputs = {
                "ansible_inventory": "all:\n  hosts:\n    ms1_target:\n",
                "container_name": "ut-7-target",
                "network_name": "ut-7-net",
                "host_http_url": "http://127.0.0.1:18080",
            }
            result = environment_lifecycle.CommandResult(args, 0, outputs[output_name])
        elif len(args) >= 3 and args[0] == environment_lifecycle.sys.executable and args[1:3] == ["-m", "pytest"]:
            junit_path = Path(args[args.index("--junitxml") + 1])
            junit_path.parent.mkdir(parents=True, exist_ok=True)
            junit_path.write_text(
                "<?xml version='1.0' encoding='utf-8'?><testsuite tests='1' failures='0' errors='0' skipped='0'><testcase classname='fake' name='passes' /></testsuite>",
                encoding="utf-8",
            )
            result = environment_lifecycle.CommandResult(args, 0, "1 passed\n")
        else:
            result = environment_lifecycle.CommandResult(args, 0, "")

        message = f"$ {command}\n{result.stdout}"
        if append:
            environment_lifecycle.append_log(log_path, message)
        else:
            environment_lifecycle.write_log(log_path, message)
        return result

    environment_lifecycle.run_command = fake_run_command
    environment_lifecycle.urlopen = fake_urlopen
    try:
        rc = environment_lifecycle.main(
            [
                "--output-dir",
                str(output_dir),
                "--build-artifact-dir",
                str(build_dir),
                "--repository",
                "RanamicusTechnology/11-env-hands-on",
                "--workflow-run-id",
                "28729279045",
                "--workflow-run-attempt",
                "1",
                "--test-run-id",
                "TR-UT-ISSUE-7-28729279045-A1",
                "--issue-number",
                "7",
                "--target-version",
                "0.0.0",
                "--required-final-stage",
                "UT",
                "--pr-number",
                "8",
                "--pr-head-sha",
                "6780c750712f373187be0654642548eb6e93f841",
                "--governance-job-result",
                "success",
                "--governance-result",
                "success",
                "--static-analysis-job-result",
                "success",
                "--static-analysis-result",
                "success",
                "--unit-test-job-result",
                "success",
                "--unit-test-result",
                "success",
                "--build-package-job-result",
                "success",
                "--build-package-result",
                "success",
                "--build-artifact-name",
                "build-go-app_TR-UT-ISSUE-7-28729279045-A1",
                "--build-artifact-id",
                "8088230457",
                "--build-artifact-version",
                version,
                "--build-artifact-checksum",
                checksum,
                "--build-artifact-uploaded",
                "true",
                "--github-output",
                str(github_output),
                "--created-at",
                "2026-07-05T00:00:00Z",
            ]
        )
    finally:
        environment_lifecycle.run_command = original_run_command
        environment_lifecycle.urlopen = original_urlopen

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    result = json.loads(
        (output_dir / "environment-lifecycle-result.json").read_text(encoding="utf-8")
    )
    assert result["environment_lifecycle_result"] == "success"
    assert manifest["test_result"] == "Passed"
    assert manifest["infrastructure_test_execution_state"] == "Completed"
    assert manifest["infrastructure_test_result"] == "Passed"
    assert manifest["api_test_execution_state"] == "Completed"
    assert manifest["api_test_result"] == "Passed"
    assert manifest["missing_evidence"] == []
    assert manifest["missing_evidence_count"] == 0
    assert manifest["environment_evidence_complete"] is True
    assert result["evidence"]["missing_evidence_count"] == 0
    assert result["evidence"]["environment_evidence_complete"] is True
    assert result["tests"]["infrastructure"]["result_files"] == [
        "test-results/infrastructure-test-junit.xml",
        "test-results/infrastructure-test-result.json",
        "summaries/infrastructure-test-summary.md",
    ]
    assert "logs/infrastructure-test.log" in manifest["collected_evidence"]
    assert "test-results/api-test-junit.xml" in manifest["collected_evidence"]
    outputs = github_output.read_text(encoding="utf-8")
    assert "missing_evidence_count=0" in outputs
    assert "environment_evidence_complete=true" in outputs
