# Create main.py CLI interface
main_code = '''#!/usr/bin/env python3
"""
Migr8 - Upload Vulnerability Reconnaissance Framework
Main CLI entrypoint

Usage:
    python main.py --target <url> --base <url> --mode <mode> [options]
"""

import sys
import os
import argparse
import validators
from urllib.parse import urlparse

# Add the migr8 package to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.upload_tester import UploadTester
from core.recon_scanner import ReconScanner
from core.header_analyser import HeaderAnalyser
from core.aspx_checker import AspxChecker
from core.htaccess_probe import HtaccessProbe
from core.path_bruteforce import PathBruteforce
from core.contenttype_bypass import ContentTypeBypass
from utils.logger import logger

class Migr8Framework:
    """Main Migr8 framework orchestrator"""
    
    def __init__(self):
        self.banner = """
██████╗ ███╗   ███╗██╗ ██████╗ ██████╗  █████╗ 
██╔═████╗████╗ ████║██║██╔════╝ ██╔══██╗██╔══██╗
▀██╗██╔▀▀██║╚██╗██╔══██║██║  ███╗██████╔╝╚█████╔╝
▄██═▀▀██╗██╔═╝ ╚═══████║██║   ██║██╔══██╗██╔══██╗
██████╔╝██║     ████╔═█║╚██████╔╝██║  ██║╚█████╔╝
╚═════╝ ╚═╝     ╚═══╝  ╚═════╝ ╚═╝  ╚═╝ ╚════╝ 
                                                
    Upload Vulnerability Reconnaissance Framework
             Created by Security Researchers
"""
    
    def run(self):
        """Main entry point"""
        logger.banner("Migr8 Framework")
        print(self.banner)
        
        # Parse arguments
        args = self.parse_arguments()
        
        # Validate arguments
        if not self.validate_arguments(args):
            return 1
        
        # Execute based on mode
        try:
            if args.mode == 'basic':
                return self.mode_basic(args)
            elif args.mode == 'aspx':
                return self.mode_aspx(args)
            elif args.mode == 'htaccess':
                return self.mode_htaccess(args)
            elif args.mode == 'bruteforce':
                return self.mode_bruteforce(args)
            elif args.mode == 'pdf_bypass':
                return self.mode_pdf_bypass(args)
            elif args.mode == 'recursive':
                return self.mode_recursive(args)
            else:
                logger.error(f"Unknown mode: {args.mode}")
                return 1
                
        except KeyboardInterrupt:
            logger.warning("Operation interrupted by user")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return 1
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='Migr8 - Upload Vulnerability Reconnaissance Framework',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Basic upload testing:
    python main.py --target http://example.com/upload.php --base http://example.com --mode basic

  ASPX-specific testing:
    python main.py --target http://example.com/upload.aspx --base http://example.com --mode aspx

  .htaccess bypass testing:
    python main.py --target http://example.com/upload.php --base http://example.com --mode htaccess

  Path bruteforcing:
    python main.py --base http://example.com --mode bruteforce --payload test.php

  Content-type bypass (PDF spoofing):
    python main.py --target http://example.com/upload.php --base http://example.com --mode pdf_bypass

  Recursive enumeration:
    python main.py --base http://example.com --mode recursive --wordlist custom_dirs.txt
            """
        )
        
        parser.add_argument(
            '--target',
            type=str,
            help='Upload endpoint URL (required for most modes)'
        )
        
        parser.add_argument(
            '--base',
            type=str,
            required=True,
            help='Base URL for file accessibility testing'
        )
        
        parser.add_argument(
            '--payload',
            type=str,
            help='Path to payload file to upload (optional, defaults to built-in payloads)'
        )
        
        parser.add_argument(
            '--mode',
            type=str,
            required=True,
            choices=['basic', 'aspx', 'htaccess', 'bruteforce', 'pdf_bypass', 'recursive'],
            help='Testing mode to execute'
        )
        
        parser.add_argument(
            '--wordlist',
            type=str,
            help='Path to custom wordlist file for directory enumeration'
        )
        
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Request timeout in seconds (default: 30)'
        )
        
        parser.add_argument(
            '--threads',
            type=int,
            default=10,
            help='Number of threads for concurrent operations (default: 10)'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        
        return parser.parse_args()
    
    def validate_arguments(self, args):
        """Validate command line arguments"""
        # Validate base URL
        if not validators.url(args.base):
            logger.error(f"Invalid base URL: {args.base}")
            return False
        
        # Validate target URL if provided
        if args.target and not validators.url(args.target):
            logger.error(f"Invalid target URL: {args.target}")
            return False
        
        # Check if target is required for the mode
        target_required_modes = ['basic', 'aspx', 'htaccess', 'pdf_bypass']
        if args.mode in target_required_modes and not args.target:
            logger.error(f"--target is required for mode: {args.mode}")
            return False
        
        # Validate payload file if provided
        if args.payload and not os.path.exists(args.payload):
            logger.error(f"Payload file not found: {args.payload}")
            return False
        
        # Validate wordlist file if provided
        if args.wordlist and not os.path.exists(args.wordlist):
            logger.error(f"Wordlist file not found: {args.wordlist}")
            return False
        
        return True
    
    def mode_basic(self, args):
        """Execute basic upload testing mode"""
        logger.section("Basic Upload Testing")
        
        # Determine payload file
        payload_file = self._get_payload_file(args.payload, 'php')
        if not payload_file:
            return 1
        
        # Initialize modules
        uploader = UploadTester(timeout=args.timeout)
        scanner = ReconScanner(timeout=args.timeout)
        header_analyzer = HeaderAnalyser(timeout=args.timeout)
        
        try:
            # Step 1: Analyze headers
            logger.info("Step 1: Analyzing target headers")
            header_results = header_analyzer.analyze_headers(args.target)
            if header_results:
                self._display_header_summary(header_results)
            
            # Step 2: Test upload
            logger.info("Step 2: Testing file upload")
            upload_result = uploader.test_upload(args.target, payload_file)
            if not upload_result:
                logger.error("Upload test failed")
                return 1
            
            # Step 3: Test accessibility and execution
            if upload_result['success']:
                logger.info("Step 3: Testing file accessibility and execution")
                filename = upload_result['filename']
                recon_result = scanner.check_file_accessibility(args.base, filename)
                
                if recon_result['total_found'] > 0:
                    logger.success(f"File accessible at {recon_result['total_found']} location(s)")
                    
                    # Test execution for accessible files
                    for url_info in recon_result['accessible_urls']:
                        if url_info['executed']:
                            logger.success(f"Code execution confirmed: {url_info['url']}")
                else:
                    logger.warning("Uploaded file not accessible via common paths")
            
            logger.success("Basic upload testing complete")
            return 0
            
        finally:
            uploader.close()
            scanner.close()
            header_analyzer.close()
    
    def mode_aspx(self, args):
        """Execute ASPX-specific testing mode"""
        logger.section("ASPX Upload Testing")
        
        # Determine payload file
        payload_file = self._get_payload_file(args.payload, 'aspx')
        if not payload_file:
            return 1
        
        # Initialize modules
        aspx_checker = AspxChecker(timeout=args.timeout)
        scanner = ReconScanner(timeout=args.timeout)
        
        try:
            # Step 1: Test ASPX upload
            logger.info("Step 1: Testing ASPX upload with multiple techniques")
            upload_result = aspx_checker.test_aspx_upload(args.target, payload_file)
            if not upload_result:
                logger.error("ASPX upload test failed")
                return 1
            
            # Step 2: Test ASPX execution
            if upload_result['successful_uploads']:
                logger.info("Step 2: Testing ASPX execution")
                for upload in upload_result['successful_uploads']:
                    filename = upload['filename']
                    execution_result = aspx_checker.test_aspx_execution(args.base, filename)
                    
                    if execution_result['executed_urls']:
                        logger.success(f"ASPX execution confirmed for {filename}")
                        for exec_info in execution_result['executed_urls']:
                            logger.success(f"Execution URL: {exec_info['url']}")
            
            # Step 3: Test extension bypasses
            logger.info("Step 3: Testing ASPX extension bypasses")
            extension_result = aspx_checker.test_aspx_extensions(args.target, payload_file)
            if extension_result and extension_result['successful_bypasses']:
                logger.success(f"{extension_result['bypass_count']} extension bypasses successful")
            
            logger.success("ASPX testing complete")
            return 0
            
        finally:
            aspx_checker.close()
            scanner.close()
    
    def mode_htaccess(self, args):
        """Execute .htaccess bypass testing mode"""
        logger.section(".htaccess Bypass Testing")
        
        # Initialize module
        htaccess_probe = HtaccessProbe(timeout=args.timeout)
        
        try:
            # Execute comprehensive .htaccess testing
            logger.info("Starting comprehensive .htaccess bypass testing")
            results = htaccess_probe.comprehensive_htaccess_test(args.target, args.base)
            
            if results['summary']['successful_bypasses'] > 0:
                logger.success(f".htaccess bypass successful! {results['summary']['successful_bypasses']} bypasses found")
                
                # Display successful bypasses
                for bypass in results['bypass_test']['successful_bypasses']:
                    logger.success(f"Bypass URL: {bypass['execution_url']}")
                    logger.info(f"Method: {bypass['method']}")
            else:
                logger.warning("No .htaccess bypasses successful")
            
            logger.success(".htaccess testing complete")
            return 0
            
        finally:
            htaccess_probe.close()
    
    def mode_bruteforce(self, args):
        """Execute path bruteforce mode"""
        logger.section("Path Bruteforce")
        
        # Initialize module
        bruteforcer = PathBruteforce(timeout=args.timeout, max_threads=args.threads)
        
        try:
            if args.payload:
                # File-specific bruteforce
                logger.info(f"Bruteforcing paths for file: {os.path.basename(args.payload)}")
                filenames = [os.path.basename(args.payload)]
                results = bruteforcer.bruteforce_files(args.base, filenames, args.wordlist)
            else:
                # Directory bruteforce
                logger.info("Bruteforcing directories")
                results = bruteforcer.bruteforce_directories(args.base, args.wordlist, recursive=False)
            
            if results:
                if 'found_files' in results and results['found_files']:
                    logger.success(f"Found {len(results['found_files'])} files")
                    for file_info in results['found_files']:
                        status = " (executed)" if file_info['executed'] else ""
                        logger.success(f"File: {file_info['url']}{status}")
                
                if 'found_directories' in results and results['found_directories']:
                    logger.success(f"Found {len(results['found_directories'])} directories")
                    for dir_info in results['found_directories']:
                        logger.success(f"Directory: {dir_info['url']}")
            
            logger.success("Path bruteforce complete")
            return 0
            
        finally:
            bruteforcer.close()
    
    def mode_pdf_bypass(self, args):
        """Execute PDF Content-Type bypass mode"""
        logger.section("PDF Content-Type Bypass")
        
        # Determine payload file
        payload_file = self._get_payload_file(args.payload, 'php')
        if not payload_file:
            return 1
        
        # Initialize module
        bypass_tester = ContentTypeBypass(timeout=args.timeout)
        
        try:
            # Execute comprehensive bypass testing
            logger.info("Starting comprehensive Content-Type bypass testing")
            results = bypass_tester.comprehensive_bypass_test(args.target, args.base, payload_file)
            
            summary = results['summary']
            if summary['total_successful_bypasses'] > 0:
                logger.success(f"Content-Type bypass successful! {summary['total_successful_bypasses']} bypasses found")
                
                if summary['total_executions_confirmed'] > 0:
                    logger.success(f"Code execution confirmed: {summary['total_executions_confirmed']} files")
            else:
                logger.warning("No Content-Type bypasses successful")
            
            logger.success("PDF bypass testing complete")
            return 0
            
        finally:
            bypass_tester.close()
    
    def mode_recursive(self, args):
        """Execute recursive enumeration mode"""
        logger.section("Recursive Directory Enumeration")
        
        # Initialize module
        bruteforcer = PathBruteforce(timeout=args.timeout, max_threads=args.threads)
        
        try:
            # Determine files to search for
            filenames = []
            if args.payload:
                filenames.append(os.path.basename(args.payload))
            else:
                # Default files to search for
                filenames = ['test.php', 'test.aspx', 'shell.php', 'cmd.php', 'upload.php']
            
            # Execute smart enumeration
            logger.info("Starting recursive enumeration with smart discovery")
            results = bruteforcer.smart_enumeration(args.base, filenames, args.wordlist)
            
            if results and results['summary']['total_accessible_resources'] > 0:
                summary = results['summary']
                logger.success(f"Recursive enumeration complete:")
                logger.success(f"  Directories found: {summary['directories_found']}")
                logger.success(f"  Files found: {summary['files_found']}")
                logger.success(f"  Total resources: {summary['total_accessible_resources']}")
            else:
                logger.warning("No accessible resources found")
            
            logger.success("Recursive enumeration complete")
            return 0
            
        finally:
            bruteforcer.close()
    
    def _get_payload_file(self, payload_arg, default_type):
        """Get payload file path, using default if not specified"""
        if payload_arg:
            return payload_arg
        
        # Use built-in payload
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if default_type == 'php':
            default_payload = os.path.join(script_dir, 'payloads', 'test.php')
        elif default_type == 'aspx':
            default_payload = os.path.join(script_dir, 'payloads', 'test.aspx')
        else:
            default_payload = os.path.join(script_dir, 'payloads', 'sample.txt')
        
        if os.path.exists(default_payload):
            logger.info(f"Using default payload: {default_payload}")
            return default_payload
        else:
            logger.error(f"Default payload not found: {default_payload}")
            return None
    
    def _display_header_summary(self, header_results):
        """Display header analysis summary"""
        server_info = header_results['server_info']
        if server_info['web_server']:
            logger.info(f"Web Server: {server_info['web_server']}")
        if server_info['language']:
            logger.info(f"Language: {server_info['language']}")
        
        vuln_count = len(header_results['vulnerabilities'])
        if vuln_count > 0:
            logger.warning(f"Security issues found: {vuln_count}")
        else:
            logger.success("No obvious security issues in headers")

def main():
    """Main entry point"""
    framework = Migr8Framework()
    return framework.run()

if __name__ == '__main__':
    sys.exit(main())
'''

with open("migr8/main.py", 'w') as f:
    f.write(main_code)
print("Created: migr8/main.py")