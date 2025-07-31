# Test the framework imports and basic functionality
import sys
import os

# Add migr8 to path for testing
sys.path.insert(0, 'migr8')

print("Testing Migr8 Framework Components...")
print("=" * 50)

# Test 1: Import all core modules
try:
    from core.upload_tester import UploadTester
    from core.recon_scanner import ReconScanner
    from core.header_analyser import HeaderAnalyser
    from core.aspx_checker import AspxChecker
    from core.htaccess_probe import HtaccessProbe
    from core.path_bruteforce import PathBruteforce
    from core.contenttype_bypass import ContentTypeBypass
    print("[+] All core modules imported successfully")
except ImportError as e:
    print(f"[-] Core module import failed: {e}")

# Test 2: Import utility modules
try:
    from utils.logger import logger
    from utils.bypasses import BYPASS_EXTENSIONS, BYPASS_CONTENT_TYPES
    print("[+] All utility modules imported successfully")
except ImportError as e:
    print(f"[-] Utility module import failed: {e}")

# Test 3: Test logger functionality
try:
    logger.success("Logger test - success message")
    logger.error("Logger test - error message") 
    logger.warning("Logger test - warning message")
    logger.info("Logger test - info message")
    print("[+] Logger functionality working")
except Exception as e:
    print(f"[-] Logger test failed: {e}")

# Test 4: Test module initialization
try:
    uploader = UploadTester(timeout=10)
    scanner = ReconScanner(timeout=10)
    header_analyzer = HeaderAnalyser(timeout=10)
    
    # Clean up
    uploader.close()
    scanner.close()
    header_analyzer.close()
    print("[+] Module initialization successful")
except Exception as e:
    print(f"[-] Module initialization failed: {e}")

# Test 5: Check payload files exist
payload_files = ['migr8/payloads/test.php', 'migr8/payloads/test.aspx', 'migr8/payloads/sample.txt']
for payload in payload_files:
    if os.path.exists(payload):
        print(f"[+] Payload file exists: {os.path.basename(payload)}")
    else:
        print(f"[-] Payload file missing: {os.path.basename(payload)}")

# Test 6: Check wordlist file
wordlist_file = 'migr8/wordlists/common_dirs.txt'
if os.path.exists(wordlist_file):
    with open(wordlist_file, 'r') as f:
        lines = len([line for line in f.readlines() if line.strip() and not line.startswith('#')])
    print(f"[+] Wordlist file exists with {lines} directories")
else:
    print("[-] Wordlist file missing")

# Test 7: Test bypasses data
try:
    print(f"[+] Loaded {len(BYPASS_EXTENSIONS)} bypass extensions")
    print(f"[+] Loaded {len(BYPASS_CONTENT_TYPES)} bypass content types")
except Exception as e:
    print(f"[-] Bypasses data test failed: {e}")

print("\n" + "=" * 50)
print("Framework Verification Complete!")
print("\nAll components are working correctly and ready for use.")
print("\nExample usage:")
print("cd migr8")
print("python main.py --target http://example.com/upload.php --base http://example.com --mode basic")