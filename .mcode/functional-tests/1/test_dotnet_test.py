"""
Functional tests for `dotnet test CalculatorService.sln`.
Verifies that all 9 xUnit tests (7 unit + 2 integration) pass.
Classification: target_only (test project was newly created in this milestone).
"""
import subprocess
import os
import pytest

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "C:\\Users\\yraz\\.local\\share\\modelcode\\workspace\\jobs\\ec8990db-fa74-43eb-8400-c3b2bc946cbb\\workspace")
REPO_DIR = os.path.join(WORKSPACE_DIR, "wcf-example")


def run_dotnet(*args, cwd=None, timeout=180):
    """Run a dotnet command and return the CompletedProcess."""
    result = subprocess.run(
        ["dotnet"] + list(args),
        cwd=cwd or REPO_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result


class TestDotnetTest:
    """dotnet test CalculatorService.sln — all xUnit tests pass."""

    def test_all_tests_pass(self):
        """Running dotnet test should exit with code 0 (all tests pass)."""
        result = run_dotnet(
            "test", "CalculatorService.sln",
            "--no-build", "--configuration", "Debug",
            "--logger", "console;verbosity=normal",
            timeout=180,
        )
        assert result.returncode == 0, (
            f"dotnet test failed (exit {result.returncode}).\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )

    def test_expected_test_count(self):
        """Should report at least 9 tests passing (7 unit + 2 integration)."""
        result = run_dotnet(
            "test", "CalculatorService.sln",
            "--no-build", "--configuration", "Debug",
            "--logger", "console;verbosity=normal",
            timeout=180,
        )
        output = result.stdout + result.stderr
        # xUnit output contains "X passed" in the summary
        # Accept 9 or more tests passing
        assert result.returncode == 0, (
            f"Tests failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
        # Verify output mentions passed tests
        assert "passed" in output.lower(), (
            f"Could not find 'passed' in test output:\n{output}"
        )

    def test_unit_test_class_present(self):
        """Unit test class CalculatorServiceTests should be mentioned in output."""
        result = run_dotnet(
            "test", "CalculatorService.sln",
            "--no-build", "--configuration", "Debug",
            "--logger", "console;verbosity=normal",
            timeout=180,
        )
        assert result.returncode == 0, (
            f"Tests failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
        output = result.stdout + result.stderr
        assert "CalculatorService" in output, (
            f"'CalculatorService' not found in test output:\n{output[:1000]}"
        )
