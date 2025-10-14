"""
EventSieve - Analyzer Module

Core log analysis functionality using regex patterns.
"""

import re
from pathlib import Path
from colorama import Fore, Style


def analyze_log(log_file, rules):
    """Analyze the log file and return suspicious activities."""
    suspicious_activities = []

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                for rule in rules:
                    pattern = rule.get('pattern', '')
                    description = rule.get('description', 'Unknown rule')
                    severity = rule.get('severity', 'low')

                    try:
                        if re.search(pattern, line, re.IGNORECASE):
                            suspicious_activities.append({
                                'line_number': line_num,
                                'line': line,
                                'rule': description,
                                'severity': severity,
                                'pattern': pattern
                            })
                    except re.error as e:
                        print(f"{Fore.YELLOW}Warning: Invalid regex pattern '{pattern}': {e}{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}Error: Log file not found: {log_file}{Style.RESET_ALL}")
        raise
    except Exception as e:
        print(f"{Fore.RED}Error: Error reading log file: {e}{Style.RESET_ALL}")
        raise

    return suspicious_activities


def analyze_log_line(line, line_num, rules):
    """Analyze a single log line and return matching activities."""
    activities = []
    line = line.strip()

    for rule in rules:
        pattern = rule.get('pattern', '')
        description = rule.get('description', 'Unknown rule')
        severity = rule.get('severity', 'low')

        try:
            if re.search(pattern, line, re.IGNORECASE):
                activities.append({
                    'line_number': line_num,
                    'line': line,
                    'rule': description,
                    'severity': severity,
                    'pattern': pattern
                })
        except re.error as e:
            print(f"{Fore.YELLOW}Warning: Invalid regex pattern '{pattern}': {e}{Style.RESET_ALL}")

    return activities