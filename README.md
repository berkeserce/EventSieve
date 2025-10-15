# 🔍 EventSieve - Advanced Log Analysis & Security Intelligence

<div align="center">

![EventSieve Banner](https://img.shields.io/badge/EventSieve-Advanced%20Log%20Analysis-blue?style=for-the-badge&logo=security&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Professional cybersecurity log analysis tool with real-time monitoring and intelligent threat detection**

[📖 Documentation](#-documentation) • [🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [🎯 Examples](#-examples)

</div>

---

## 📋 Table of Contents

- [🔍 Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📖 Documentation](#-documentation)
- [🎯 Examples](#-examples)
- [🔧 Installation](#-installation)
- [📊 Usage](#-usage)
- [🎨 HTML Reports](#-html-reports)
- [👀 Real-time Monitoring](#-real-time-monitoring)
- [🎮 Interactive Mode](#-interactive-mode)
- [🧪 Testing](#-testing)
- [🏗️ Project Structure](#️-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🔍 Overview

**EventSieve** is a cutting-edge cybersecurity tool designed for security professionals, system administrators, and IT teams. It performs intelligent log analysis using regex-based rules to detect suspicious activities, security threats, and anomalous behavior patterns across various log formats.

### 🎯 Key Capabilities

- **🧠 Intelligent Pattern Matching**: Advanced regex rules with severity classification
- **📊 Multi-Format Reporting**: Professional HTML reports with interactive visualizations
- **⚡ Real-Time Monitoring**: Continuous log surveillance with instant alerts
- **🎮 User-Friendly Interface**: Interactive menu system with system log auto-discovery
- **🔧 Highly Configurable**: JSON-based rule engine for custom threat detection
- **📱 Cross-Platform**: Works on Linux, macOS, and Windows environments

---

## ✨ Features

### 🔒 Security Analysis
- ✅ **Authentication Monitoring**: Failed login attempts, brute force detection
- ✅ **System Security**: Root access, privilege escalation, unauthorized commands
- ✅ **Network Security**: Firewall violations, suspicious connections
- ✅ **Malware Detection**: Virus signatures, suspicious file activities
- ✅ **Compliance Monitoring**: GDPR, HIPAA, PCI-DSS rule validation

### 📊 Reporting & Visualization
- ✅ **Interactive HTML Reports**: Modern black-white theme with animations
- ✅ **Statistical Dashboards**: Severity distribution charts and metrics
- ✅ **Detailed Activity Logs**: Line-by-line analysis with pattern matching
- ✅ **Export Capabilities**: TXT and HTML format support
- ✅ **Responsive Design**: Mobile-friendly report viewing

### ⚡ Performance & Monitoring
- ✅ **Real-Time Analysis**: Live log monitoring with configurable intervals
- ✅ **High Performance**: Efficient processing of large log files
- ✅ **Memory Optimized**: Smart caching and resource management
- ✅ **Background Processing**: Non-blocking real-time monitoring

### 🎮 User Experience
- ✅ **Interactive CLI**: Color-coded terminal interface
- ✅ **Auto-Discovery**: Automatic system log detection and categorization
- ✅ **Flexible Configuration**: Command-line and interactive modes
- ✅ **Error Handling**: Comprehensive validation and user feedback

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.6+**
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/berkeserce/EventSieve.git
cd EventSieve

# Install dependencies
pip install -r requirements.txt

# Or manual installation
pip install colorama jinja2
```

### Basic Usage

```bash
# Analyze a log file
python -m src.main -l sample.log -r rules.json

# Generate reports
python -m src.main -l sample.log -r rules.json -o analysis.txt --html-output report.html

# Interactive mode
python -m src.main
```

---

## 📖 Documentation

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--log-file` | `-l` | Path to log file (required) | - |
| `--rules-file` | `-r` | Path to rules JSON file | `rules.json` |
| `--output` | `-o` | TXT report output path | Auto-generated |
| `--html-output` | - | HTML report output path | - |
| `--watch` | - | Enable real-time monitoring | `False` |
| `--interval` | - | Monitoring check interval (seconds) | `1.0` |

### Rules Configuration

The `rules.json` file defines detection patterns:

```json
[
    {
        "pattern": "Failed password|Authentication failure",
        "description": "Failed login attempt detected",
        "severity": "medium"
    },
    {
        "pattern": "sshd.*Invalid user|sshd.*Failed password",
        "description": "SSH authentication failure",
        "severity": "high"
    }
]
```

**Severity Levels:**
- `low` - Informational events
- `medium` - Potential security concerns
- `high` - Significant threats requiring attention
- `critical` - Immediate action required

---

## 🎯 Examples

### Basic Log Analysis
```bash
python -m src.main -l /var/log/auth.log -r rules.json -o security_audit.txt
```

### Full Security Assessment
```bash
python -m src.main \
  -l /var/log/auth.log \
  -r comprehensive_rules.json \
  -o auth_analysis.txt \
  --html-output security_report.html
```

### Real-Time Monitoring
```bash
# Monitor authentication logs
python -m src.main -l /var/log/auth.log -r rules.json --watch --interval 0.5

# Monitor with live HTML reports
python -m src.main \
  -l /var/log/syslog \
  -r rules.json \
  --watch \
  --html-output live_monitoring.html
```

### Interactive Mode
```bash
python -m src.main
# Follow menu prompts for log selection and analysis options
```

---

## 🎨 HTML Reports

EventSieve generates professional HTML reports with modern design:

### ✨ Report Features
- **📈 Statistics Dashboard**: Activity counts and severity distributions
- **📊 Interactive Charts**: Visual representation of threat levels
- **🔍 Detailed Analysis**: Line-by-line suspicious activity breakdown
- **🎨 Modern UI**: Clean black-white theme with subtle animations
- **📱 Responsive**: Optimized for desktop and mobile viewing
- **⚡ Fast Loading**: Optimized HTML with minimal dependencies

### Sample Report Structure
```
├── Header (EventSieve Logo & Timestamp)
├── Statistics Cards (Total, Critical, High, Medium counts)
├── Severity Distribution Chart (Interactive bars)
├── Suspicious Activities List (Filtered by severity)
└── Footer (File info & generation details)
```

### Opening Reports
```bash
# Generate and open HTML report
python -m src.main -l sample.log -r rules.json --html-output analysis.html
# Then open analysis.html in your web browser
```

---

## 👀 Real-Time Monitoring

Monitor log files continuously for immediate threat detection:

### Key Features
- **⚡ Instant Detection**: New log entries analyzed immediately
- **🔔 Live Alerts**: Real-time console notifications
- **📊 Dynamic Reports**: HTML reports update automatically
- **⚙️ Configurable**: Adjustable check intervals
- **💾 Memory Efficient**: Automatic cleanup of old entries

### Monitoring Example
```bash
python -m src.main -l /var/log/auth.log -r rules.json --watch --interval 2.0
```

**Output:**
```
EventSieve - Real-time Log Monitoring Started
Log file: /var/log/auth.log
Rules file: rules.json
Check interval: 2.0 seconds
--------------------------------------------------
262 rules loaded.
Monitoring for new log entries... (Press Ctrl+C to stop)

[14:23:15] New suspicious activities detected:
Line 1250: Failed login attempt (Severity: medium)
   Content: Oct 15 14:23:15 server sshd[1234]: Failed password for user hacker
```

---

## 🎮 Interactive Mode

User-friendly terminal interface with advanced features:

### Main Menu Options
1. **📁 Select Log File** - Manual file selection or auto-discovery
2. **📋 Select Rules File** - Choose detection rule set
3. **▶️ Start Analysis** - Run analysis with current settings
4. **📄 Set TXT Report** - Configure text output
5. **🌐 Generate HTML Report** - Create visual reports
6. **👀 Start Real-time Monitoring** - Live surveillance mode
7. **⚙️ Current Settings** - View configuration

### System Log Auto-Discovery
- **🔍 Automatic Scanning**: Detects common log locations
- **📂 Smart Categorization**: Identifies log types and permissions
- **✅ Validation**: Shows only accessible files
- **🎯 Quick Selection**: Choose from numbered list

**Supported Log Types:**
- Authentication logs (`/var/log/auth.log`, `/var/log/secure`)
- System logs (`/var/log/syslog`, `/var/log/messages`)
- Web server logs (Apache/Nginx access and error logs)
- Database logs (MySQL, PostgreSQL)
- Mail server logs (Postfix, Sendmail)
- Kernel logs (`/var/log/kern.log`)

---

## 🧪 Testing

### Test Commands
```bash
# Basic functionality test
python -m src.main -l sample.log -r rules.json

# Report generation test
python -m src.main -l sample.log -r rules.json -o test_output.txt --html-output test_report.html

# Real-time monitoring test (with sample log)
python -m src.main -l sample.log -r rules.json --watch --interval 5.0

# Interactive mode test
python -m src.main
```

### Sample Output
```
EventSieve - Starting Log Analysis...
Log file: sample.log
Rules file: rules.json
--------------------------------------------------
262 rules loaded.
Total 15 suspicious activities found:

1. Line 1: Failed login attempt (Severity: medium)
   Content: Oct 13 10:15:01 server sshd[1234]: Failed password...
   Pattern: Failed password|Authentication failure

2. Line 2: SSH authentication failure (Severity: high)
   Content: Oct 13 10:15:02 server sshd[1234]: Failed password...
   Pattern: sshd.*Invalid user|sshd.*Failed password
...
✓ HTML report generated: test_report.html
To open in web browser: file:///home/user/EventSieve/test_report.html
```

---

## 🏗️ Project Structure

```
EventSieve/
├── 📁 src/                          # Main source code
│   ├── __init__.py
│   ├── main.py                     # Application entry point
│   ├── 📁 core/                    # Core business logic
│   │   ├── analyzer.py            # Log analysis engine
│   │   ├── rules.py               # Rule loading & validation
│   │   └── watcher.py             # Real-time monitoring
│   ├── 📁 ui/                     # User interface components
│   │   ├── cli.py                 # Command-line interface
│   │   └── interactive.py         # Interactive menu system
│   ├── 📁 reports/                # Report generation
│   │   ├── text_report.py         # TXT report generator
│   │   └── html_report.py         # HTML report generator
│   └── 📁 utils/                  # Utility functions
│       └── system_logs.py         # System log discovery
├── 📄 main.py                      # Legacy entry point
├── 📄 requirements.txt             # Python dependencies
├── 📄 rules.json                   # Security rules configuration
├── 📄 report_template.html         # HTML report template
├── 📄 sample.log                   # Sample log file for testing
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 README.md                    # This file
└── 📁 .github/                     # GitHub configuration
    └── copilot-instructions.md     # AI assistant guidelines
```

### Architecture Benefits
- **🔧 Modular Design**: Clean separation of concerns
- **🧪 Testable**: Each component can be tested independently
- **🔄 Maintainable**: Easy to add new features
- **📚 Readable**: Well-documented code structure

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/EventSieve.git
cd EventSieve

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Development tools

# Run tests
pytest

# Code formatting
black src/
```

### Adding New Rules
1. Edit `rules.json` with new patterns
2. Test with sample logs
3. Update documentation if needed
4. Submit pull request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Permissions
- ✅ **Commercial Use**: Allowed
- ✅ **Modification**: Allowed
- ✅ **Distribution**: Allowed
- ✅ **Private Use**: Allowed
- ⚠️ **Liability**: No warranty provided
- ⚠️ **Trademark**: No trademark usage

---

## � Acknowledgments

- **Security Community**: For inspiration and rule patterns
- **Open Source Libraries**: colorama, jinja2, and Python ecosystem
- **Contributors**: Everyone who helps improve EventSieve

---

<div align="center">

**Made with ❤️ for the cybersecurity community**

[⬆️ Back to Top](#-eventsieve---advanced-log-analysis--security-intelligence)

</div>