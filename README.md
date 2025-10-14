# EventSieve - Rule-Based Log Analysis Tool

EventSieve is a log analysis tool developed for cybersecurity professionals. It reads specified log files and detects suspicious activities according to Regex patterns in JSON format rule files, providing detailed reports.

## Features

- **Rule-Based Analysis**: Log analysis according to regex rules defined in JSON format
- **Flexible Configuration**: Easy configuration for different log formats and rules
- **Detailed Reporting**: Classification of suspicious activities by severity level
- **Multiple Report Formats**: Both TXT and visual HTML reports
- **Command Line Interface**: Argparse-based options for easy usage
- **Interactive Menu**: User-friendly experience with colored terminal menu

## Installation

Python 3.6+ is required.

```bash
# No external dependencies required, only Python standard libraries are used
```

## Usage

### Basic Usage

```bash
python main.py -l sample.log -r rules.json
```

### Modular Usage (Recommended)

```bash
python -m src.main -l sample.log -r rules.json -o report.txt --html-output report.html
```

### All Options

```bash
python -m src.main --log-file /path/to/logfile.log --rules-file /path/to/rules.json --output /path/to/report.txt --html-output /path/to/report.html --watch --interval 2.0
```

### Options

- `-l, --log-file`: Path to the log file to analyze (required)
- `-r, --rules-file`: Path to the rules file (default: rules.json)
- `-o, --output`: Path to save TXT report (optional)
- `--html-output`: Path to save HTML report (optional)
- `--watch`: Enable real-time monitoring mode
- `--interval`: Check interval in seconds for watch mode (default: 1.0)
- `--watch`: Enable real-time monitoring mode
- `--interval`: Check interval in seconds for watch mode (default: 1.0)

## Rules File Format

The `rules.json` file should be in the following format:

```json
[
    {
        "pattern": "regex_pattern",
        "description": "Rule description",
        "severity": "low|medium|high|critical"
    }
]
```

### Example Rules

- `"Failed password|Authentication failure"`: Failed login attempts
- `"sshd.*Invalid user"`: SSH invalid user attempts
- `"brute.*force"`: Brute force attacks
- `"malware|virus"`: Malware detections

## Example Output

```
EventSieve - Starting Log Analysis...
Log file: sample.log
Rules file: rules.json
--------------------------------------------------
10 rules loaded.
Total 15 suspicious activities found:

1. Line 1: Failed login attempt (Severity: medium)
   Content: Oct 13 10:15:01 server sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2
   Pattern: Failed password|Authentication failure|Invalid user

2. Line 2: SSH failed login attempt (Severity: high)
   Content: Oct 13 10:15:02 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
   Pattern: sshd.*Invalid user|sshd.*Failed password
...
```

## HTML Reports

EventSieve can also present analysis results as professional-looking HTML reports. HTML reports include:

- **Statistics Cards**: Total activity count and severity distribution
- **Graphical Display**: Visualization of threat levels with bar charts
- **Detailed List**: Detailed information for each suspicious activity
- **Responsive Design**: Can be viewed on mobile devices
- **Modern Black-Green Theme**: Hacker-themed but professional appearance
- **Interactive Elements**: Hover effects and animations

### HTML Report Example

```bash
python main.py -l sample.log -r rules.json --html-output security_report.html
```

HTML reports can be opened in your web browser using the `file://` protocol. They provide a professional security report appearance with a modern black-green theme.

## Real-time Monitoring

EventSieve supports real-time log monitoring, continuously watching log files for new entries and analyzing them immediately.

### Real-time Monitoring Usage

```bash
# Basic real-time monitoring
python main.py -l /var/log/auth.log -r rules.json --watch

# With custom interval and reports
python main.py -l /var/log/auth.log -r rules.json --watch --interval 0.5 --html-output realtime_report.html

# Stop monitoring with Ctrl+C
```

### Real-time Features

- **Continuous Monitoring**: Automatically detects new log entries
- **Instant Alerts**: Shows suspicious activities as they occur
- **Live Reports**: Updates HTML reports in real-time
- **Configurable Intervals**: Adjust check frequency (default: 1 second)
- **Memory Efficient**: Prevents memory leaks with activity history limits

## Security Notes

- This tool only performs log analysis, it does not take active security measures
- Check file permissions when working with sensitive log files
- Test the performance of regex patterns (especially with large log files)

## License

This project is open source and published under the MIT license.