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