#!/usr/bin/env python3
"""
EventSieve - Rule-Based Log Analysis Tool

Main entry point for the application.
"""

import sys
from pathlib import Path

from .ui.cli import setup_parser
from .ui.interactive import interactive_mode
from .core.rules import load_rules
from .core.analyzer import analyze_log
from .core.watcher import watch_log_file
from .reports.text_report import generate_report
from .reports.html_report import generate_html_report


def main():
    """Main application entry point."""
    # If arguments provided, run in command line mode
    if len(sys.argv) > 1:
        parser = setup_parser()
        args = parser.parse_args()

        # Check file paths
        log_path = Path(args.log_file)
        rules_path = Path(args.rules_file)

        if not log_path.exists():
            print(f"Error: Log file not found: {log_path}")
            sys.exit(1)

        if not rules_path.exists():
            print(f"Error: Rules file not found: {rules_path}")
            sys.exit(1)

        # Check if watch mode is enabled
        if args.watch:
            # Start real-time monitoring
            watch_log_file(str(log_path), str(rules_path), args.output, args.html_output, args.interval)
            return

        print("EventSieve - Starting Log Analysis...")
        print(f"Log file: {log_path}")
        print(f"Rules file: {rules_path}")
        if args.output:
            print(f"Output file: {args.output}")
        print("-" * 50)

        # Load rules
        rules = load_rules(str(rules_path))
        if not rules:
            sys.exit(1)
        print(f"{len(rules)} rules loaded.")

        # Analyze log
        activities = analyze_log(str(log_path), rules)

        # Generate reports
        generate_report(activities, args.output)

        if args.html_output:
            generate_html_report(activities, args.html_output, str(log_path), str(rules_path))
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()