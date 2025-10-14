"""
EventSieve - Text Report Module

Generates text-based reports for console and file output.
"""

from colorama import Fore, Back, Style


def generate_report(activities, output_file=None):
    """Generate report."""
    if not activities:
        report = f"{Fore.GREEN}No suspicious activities found.{Style.RESET_ALL}"
    else:
        report = f"{Fore.YELLOW}Total {len(activities)} suspicious activities found:{Style.RESET_ALL}\n\n"
        for i, activity in enumerate(activities, 1):
            severity_color = {
                'low': Fore.GREEN,
                'medium': Fore.YELLOW,
                'high': Fore.RED,
                'critical': Fore.RED + Back.WHITE
            }.get(activity['severity'], Fore.WHITE)

            report += f"{Fore.CYAN}{i}. Line {activity['line_number']}: {activity['rule']} {severity_color}(Severity: {activity['severity']}){Style.RESET_ALL}\n"
            report += f"{Fore.WHITE}   Content: {activity['line']}{Style.RESET_ALL}\n"
            report += f"{Fore.WHITE}   Pattern: {activity['pattern']}{Style.RESET_ALL}\n\n"

    if output_file:
        try:
            # Plain report for file
            plain_report = report.replace(Fore.GREEN, '').replace(Fore.YELLOW, '').replace(Fore.RED, '').replace(Fore.CYAN, '').replace(Fore.WHITE, '').replace(Back.WHITE, '').replace(Style.RESET_ALL, '')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(plain_report)
            print(f"{Fore.GREEN}Report saved: {output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: Error saving report: {e}{Style.RESET_ALL}")

    print(report)