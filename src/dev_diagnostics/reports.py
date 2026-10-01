import json


def create_report():
    """Create a complete diagnostic report."""
    from .checks import (
        check_python,
        check_disk,
        check_environment,
        check_developer_tools,
    )

    return {
        "python": check_python(),
        "disk": check_disk(),
        "environment": check_environment(),
        "developer_tools": check_developer_tools(),
    }


def determine_overall_status(report):
    """Determine the overall health status."""

    statuses = []

    statuses.append(report["python"]["status"])
    statuses.append(report["disk"]["status"])
    statuses.append(report["environment"]["status"])

    for tool in report["developer_tools"]:
        statuses.append(tool["status"])

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    return "OK"


def generate_json(report):
    """Return the report as formatted JSON."""

    report["overall_status"] = determine_overall_status(report)

    return json.dumps(
        report,
        indent=2
    )


def generate_text(report):
    """Generate a human-readable report."""

    overall_status = determine_overall_status(report)

    lines = [
        "=" * 40,
        "Developer Environment Health Report",
        "=" * 40,
        "",
        "Python",
        f"  Version: {report['python']['version']}",
        f"  Status:  {report['python']['status']}",
        "",
        "Disk",
        f"  Total:   {report['disk']['total_gb']} GB",
        f"  Free:    {report['disk']['free_gb']} GB",
        f"  Status:  {report['disk']['status']}",
        "",
        "Environment Variables",
    ]

    for name, status in report["environment"]["variables"].items():
        lines.append(f"  {name}: {status}")

    lines.extend([
        f"  Status: {report['environment']['status']}",
        "",
        "Developer Tools",
    ])

    for tool in report["developer_tools"]:
        version = tool["version"] or "Not installed"

        lines.append(
            f"  {tool['name']}: {version} [{tool['status']}]"
        )

    lines.extend([
        "",
        f"Overall Status: {overall_status}",
        "=" * 40,
    ])

    return "\n".join(lines)