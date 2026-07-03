"""
Functional tests for dotnet build.
Verifies that `dotnet build CalculatorService.sln` succeeds.
Classification: origin_and_target (build existed on Baseline Ref).
"""
import pytest
from conftest import run_dotnet


class TestDotnetBuild:
    """dotnet build CalculatorService.sln — happy path."""

    def test_build_succeeds(self):
        """Building the full solution should exit with code 0."""
        result = run_dotnet("build", "CalculatorService.sln", "--configuration", "Debug")
        assert result.returncode == 0, (
            f"dotnet build failed (exit {result.returncode}).\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
        output = result.stdout + result.stderr
        assert "error" not in output.lower() or "0 error" in output.lower(), (
            f"Build output contains errors:\n{output}"
        )
