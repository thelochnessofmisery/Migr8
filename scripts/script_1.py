# Create the logger.py utility
logger_code = '''"""
Logger utility for Migr8 framework
Provides color-coded console output with clear prefixes
"""

import colorama
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

class Logger:
    """Color-coded logger with standardized prefixes"""
    
    def __init__(self):
        self.colors = {
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'info': Fore.CYAN,
            'debug': Fore.MAGENTA
        }
    
    def success(self, message):
        """Log success message with [+] prefix"""
        print(f"{self.colors['success']}[+]{Style.RESET_ALL} {message}")
    
    def error(self, message):
        """Log error message with [-] prefix"""
        print(f"{self.colors['error']}[-]{Style.RESET_ALL} {message}")
    
    def warning(self, message):
        """Log warning message with [!] prefix"""
        print(f"{self.colors['warning']}[!]{Style.RESET_ALL} {message}")
    
    def info(self, message):
        """Log info message with [*] prefix"""
        print(f"{self.colors['info']}[*]{Style.RESET_ALL} {message}")
    
    def debug(self, message):
        """Log debug message with [#] prefix"""
        print(f"{self.colors['debug']}[#]{Style.RESET_ALL} {message}")
    
    def banner(self, title):
        """Display banner with title"""
        banner_line = "=" * 60
        print(f"{Fore.CYAN}{banner_line}")
        print(f"  {title}")
        print(f"{banner_line}{Style.RESET_ALL}")
    
    def section(self, title):
        """Display section header"""
        print(f"\\n{Fore.YELLOW}{'='*20} {title} {'='*20}{Style.RESET_ALL}")

# Global logger instance
logger = Logger()
'''

with open("migr8/utils/logger.py", 'w') as f:
    f.write(logger_code)
print("Created: migr8/utils/logger.py")