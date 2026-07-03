"""
Shared helpers and constants for functional tests.
"""
import subprocess
import os

WORKSPACE_DIR = os.environ["WORKSPACE_DIR"]
REPO_DIR = os.path.join(WORKSPACE_DIR, "wcf-example")

# Resolve the dotnet executable: prefer DOTNET_ROOT (set by pixi env activation),
# then fall back to "dotnet" on PATH.
_dotnet_root = os.environ.get("DOTNET_ROOT", "")
if _dotnet_root:
    DOTNET_EXE = os.path.join(_dotnet_root, "dotnet.exe")
    if not os.path.isfile(DOTNET_EXE):
        DOTNET_EXE = os.path.join(_dotnet_root, "dotnet")
else:
    DOTNET_EXE = "dotnet"


def run_dotnet(*args, cwd=None, timeout=120):
    """Run a dotnet command and return the CompletedProcess."""
    result = subprocess.run(
        [DOTNET_EXE] + list(args),
        cwd=cwd or REPO_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result
