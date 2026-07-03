"""
Functional tests for dotnet build.
Verifies that `dotnet build CalculatorService.sln` succeeds.
Classification: origin_and_target (build existed on Baseline Ref).
"""
import subprocess
import os
import pytest

WORKSPACE_DIR = os.environ["WORKSPACE_DIR"]
REPO_DIR = os.path.join(WORKSPACE_DIR, "wcf-example")


def run_dotnet(*args, cwd=None, timeout=120):
    """Run a dotnet command and return the CompletedProcess."""
    result = subprocess.run(
        ["dotnet"] + list(args),
        cwd=cwd or REPO_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result


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
