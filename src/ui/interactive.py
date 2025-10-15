"""
EventSieve - Interactive Module

Interactive menu system for user-friendly operation.
"""

from pathlib import Path
from colorama import Fore, Style

from .display import show_banner, show_menu, get_file_path
from ..core.rules import load_rules
from ..core.analyzer import analyze_log
from ..core.watcher import watch_log_file
from ..reports.text_report import generate_report
from ..reports.html_report import generate_html_report
from ..utils.system_logs import scan_system_logs, display_found_logs, select_log_files


def interactive_mode():
    """Interactive mode."""
    show_banner()

    config = {
        'log_file': None,
        'rules_file': 'rules.json',
        'output_file': None,
        'html_output_file': None
    }

    while True:
        show_menu()

        choice = input(f"{Fore.GREEN}Your choice (0-7): {Style.RESET_ALL}").strip()

        if choice == '0':
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break

        elif choice == '1':
            # Ask if user wants to scan system logs
            scan_choice = input(f"{Fore.CYAN}Scan system for available log files? (y/n): {Style.RESET_ALL}").lower().strip()

            if scan_choice == 'y':
                print(f"{Fore.YELLOW}🔍 Scanning system for log files...{Style.RESET_ALL}")

                found_logs = scan_system_logs()
                display_found_logs(found_logs)

                if found_logs:
                    selected_files = select_log_files(found_logs)

                    if selected_files:
                        if len(selected_files) == 1:
                            config['log_file'] = selected_files[0]
                            print(f"{Fore.GREEN}✓ Log file set: {selected_files[0]}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}Multiple files selected. Please choose one for analysis.{Style.RESET_ALL}")
                            # Show numbered list for final selection
                            for i, file_path in enumerate(selected_files, 1):
                                print(f"{i}. {file_path}")

                            final_choice = input("Select file number: ").strip()
                            try:
                                idx = int(final_choice) - 1
                                if 0 <= idx < len(selected_files):
                                    config['log_file'] = selected_files[idx]
                                    print(f"{Fore.GREEN}✓ Log file set: {selected_files[idx]}{Style.RESET_ALL}")
                                else:
                                    print(f"{Fore.RED}Invalid selection{Style.RESET_ALL}")
                            except ValueError:
                                print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}No files selected. Please choose manually.{Style.RESET_ALL}")
                        log_file = get_file_path("Enter log file path manually", file_type="Log file")
                        if log_file:
                            config['log_file'] = log_file
                            print(f"{Fore.GREEN}✓ Log file set: {log_file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}No system logs found. Please enter path manually.{Style.RESET_ALL}")
                    log_file = get_file_path("Enter log file path", file_type="Log file")
                    if log_file:
                        config['log_file'] = log_file
                        print(f"{Fore.GREEN}✓ Log file set: {log_file}{Style.RESET_ALL}")
            else:
                # Manual file selection
                log_file = get_file_path("Enter log file path", file_type="Log file")
                if log_file:
                    config['log_file'] = log_file
                    print(f"{Fore.GREEN}✓ Log file set: {log_file}{Style.RESET_ALL}")

        elif choice == '2':
            rules_file = get_file_path("Enter rules file path", config['rules_file'], file_type="Rules file")
            if rules_file:
                config['rules_file'] = rules_file
                print(f"{Fore.GREEN}✓ Rules file set: {rules_file}{Style.RESET_ALL}")

        elif choice == '3':
            if not config['log_file']:
                print(f"{Fore.RED}Error: Please select log file first!{Style.RESET_ALL}")
                continue

            if not config['rules_file']:
                print(f"{Fore.RED}Error: Rules file not found!{Style.RESET_ALL}")
                continue

            print(f"{Fore.YELLOW}Starting analysis...{Style.RESET_ALL}")

            # Load rules
            rules = load_rules(config['rules_file'])
            if not rules:
                continue

            print(f"{Fore.GREEN}{len(rules)} rules loaded.{Style.RESET_ALL}")

            # Analyze log
            activities = analyze_log(config['log_file'], rules)

            # Generate TXT report
            output_file = config['output_file']
            if not output_file:
                # Auto-generate filename based on log file
                from pathlib import Path
                log_name = Path(config['log_file']).stem
                output_file = f"{log_name}_analysis.txt"
                print(f"{Fore.YELLOW}No TXT output file specified, saving to: {output_file}{Style.RESET_ALL}")

            generate_report(activities, output_file)

            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            show_banner()

        elif choice == '4':
            output_file = input(f"{Fore.CYAN}Enter TXT report file path (leave empty to not save report): {Style.RESET_ALL}").strip()
            if output_file:
                config['output_file'] = output_file
                print(f"{Fore.GREEN}✓ TXT report file set: {output_file}{Style.RESET_ALL}")
            else:
                config['output_file'] = None
                print(f"{Fore.YELLOW}TXT report file removed.{Style.RESET_ALL}")

        elif choice == '5':
            if not config['log_file']:
                print(f"{Fore.RED}Error: Please select log file first!{Style.RESET_ALL}")
                continue

            if not config['rules_file']:
                print(f"{Fore.RED}Error: Rules file not found!{Style.RESET_ALL}")
                continue

            html_file = input(f"{Fore.CYAN}Enter HTML report file path (default: report.html): {Style.RESET_ALL}").strip()
            if not html_file:
                html_file = 'report.html'

            print(f"{Fore.YELLOW}Generating HTML report...{Style.RESET_ALL}")

            # Load rules
            rules = load_rules(config['rules_file'])
            if not rules:
                continue

            # Analyze log
            activities = analyze_log(config['log_file'], rules)

            # Generate HTML report
            generate_html_report(activities, html_file, config['log_file'], config['rules_file'])

            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            show_banner()

        elif choice == '6':
            if not config['log_file']:
                print(f"{Fore.RED}Error: Please select log file first!{Style.RESET_ALL}")
                continue

            if not config['rules_file']:
                print(f"{Fore.RED}Error: Rules file not found!{Style.RESET_ALL}")
                continue

            interval = input(f"{Fore.CYAN}Enter check interval in seconds (default: 1.0): {Style.RESET_ALL}").strip()
            if not interval:
                interval = 1.0
            else:
                try:
                    interval = float(interval)
                except ValueError:
                    print(f"{Fore.RED}Invalid interval, using default 1.0 seconds.{Style.RESET_ALL}")
                    interval = 1.0

            print(f"{Fore.YELLOW}Starting real-time monitoring...{Style.RESET_ALL}")

            # Load rules
            rules = load_rules(config['rules_file'])
            if not rules:
                continue

            # Start real-time monitoring
            watch_log_file(config['log_file'], config['rules_file'], config['output_file'], config['html_output_file'], interval)

            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            show_banner()

        elif choice == '7':
            print(f"\n{Fore.CYAN}Current Settings:{Style.RESET_ALL}")
            print(f"  Log File: {config['log_file'] or 'Not specified'}")
            print(f"  Rules File: {config['rules_file'] or 'Not specified'}")
            print(f"  TXT Report File: {config['output_file'] or 'Will not be saved'}")
            print(f"  HTML Report File: {config['html_output_file'] or 'Not specified'}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            show_banner()

        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            continue