"""
EventSieve - CLI Module

Command-line argument parsing and setup.
"""

import argparse


def setup_parser():
    """Setup and return the argument parser."""
    parser = argparse.ArgumentParser(
        description='EventSieve - Rule-Based Log Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python -m src.main -l access.log -r rules.json -o report.txt
  python -m src.main --log-file /var/log/auth.log --rules-file custom_rules.json
  python -m src.main -l sample.log -r rules.json --watch --interval 1.0
        """
    )

    parser.add_argument(
        '-l', '--log-file',
        required=True,
        help='Path to the log file to analyze'
    )

    parser.add_argument(
        '-r', '--rules-file',
        default='rules.json',
        help='Path to the rules file (default: rules.json)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Path to save TXT report (optional)'
    )

    parser.add_argument(
        '--html-output',
        help='Path to save HTML report (optional)'
    )

    parser.add_argument(
        '--watch',
        action='store_true',
        help='Enable real-time monitoring mode'
    )

    parser.add_argument(
        '--interval',
        type=float,
        default=1.0,
        help='Check interval in seconds for watch mode (default: 1.0)'
    )

    return parser