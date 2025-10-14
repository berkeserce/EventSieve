"""
EventSieve - Watcher Module

Real-time log file monitoring functionality.
"""

import time
from pathlib import Path
from datetime import datetime
from colorama import Fore, Back, Style

from .analyzer import analyze_log_line
from ..reports.html_report import generate_html_report


def watch_log_file(log_file, rules_file, output_file=None, html_output_file=None, interval=1.0):
    """Watch log file for changes and analyze new entries in real-time."""
    from .rules import load_rules

    print(f"{Fore.GREEN}EventSieve - Real-time Log Monitoring Started{Style.RESET_ALL}")
    print(f"Log file: {log_file}")
    print(f"Rules file: {rules_file}")
    print(f"Check interval: {interval} seconds")
    print(f"{Fore.GREEN}{'-' * 60}{Style.RESET_ALL}")

    # Load rules
    rules = load_rules(rules_file)
    if not rules:
        return

    print(f"{len(rules)} rules loaded.")
    print(f"{Fore.CYAN}Monitoring for new log entries... (Press Ctrl+C to stop){Style.RESET_ALL}")

    # Track last position in file
    last_position = 0
    last_activities = []

    try:
        while True:
            try:
                # Check if file exists
                if not Path(log_file).exists():
                    print(f"{Fore.YELLOW}Warning: Log file not found, waiting...{Style.RESET_ALL}")
                    time.sleep(interval)
                    continue

                # Get current file size
                current_size = Path(log_file).stat().st_size

                # If file was truncated or reset, reset position
                if current_size < last_position:
                    last_position = 0

                # If file has grown, read new content
                if current_size > last_position:
                    new_activities = []

                    with open(log_file, 'r', encoding='utf-8') as f:
                        f.seek(last_position)
                        lines = f.readlines()

                        for line_num_offset, line in enumerate(lines, 1):
                            line = line.strip()
                            if not line:
                                continue

                            # Calculate actual line number in file
                            actual_line_num = sum(1 for _ in open(log_file, 'r', encoding='utf-8')) - len(lines) + line_num_offset

                            # Analyze the line
                            activities = analyze_log_line(line, actual_line_num, rules)

                            for activity in activities:
                                # Check if this activity is new (not in last_activities)
                                if activity not in last_activities:
                                    new_activities.append(activity)

                    # Display new activities
                    if new_activities:
                        print(f"\n{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] New suspicious activities detected:{Style.RESET_ALL}")

                        for activity in new_activities:
                            severity_color = {
                                'low': Fore.GREEN,
                                'medium': Fore.YELLOW,
                                'high': Fore.RED,
                                'critical': Fore.RED + Back.WHITE
                            }.get(activity['severity'], Fore.WHITE)

                            print(f"{Fore.CYAN}Line {activity['line_number']}: {activity['rule']} {severity_color}(Severity: {activity['severity']}){Style.RESET_ALL}")
                            print(f"{Fore.WHITE}   Content: {activity['line']}{Style.RESET_ALL}")

                        last_activities.extend(new_activities)

                        # Keep only last 100 activities to prevent memory issues
                        if len(last_activities) > 100:
                            last_activities = last_activities[-100:]

                        # Update HTML report if specified
                        if html_output_file:
                            all_activities = []
                            # Read all activities from file for complete report
                            try:
                                with open(log_file, 'r', encoding='utf-8') as f:
                                    for line_num, line in enumerate(f, 1):
                                        line = line.strip()
                                        if not line:
                                            continue

                                        activities = analyze_log_line(line, line_num, rules)
                                        all_activities.extend(activities)

                                generate_html_report(all_activities, html_output_file, log_file, rules_file)
                                print(f"{Fore.GREEN}HTML report updated.{Style.RESET_ALL}")
                            except Exception as e:
                                print(f"{Fore.YELLOW}Warning: Could not update HTML report: {e}{Style.RESET_ALL}")

                    # Update last position
                    last_position = current_size

                # Wait before next check
                time.sleep(interval)

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Monitoring stopped by user.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error during monitoring: {e}{Style.RESET_ALL}")
                time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Real-time monitoring stopped.{Style.RESET_ALL}")

    # Generate final reports if requested
    if output_file or html_output_file:
        print(f"{Fore.CYAN}Generating final reports...{Style.RESET_ALL}")

        # Analyze complete log file
        from .analyzer import analyze_log
        activities = analyze_log(log_file, rules)

        if output_file:
            from ..reports.text_report import generate_report
            generate_report(activities, output_file)

        if html_output_file:
            generate_html_report(activities, html_output_file, log_file, rules_file)