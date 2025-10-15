"""
EventSieve - Display Module

Handles terminal display, banners, and UI elements.
"""

import os
from pathlib import Path
from colorama import init, Fore, Back, Style

# Colorama başlat
init(autoreset=True)


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
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}MAIN MENU{Style.RESET_ALL}                                                 {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[1]{Style.RESET_ALL} Select Log File                                       {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[2]{Style.RESET_ALL} Select Rules File                                     {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[3]{Style.RESET_ALL} Start Analysis                                        {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[4]{Style.RESET_ALL} Set TXT Report File                                   {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[5]{Style.RESET_ALL} Generate HTML Report                                  {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[6]{Style.RESET_ALL} Start Real-time Monitoring                            {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[7]{Style.RESET_ALL} Current Settings                                      {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}[0]{Style.RESET_ALL} Exit                                                  {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
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