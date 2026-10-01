import os
import platform
import shutil
import subprocess
import sys


def check_python():
    """Check the installed Python version."""

    version = platform.python_version()

    major, minor = sys.version_info[:2]

    if major == 3 and minor >= 10:
        status = "OK"
    else:
        status = "WARNING"

    return {
        "name": "Python",
        "version": version,
        "status": status,
    }


def check_disk():
    """Check available disk space."""

    root = os.path.abspath(os.sep)

    total, used, free = shutil.disk_usage(root)

    total_gb = round(total / (1024 ** 3), 2)
    free_gb = round(free / (1024 ** 3), 2)

    if free_gb < 10:
        status = "CRITICAL"
    elif free_gb < 20:
        status = "WARNING"
    else:
        status = "OK"

    return {
        "name": "Disk",
        "total_gb": total_gb,
        "free_gb": free_gb,
        "status": status,
    }


def check_environment():
    """Check important environment variables."""

    variables = [
        "PATH",
        "USERPROFILE",
        "TEMP",
    ]

    result = {}

    for variable in variables:
        result[variable] = (
            "configured"
            if os.environ.get(variable)
            else "missing"
        )

    status = (
        "OK"
        if all(value == "configured" for value in result.values())
        else "WARNING"
    )

    return {
        "name": "Environment",
        "variables": result,
        "status": status,
    }


def check_tool(tool_name):
    """Check whether a developer tool is installed."""

    try:
        result = subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if result.returncode == 0 and output:
            first_line = output.splitlines()[0]

            return {
                "name": tool_name,
                "installed": True,
                "version": first_line,
                "status": "OK",
            }

    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return {
        "name": tool_name,
        "installed": False,
        "version": None,
        "status": "WARNING",
    }


def check_developer_tools():
    """Check common developer tools."""

    tools = [
        "git",
        "docker",
        "node",
        "java",
    ]

    return [
        check_tool(tool)
        for tool in tools
    ]