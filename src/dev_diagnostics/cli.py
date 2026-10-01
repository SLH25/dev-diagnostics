import argparse
import json
import sys

from .events import analyze_events, load_events
from .reports import (
    create_report,
    determine_overall_status,
    generate_json,
    generate_text,
)


def build_parser():
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Inspect a developer machine and "
            "generate a health report."
        )
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the environment report as JSON.",
    )

    parser.add_argument(
        "--events",
        metavar="FILE",
        help="Analyze diagnostic events from a JSON file.",
    )

    return parser


def main():
    """Run the CLI application."""

    parser = build_parser()
    args = parser.parse_args()

    report = create_report()

    if args.events:
        try:
            events = load_events(args.events)
            report["events"] = analyze_events(events)

        except (OSError, json.JSONDecodeError) as error:
            print(
                f"Error reading events file: {error}",
                file=sys.stderr,
            )
            return 2

    environment_status = determine_overall_status(report)

    statuses = [environment_status]

    if "events" in report:
        statuses.append(report["events"]["status"])

    if "CRITICAL" in statuses:
        overall_status = "CRITICAL"
    elif "WARNING" in statuses:
        overall_status = "WARNING"
    else:
        overall_status = "OK"

    report["overall_status"] = overall_status

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(generate_text(report))

        if "events" in report:
            events = report["events"]

            print()
            print("Diagnostic Events")
            print("-" * 50)
            print(f"Total events:      {events['total_events']}")
            print(f"INFO:              {events['info']}")
            print(f"WARNINGS:          {events['warnings']}")
            print(f"ERRORS:            {events['errors']}")
            print(
                f"Average latency:   "
                f"{events['average_latency_ms']} ms"
            )
            print(f"Status:             {events['status']}")

            print()
            print("Services")

            for service, count in events["services"].items():
                print(f"  {service}: {count}")

    if overall_status == "CRITICAL":
        return 2

    if overall_status == "WARNING":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())