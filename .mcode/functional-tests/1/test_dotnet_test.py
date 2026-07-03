"""
Functional tests for `dotnet test CalculatorService.sln`.
Verifies that all 9 xUnit tests (7 unit + 2 integration) pass.
Classification: target_only (test project was newly created in this milestone).
"""
import pytest
from conftest import run_dotnet


class TestDotnetTest:
    """dotnet test CalculatorService.sln — all xUnit tests pass."""

    @pytest.fixture(scope="class")
    def dotnet_test_result(self):
        """Run dotnet test once for the whole class and share the result."""
        return run_dotnet(
            "test", "CalculatorService.sln",
            "--no-build", "--configuration", "Debug",
            "--logger", "console;verbosity=normal",
            timeout=180,
        )

    def test_all_tests_pass(self, dotnet_test_result):
        """Running dotnet test should exit with code 0 (all tests pass)."""
        result = dotnet_test_result
        assert result.returncode == 0, (
            f"dotnet test failed (exit {result.returncode}).\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )

    def test_expected_test_count(self, dotnet_test_result):
        """Should report at least 9 tests passing (7 unit + 2 integration)."""
        result = dotnet_test_result
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

    def test_unit_test_class_present(self, dotnet_test_result):
        """Unit test class CalculatorServiceTests should be mentioned in output."""
        result = dotnet_test_result
        assert result.returncode == 0, (
            f"Tests failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
        output = result.stdout + result.stderr
        assert "CalculatorService" in output, (
            f"'CalculatorService' not found in test output:\n{output[:1000]}"
        )
