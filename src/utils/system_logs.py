"""
EventSieve - System Logs Utility

Automatically discovers system log files on Linux systems.
"""

import os
from pathlib import Path
from typing import List, Dict


def get_common_log_paths() -> List[str]:
    """Get common system log file paths."""
    common_paths = [
        # Authentication logs
        "/var/log/auth.log",
        "/var/log/secure",

        # System logs
        "/var/log/syslog",
        "/var/log/messages",
        "/var/log/system.log",

        # Kernel logs
        "/var/log/kern.log",
        "/var/log/dmesg",

        # Web server logs
        "/var/log/apache2/access.log",
        "/var/log/apache2/error.log",
        "/var/log/httpd/access_log",
        "/var/log/httpd/error_log",
        "/var/log/nginx/access.log",
        "/var/log/nginx/error.log",

        # Database logs
        "/var/log/mysql/error.log",
        "/var/log/mysql/mysql.log",
        "/var/log/postgresql/postgresql.log",

        # Mail logs
        "/var/log/mail.log",
        "/var/log/maillog",

        # Other common logs
        "/var/log/cron",
        "/var/log/daemon.log",
        "/var/log/user.log",
        "/var/log/boot.log",
    ]

    return common_paths


def scan_system_logs() -> List[Dict[str, str]]:
    """Scan system for available log files."""
    found_logs = []

    for log_path in get_common_log_paths():
        path_obj = Path(log_path)

        if path_obj.exists() and path_obj.is_file():
            try:
                # Get file size
                size = path_obj.stat().st_size
                size_mb = size / (1024 * 1024)

                # Get last modified time
                mtime = path_obj.stat().st_mtime
                from datetime import datetime
                modified_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

                # Determine log type
                log_type = "Unknown"
                if "auth" in log_path.lower():
                    log_type = "Authentication"
                elif "syslog" in log_path.lower() or "messages" in log_path.lower():
                    log_type = "System"
                elif "kern" in log_path.lower():
                    log_type = "Kernel"
                elif "apache" in log_path.lower() or "httpd" in log_path.lower():
                    log_type = "Apache Web Server"
                elif "nginx" in log_path.lower():
                    log_type = "Nginx Web Server"
                elif "mysql" in log_path.lower():
                    log_type = "MySQL Database"
                elif "postgres" in log_path.lower():
                    log_type = "PostgreSQL Database"
                elif "mail" in log_path.lower():
                    log_type = "Mail Server"
                elif "cron" in log_path.lower():
                    log_type = "Cron Jobs"

                found_logs.append({
                    'path': str(path_obj),
                    'type': log_type,
                    'size_mb': round(size_mb, 2),
                    'modified': modified_time,
                    'readable': os.access(path_obj, os.R_OK)
                })

            except (OSError, PermissionError):
                # Skip files we can't access
                continue

    return found_logs


def display_found_logs(logs: List[Dict[str, str]]) -> None:
    """Display found log files in a formatted way."""
    if not logs:
        print("❌ No system log files found on this system.")
        return

    print(f"\n📋 Found {len(logs)} system log files:")
    print("=" * 80)

    for i, log in enumerate(logs, 1):
        access_icon = "✅" if log['readable'] else "❌"
        print(f"{i:2d}. {access_icon} {log['type']}")
        print(f"    📁 Path: {log['path']}")
        print(f"    📊 Size: {log['size_mb']} MB")
        print(f"    🕒 Modified: {log['modified']}")
        print()


def select_log_files(logs: List[Dict[str, str]]) -> List[str]:
    """Let user select log files from the found list."""
    if not logs:
        return []

    selected_files = []

    while True:
        print("\n🔍 Log file selection options:")
        print("1. Select specific files (enter numbers separated by comma)")
        print("2. Select all readable files")
        print("3. Select by type (auth, system, web, etc.)")
        print("4. Cancel selection")
        print()

        choice = input("Your choice (1-4): ").strip()

        if choice == "1":
            # Manual selection
            indices_input = input("Enter file numbers (e.g., 1,3,5): ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in indices_input.split(',')]
                for idx in indices:
                    if 0 <= idx < len(logs):
                        log = logs[idx]
                        if log['readable']:
                            selected_files.append(log['path'])
                            print(f"✅ Selected: {log['path']}")
                        else:
                            print(f"❌ Skipped (no read permission): {log['path']}")
                    else:
                        print(f"❌ Invalid index: {idx + 1}")
            except ValueError:
                print("❌ Invalid input format")

        elif choice == "2":
            # Select all readable files
            for log in logs:
                if log['readable']:
                    selected_files.append(log['path'])
                    print(f"✅ Selected: {log['path']}")
            break

        elif choice == "3":
            # Select by type
            print("\n📂 Available log types:")
            types = list(set(log['type'] for log in logs))
            for i, log_type in enumerate(types, 1):
                count = sum(1 for log in logs if log['type'] == log_type)
                print(f"{i}. {log_type} ({count} files)")

            type_choice = input("\nSelect type number: ").strip()
            try:
                type_idx = int(type_choice) - 1
                if 0 <= type_idx < len(types):
                    selected_type = types[type_idx]
                    for log in logs:
                        if log['type'] == selected_type and log['readable']:
                            selected_files.append(log['path'])
                            print(f"✅ Selected: {log['path']}")
                    break
                else:
                    print("❌ Invalid type selection")
            except ValueError:
                print("❌ Invalid input")

        elif choice == "4":
            # Cancel
            break

        else:
            print("❌ Invalid choice")

        if selected_files:
            confirm = input(f"\nProceed with {len(selected_files)} selected files? (y/n): ").lower()
            if confirm == 'y':
                break
            else:
                selected_files = []  # Reset selection

    return selected_files