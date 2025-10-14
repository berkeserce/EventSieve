"""
EventSieve - HTML Report Module

Generates HTML reports using Jinja2 templates.
"""

import os
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style
from jinja2 import Template


def generate_html_report(activities, output_file, log_file, rules_file):
    """Generate HTML report."""
    try:
        # Read template file
        template_path = Path(__file__).parent.parent.parent / "report_template.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        template = Template(template_content)

        # Calculate statistics
        total_activities = len(activities)

        severity_counts = {
            'low': 0,
            'medium': 0,
            'high': 0,
            'critical': 0
        }

        for activity in activities:
            severity = activity.get('severity', 'low')
            severity_counts[severity] += 1

        # Calculate percentage (show minimum 5%)
        max_count = max(severity_counts.values()) if severity_counts.values() else 1
        severity_percentages = {}
        for severity, count in severity_counts.items():
            percentage = max(5, (count / max_count) * 100) if count > 0 else 5
            severity_percentages[severity] = percentage

        # Template variables
        template_vars = {
            'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'total_activities': total_activities,
            'activities': activities,
            'log_file': log_file,
            'rules_file': rules_file,
            'low_count': severity_counts['low'],
            'medium_count': severity_counts['medium'],
            'high_count': severity_counts['high'],
            'critical_count': severity_counts['critical'],
            'low_percentage': severity_percentages['low'],
            'medium_percentage': severity_percentages['medium'],
            'high_percentage': severity_percentages['high'],
            'critical_percentage': severity_percentages['critical']
        }

        # Generate HTML
        html_content = template.render(**template_vars)

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"{Fore.GREEN}✓ HTML report generated: {output_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}To open in web browser: file://{Path(output_file).resolve()}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: Could not generate HTML report: {e}{Style.RESET_ALL}")