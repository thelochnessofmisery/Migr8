# Create requirements.txt
requirements_content = '''# Migr8 Framework Requirements
# Install with: pip install -r requirements.txt

requests>=2.25.1
colorama>=0.4.4
validators>=0.18.2
'''

with open("migr8/requirements.txt", 'w') as f:
    f.write(requirements_content)
print("Created: migr8/requirements.txt")

# Create setup.sh script
setup_script = '''#!/bin/bash
# Migr8 Framework Setup Script

echo "========================================="
echo "  Migr8 Framework Setup"
echo "========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[+] Python 3 found"

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

echo "[+] pip found"

# Install dependencies
echo "[*] Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo "[+] Dependencies installed successfully"
else
    echo "[-] Error installing dependencies"
    exit 1
fi

# Make main.py executable
chmod +x main.py

# Create symlink for easy access (optional)
if [ -w /usr/local/bin ]; then
    ln -sf "$(pwd)/main.py" /usr/local/bin/migr8
    echo "[+] Created symlink: /usr/local/bin/migr8"
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Usage examples:"
echo "  python main.py --target http://example.com/upload.php --base http://example.com --mode basic"
echo "  python main.py --base http://example.com --mode bruteforce --payload test.php"
echo ""
echo "For help: python main.py --help"
echo ""
'''

with open("migr8/setup.sh", 'w') as f:
    f.write(setup_script)
print("Created: migr8/setup.sh")

# Create README.md
readme_content = '''# Migr8 - Upload Vulnerability Reconnaissance Framework

A modular Python framework for testing file upload vulnerabilities with multiple bypass techniques and reconnaissance capabilities.

## Features

- **Modular Architecture**: Clean, extensible codebase with specialized modules
- **Multiple Testing Modes**: Basic, ASPX, .htaccess bypass, bruteforce, PDF spoofing, and recursive enumeration
- **Comprehensive Reconnaissance**: File accessibility testing, header analysis, and execution verification
- **Bypass Techniques**: Content-Type spoofing, extension bypasses, .htaccess configuration bypass
- **Concurrent Operations**: Multi-threaded directory and file discovery
- **Wordlist Support**: Configurable wordlists for directory enumeration
- **Color-coded Output**: Clear, organized results with [+], [-], [!] prefixes

## Installation

1. **Clone or extract the framework**:
   ```bash
   cd migr8
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh && ./setup.sh
   ```

   Or install manually:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Upload Testing
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode basic
```

### ASPX-Specific Testing
```bash
python main.py --target http://example.com/upload.aspx --base http://example.com --mode aspx
```

### .htaccess Bypass Testing
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode htaccess
```

### Path Bruteforcing
```bash
python main.py --base http://example.com --mode bruteforce --payload test.php
```

### Content-Type Bypass (PDF Spoofing)
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode pdf_bypass
```

### Recursive Directory Enumeration
```bash
python main.py --base http://example.com --mode recursive --wordlist custom_dirs.txt
```

## Command Line Options

- `--target`: Upload endpoint URL (required for most modes)
- `--base`: Base URL for file accessibility testing (required)
- `--payload`: Path to custom payload file (optional)
- `--mode`: Testing mode (basic, aspx, htaccess, bruteforce, pdf_bypass, recursive)
- `--wordlist`: Path to custom wordlist file (optional)
- `--timeout`: Request timeout in seconds (default: 30)
- `--threads`: Number of concurrent threads (default: 10)
- `--verbose`: Enable verbose output

## Directory Structure

```
migr8/
├── core/                    # Core testing modules
│   ├── upload_tester.py     # File upload testing
│   ├── recon_scanner.py     # File accessibility scanning
│   ├── header_analyser.py   # HTTP header analysis
│   ├── aspx_checker.py      # ASPX-specific testing
│   ├── htaccess_probe.py    # .htaccess bypass testing
│   ├── path_bruteforce.py   # Directory bruteforcing
│   └── contenttype_bypass.py # Content-Type bypass testing
├── utils/                   # Utility modules
│   ├── logger.py           # Color-coded logging
│   └── bypasses.py         # Bypass techniques database
├── payloads/               # Sample payload files
│   ├── test.php           # PHP test payload
│   ├── test.aspx          # ASPX test payload
│   └── sample.txt         # Text test file
├── wordlists/             # Directory wordlists
│   └── common_dirs.txt    # Common upload directories
├── main.py                # CLI entrypoint
├── requirements.txt       # Python dependencies
└── setup.sh              # Installation script
```

## Testing Modes

### 1. Basic Mode
- Tests standard file upload functionality
- Analyzes HTTP headers for security information
- Checks file accessibility and execution

### 2. ASPX Mode
- Specialized testing for ASPX environments
- Multiple upload techniques and content types
- Extension bypass testing
- .NET framework detection

### 3. .htaccess Mode
- Uploads crafted .htaccess files
- Tests companion payload execution
- Multiple .htaccess templates
- Apache server detection

### 4. Bruteforce Mode
- Directory and file discovery
- Multi-threaded enumeration
- Wordlist-based testing
- Execution verification

### 5. PDF Bypass Mode
- Content-Type spoofing attacks
- PHP-as-PDF bypass techniques
- Magic byte manipulation
- Polyglot file testing

### 6. Recursive Mode
- Deep directory enumeration
- Smart path discovery
- Recursive subdirectory testing
- Comprehensive file location mapping

## Security Notice

⚠️ **This tool is for authorized security testing only!**
⚠️ **Only use on systems you own or have explicit permission to test!**
⚠️ **Follow responsible disclosure practices!**

## Future Improvements

- **Concurrency**: Async/await support with connection pooling
- **Timeout Handling**: Per-module configurable timeouts with retry mechanisms
- **Passive Scanning**: Response analysis for vulnerability indicators
- **Enhanced Logging**: Structured JSON logging with SIEM integration capabilities
- **Additional Testing**: XML/XXE uploads, image-based payloads, ZIP file testing

## License

This framework is provided for educational and authorized testing purposes only.

## Contributing

Contributions are welcome! Please follow clean coding practices and add appropriate documentation.
'''

with open("migr8/README.md", 'w') as f:
    f.write(readme_content)
print("Created: migr8/README.md")