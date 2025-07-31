#!/bin/bash
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
