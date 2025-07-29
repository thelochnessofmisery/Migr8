# Migr8 - Upload Vulnerability Reconnaissance Framework

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Migr8** is a comprehensive modular Python framework designed for testing file upload vulnerabilities in web applications. It provides specialized tools for reconnaissance, bypass techniques, and security assessment of upload endpoints.

## ⚠️ **SECURITY NOTICE**

> **This tool is for authorized security testing only!**  
> **Only use on systems you own or have explicit permission to test!**  
> **Follow responsible disclosure practices!**

## 🚀 Features

### Core Modules
- **🎯 Upload Tester**: Upload arbitrary files to target endpoints with HTTP status analysis
- **🔍 Recon Scanner**: Check reachability and execution of uploaded files
- **🔧 Header Analyser**: Comprehensive HTTP header security analysis
- **💻 ASPX Checker**: Specialized testing for ASPX environments
- **⚙️ Htaccess Probe**: .htaccess bypass techniques with companion payload testing
- **📂 Path Bruteforce**: Wordlist-based directory enumeration with multi-threading
- **📄 Content-Type Bypass**: PDF spoofing and MIME type manipulation

### Advanced Capabilities
- ✅ **61 Bypass Extensions** for various file type restrictions
- ✅ **31 Content-Type** spoofing techniques
- ✅ **Multi-threaded** directory bruteforcing
- ✅ **Timestamped payloads** for unique file generation
- ✅ **Session management** with custom headers
- ✅ **Magic byte manipulation** for polyglot files
- ✅ **Execution verification** through response analysis

## 📁 Directory Structure

```
migr8/
├── README.md                      # This documentation
├── main.py                        # CLI entrypoint
├── requirements.txt               # Python dependencies
├── setup.sh                      # Installation script
├── core/                          # Core modules
│   ├── __init__.py
│   ├── upload_tester.py          # File upload testing
│   ├── recon_scanner.py          # File accessibility testing
│   ├── header_analyser.py        # HTTP header analysis
│   ├── aspx_checker.py           # ASPX specialized testing
│   ├── htaccess_probe.py         # .htaccess bypass techniques
│   ├── path_bruteforce.py        # Directory enumeration
│   └── contenttype_bypass.py     # Content-Type spoofing
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── logger.py                 # Color-coded logging
│   └── bypasses.py               # Bypass techniques database
├── payloads/                     # Sample payloads
│   ├── test.php                  # PHP reconnaissance payload
│   ├── test.aspx                 # ASPX reconnaissance payload
│   └── sample.txt                # Plain text test file
└── wordlists/                    # Directory wordlists
    └── common_dirs.txt           # 107 common upload directories
```

## 🔧 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Quick Setup

```bash
# Clone or download the framework
cd migr8

# Install dependencies
pip install -r requirements.txt

# Optional: Run setup script
chmod +x setup.sh && ./setup.sh

# Verify installation
python main.py --help
```

### Dependencies
- `requests` - HTTP library for web requests
- `colorama` - Cross-platform colored terminal text

## 📖 Usage

### Command Line Interface

```bash
python main.py [OPTIONS]
```

### Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `--target` | Upload endpoint URL | Varies* | `http://example.com/upload.php` |
| `--base` | Base URL for file accessibility | Varies* | `http://example.com` |
| `--payload` | Custom payload file path | No | `payloads/test.php` |
| `--mode` | Testing mode | Yes | `basic`, `aspx`, `htaccess`, etc. |
| `--wordlist` | Custom wordlist file path | No | `custom_dirs.txt` |

*Required parameters vary by testing mode

### Testing Modes

#### 1. Basic Mode
Standard upload testing with bypass techniques
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode basic
```

#### 2. ASPX Mode
Specialized testing for ASP.NET applications
```bash
python main.py --target http://example.com/upload.aspx --base http://example.com --mode aspx
```

#### 3. Htaccess Mode
.htaccess configuration bypass testing
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode htaccess
```

#### 4. Bruteforce Mode
Directory enumeration using wordlists
```bash
python main.py --base http://example.com --mode bruteforce --payload test.php
```

#### 5. PDF Bypass Mode
Content-Type spoofing with PDF MIME type
```bash
python main.py --target http://example.com/upload.php --base http://example.com --mode pdf_bypass
```

#### 6. Recursive Mode
Advanced directory enumeration with custom wordlists
```bash
python main.py --base http://example.com --mode recursive --wordlist wordlists/common_dirs.txt
```

## 🛠️ Technical Details

### Bypass Techniques Implemented

#### File Extension Bypasses
- Double extensions (`.php.jpg`, `.asp.gif`)
- Case variations (`.PHP`, `.AsP`)
- Null byte injection (`.php%00.jpg`)
- Special characters (`.php.`, `.php::$DATA`)
- Unicode variations and encoding bypasses

#### Content-Type Bypasses
- MIME type spoofing (`application/pdf`, `image/jpeg`)
- Magic byte manipulation
- Polyglot file generation
- Content-Type header modification

#### Specialized Tests
- **ASPX**: .NET framework detection, web.config manipulation
- **.htaccess**: Apache configuration bypass, extension whitelisting
- **Directory Discovery**: Multi-threaded enumeration, recursive scanning

### Logging System

The framework uses color-coded logging with clear prefixes:
- `[+]` Success messages (Green)
- `[-]` Error messages (Red)  
- `[!]` Warning messages (Yellow)
- `[*]` Information messages (Blue)

### Session Management
- Custom User-Agent rotation
- Session persistence across requests
- Proxy support for advanced testing
- Configurable timeout handling

## 📊 Sample Output

```
[*] Starting Migr8 v1.0.0 - Upload Vulnerability Framework
[*] Target: http://example.com/upload.php
[*] Mode: basic

[+] Upload successful: test.php (200 OK)
[*] Testing file accessibility...
[+] File accessible at: /uploads/test_1640995200.php
[+] Server-side execution confirmed!
[!] Potential vulnerability detected

[*] Testing bypass extensions...
[+] Bypass successful: test.php.jpg (200 OK)
[-] Access denied: test.phtml (403 Forbidden)

[*] Scan completed - 2/5 bypasses successful
```

## 🎯 Wordlist Configuration

### Default Wordlist
The framework includes `wordlists/common_dirs.txt` with 107 common upload directories:
- `/uploads/`, `/files/`, `/media/`
- `/images/`, `/documents/`, `/attachments/`
- Framework-specific paths (WordPress, Drupal, etc.)

### Custom Wordlists
Use the `--wordlist` parameter to specify custom directories:
```bash
python main.py --base http://example.com --mode bruteforce --wordlist /path/to/custom.txt
```

## 🔮 Future Improvements

### Planned Enhancements
- **Concurrency**: Async/await support with connection pooling
- **Timeout Handling**: Per-module configurable timeouts with retry mechanisms
- **Passive Scanning**: Response analysis for vulnerability indicators
- **Enhanced Logging**: Structured JSON logging with SIEM integration
- **Database Support**: Results storage in SQLite/PostgreSQL
- **Web Interface**: GUI dashboard for easier management
- **Plugin System**: Custom module loading architecture

### Contributing
Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

#### ImportError: No module named 'requests'
```bash
pip install -r requirements.txt
```

#### Permission Denied Errors
```bash
chmod +x setup.sh
```

#### Timeout Issues
Increase timeout values in module configurations or use proxy settings for slower targets.

## 📚 Documentation

### Module Documentation
Each core module includes detailed docstrings and inline comments. Use Python's help system:
```python
import migr8.core.upload_tester
help(migr8.core.upload_tester)
```

### Security Best Practices
- Always obtain proper authorization before testing
- Use test environments when possible
- Document findings responsibly
- Follow coordinated disclosure processes
- Keep the framework updated

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Acknowledgments

- SecLists project for wordlist inspiration
- OWASP for security testing methodologies
- Python requests and colorama maintainers

## 📞 Support

For questions, issues, or feature requests:
- Create an issue in the project repository
- Check existing documentation
- Review troubleshooting section

---

**Happy Testing! 🚀**

*Remember: Use responsibly and only on authorized targets.*
