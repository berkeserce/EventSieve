"""
EventSieve - Rules Module

Handles loading and validation of JSON rule files.
"""

import json
from pathlib import Path
from colorama import Fore, Style


def load_rules(rules_file):
    """Load the rules file."""
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Rules file not found: {rules_file}{Style.RESET_ALL}")
        return None
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Rules file is invalid JSON: {e}{Style.RESET_ALL}")
        return None


def validate_rules(rules):
    """Validate rules structure."""
    if not isinstance(rules, list):
        print(f"{Fore.RED}Error: Rules file must contain a list of rules{Style.RESET_ALL}")
        return False

    required_fields = ['pattern', 'description', 'severity']
    valid_severities = ['low', 'medium', 'high', 'critical']

    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            print(f"{Fore.RED}Error: Rule {i+1} must be a dictionary{Style.RESET_ALL}")
            return False

        for field in required_fields:
            if field not in rule:
                print(f"{Fore.RED}Error: Rule {i+1} missing required field: {field}{Style.RESET_ALL}")
                return False

        if rule['severity'] not in valid_severities:
            print(f"{Fore.RED}Error: Rule {i+1} has invalid severity: {rule['severity']}{Style.RESET_ALL}")
            return False

    return True