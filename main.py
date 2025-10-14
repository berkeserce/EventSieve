#!/usr/bin/env python3
"""
EventSieve - Rule-Based Log Analysis Tool

Legacy entry point - redirects to new modular structure.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the new main module
from src.main import main

if __name__ == '__main__':
    main()


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
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: Error reading log file: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    return suspicious_activities


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


def generate_html_report(activities, output_file, log_file, rules_file):
    """Generate HTML report."""
    try:
        # Read template file
        template_path = Path(__file__).parent / "report_template.html"
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


def show_banner():
    """Show hacker themed banner."""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""
{Fore.GREEN}{'='*60}{Style.RESET_ALL}
{Fore.RED}███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗██╗███████╗██╗   ██╗███████╗{Style.RESET_ALL}
{Fore.RED}██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝██║██╔════╝██║   ██║██╔════╝{Style.RESET_ALL}
{Fore.YELLOW}█████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗██║█████╗  ██║   ██║█████╗  {Style.RESET_ALL}
{Fore.YELLOW}██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║██║██╔══╝  ╚██╗ ██╔╝██╔══╝  {Style.RESET_ALL}
{Fore.CYAN}███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║██║███████╗ ╚████╔╝ ███████╗{Style.RESET_ALL}
{Fore.CYAN}╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝╚══════╝  ╚═══╝  ╚══════╝{Style.RESET_ALL}
{Fore.GREEN}{'='*60}{Style.RESET_ALL}
{Fore.MAGENTA}           Rule-Based Log Analysis Tool v1.0{Style.RESET_ALL}
{Fore.GREEN}{'='*60}{Style.RESET_ALL}
""")


def show_menu():
    """Show main menu."""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}MAIN MENU{Style.RESET_ALL}                                                  {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[1]{Style.RESET_ALL} Select Log File                                       {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[2]{Style.RESET_ALL} Select Rules File                                     {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[3]{Style.RESET_ALL} Start Analysis                                        {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[4]{Style.RESET_ALL} Set TXT Report File                                 {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[5]{Style.RESET_ALL} Generate HTML Report                                 {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[6]{Style.RESET_ALL} Start Real-time Monitoring                          {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[7]{Style.RESET_ALL} Current Settings                                      {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}[0]{Style.RESET_ALL} Exit                                                   {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()


def get_file_path(prompt, default=None, file_type="file"):
    """Get file path from user."""
    while True:
        if default:
            path = input(f"{Fore.CYAN}{prompt} ({Fore.GREEN}default: {default}{Fore.CYAN}): {Style.RESET_ALL}").strip()
            if not path:
                path = default
        else:
            path = input(f"{Fore.CYAN}{prompt}: {Style.RESET_ALL}").strip()
        
        if not path:
            print(f"{Fore.RED}Error: {file_type} path cannot be empty!{Style.RESET_ALL}")
            continue
            
        path_obj = Path(path)
        if path_obj.exists():
            return str(path_obj)
        else:
            print(f"{Fore.RED}Error: {path} file not found!{Style.RESET_ALL}")
            if input(f"{Fore.YELLOW}Do you want to try again? (y/n): {Style.RESET_ALL}").lower() != 'y':
                return None


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
        
        choice = input(f"{Fore.GREEN}Your choice (0-6): {Style.RESET_ALL}").strip()
        
        if choice == '0':
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
            
        elif choice == '1':
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
            generate_report(activities, config['output_file'])
            
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


def watch_log_file(log_file, rules_file, output_file=None, html_output_file=None, interval=1.0):
    """Watch log file for changes and analyze new entries in real-time."""
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
                            
                            for rule in rules:
                                pattern = rule.get('pattern', '')
                                description = rule.get('description', 'Unknown rule')
                                severity = rule.get('severity', 'low')
                                
                                try:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        activity = {
                                            'line_number': actual_line_num,
                                            'line': line,
                                            'rule': description,
                                            'severity': severity,
                                            'pattern': pattern,
                                            'timestamp': datetime.now().strftime('%H:%M:%S')
                                        }
                                        
                                        # Check if this activity is new (not in last_activities)
                                        if activity not in last_activities:
                                            new_activities.append(activity)
                                            
                                except re.error as e:
                                    print(f"{Fore.YELLOW}Warning: Invalid regex pattern '{pattern}': {e}{Style.RESET_ALL}")
                    
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
                                        
                                        for rule in rules:
                                            pattern = rule.get('pattern', '')
                                            description = rule.get('description', 'Unknown rule')
                                            severity = rule.get('severity', 'low')
                                            
                                            try:
                                                if re.search(pattern, line, re.IGNORECASE):
                                                    all_activities.append({
                                                        'line_number': line_num,
                                                        'line': line,
                                                        'rule': description,
                                                        'severity': severity,
                                                        'pattern': pattern
                                                    })
                                            except re.error:
                                                pass
                                
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
        activities = analyze_log(log_file, rules)
        
        if output_file:
            generate_report(activities, output_file)
        
        if html_output_file:
            generate_html_report(activities, html_output_file, log_file, rules_file)


def main():
    # If arguments provided, run in command line mode
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description='EventSieve - Rule-Based Log Analysis Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Example usage:
  python main.py -l access.log -r rules.json -o report.txt
  python main.py --log-file /var/log/auth.log --rules-file custom_rules.json
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
        
        args = parser.parse_args()
        
        # Check file paths
        log_path = Path(args.log_file)
        rules_path = Path(args.rules_file)
        
        if not log_path.exists():
            print(f"{Fore.RED}Error: Log file not found: {log_path}{Style.RESET_ALL}")
            sys.exit(1)
        
        if not rules_path.exists():
            print(f"{Fore.RED}Error: Rules file not found: {rules_path}{Style.RESET_ALL}")
            sys.exit(1)
        
        # Check if watch mode is enabled
        if args.watch:
            # Start real-time monitoring
            watch_log_file(str(log_path), str(rules_path), args.output, args.html_output, args.interval)
            return
        
        print(f"{Fore.GREEN}EventSieve - Starting Log Analysis...{Style.RESET_ALL}")
        print(f"Log file: {log_path}")
        print(f"Rules file: {rules_path}")
        if args.output:
            print(f"Output file: {args.output}")
        print(f"{Fore.GREEN}{'-' * 50}{Style.RESET_ALL}")
        
        # Load rules
        rules = load_rules(rules_path)
        if not rules:
            sys.exit(1)
        print(f"{len(rules)} rules loaded.")
        
        # Analyze log
        activities = analyze_log(log_path, rules)
        
        # Generate report
        generate_report(activities, args.output)
        
        # Generate HTML report (if specified)
        if hasattr(args, 'html_output') and args.html_output:
            generate_html_report(activities, args.html_output, str(log_path), str(rules_path))
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()