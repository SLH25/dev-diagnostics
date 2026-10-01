import json
from pathlib import Path


def load_events(file_path):
    """Load diagnostic events from a JSON file."""

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("events", [])


def analyze_events(events):
    """Analyze diagnostic events."""

    total = len(events)

    info_count = 0
    warning_count = 0
    error_count = 0

    latencies = []

    services = {}

    for event in events:
        level = event.get("level", "").upper()
        service = event.get("service", "unknown")
        latency = event.get("latency_ms")

        if level == "INFO":
            info_count += 1
        elif level == "WARN":
            warning_count += 1
        elif level == "ERROR":
            error_count += 1

        if isinstance(latency, (int, float)):
            latencies.append(latency)

        services.setdefault(service, 0)
        services[service] += 1

    average_latency = (
        round(sum(latencies) / len(latencies), 2)
        if latencies
        else None
    )

    if error_count > 0:
        status = "CRITICAL"
    elif warning_count > 0:
        status = "WARNING"
    else:
        status = "OK"

    return {
        "total_events": total,
        "info": info_count,
        "warnings": warning_count,
        "errors": error_count,
        "average_latency_ms": average_latency,
        "services": services,
        "status": status,
    }