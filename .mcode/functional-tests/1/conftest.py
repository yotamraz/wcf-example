"""
Shared helpers and constants for functional tests.
"""
import subprocess
import os

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
