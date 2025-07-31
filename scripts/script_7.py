# Create recon_scanner.py core module
recon_scanner_code = '''"""
Reconnaissance Scanner Module for Migr8 Framework
Checks reachability and execution of uploaded files
"""

import requests
import time
from urllib.parse import urljoin, urlparse
from ..utils.logger import logger
from ..utils.bypasses import USER_AGENTS
import random

class ReconScanner:
    """Scan for uploaded files and test their accessibility"""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
    
    def check_file_accessibility(self, base_url, filename, common_paths=None):
        """
        Check if uploaded file is accessible via common paths
        
        Args:
            base_url (str): Base URL to check
            filename (str): Name of uploaded file
            common_paths (list): List of paths to check
            
        Returns:
            dict: Accessibility results
        """
        if not common_paths:
            common_paths = [
                'uploads/', 'upload/', 'files/', 'file/', 'attachments/',
                'media/', 'images/', 'temp/', 'tmp/', ''
            ]
        
        logger.info(f"Checking accessibility for: {filename}")
        accessible_urls = []
        
        for path in common_paths:
            test_url = urljoin(base_url.rstrip('/') + '/', path + filename)
            
            try:
                response = self.session.get(test_url, timeout=self.timeout)
                
                result = {
                    'url': test_url,
                    'status_code': response.status_code,
                    'content_length': len(response.content),
                    'content_type': response.headers.get('content-type', ''),
                    'accessible': response.status_code == 200,
                    'executed': self._check_execution(response, filename)
                }
                
                if result['accessible']:
                    logger.success(f"File accessible: {test_url}")
                    accessible_urls.append(result)
                    
                    # Check if file executed (for PHP, ASPX, etc.)
                    if result['executed']:
                        logger.success(f"File executed successfully: {test_url}")
                
            except requests.exceptions.RequestException as e:
                logger.debug(f"Request failed for {test_url}: {str(e)}")
                continue
        
        if not accessible_urls:
            logger.error(f"File not accessible: {filename}")
        
        return {
            'filename': filename,
            'accessible_urls': accessible_urls,
            'total_found': len(accessible_urls)
        }
    
    def verify_execution(self, url):
        """
        Verify if a file at given URL executes server-side code
        
        Args:
            url (str): URL to check
            
        Returns:
            dict: Execution verification results
        """
        logger.info(f"Verifying execution: {url}")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'response_length': len(response.content),
                'executed': self._check_execution(response, url),
                'response_preview': response.text[:200]
            }
            
            if result['executed']:
                logger.success(f"Code execution confirmed: {url}")
            else:
                logger.warning(f"No code execution detected: {url}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to verify execution: {str(e)}")
            return None
    
    def scan_multiple_files(self, base_url, filenames, common_paths=None):
        """
        Scan accessibility for multiple files
        
        Args:
            base_url (str): Base URL to check
            filenames (list): List of filenames to check
            common_paths (list): List of paths to check
            
        Returns:
            list: Results for all files
        """
        results = []
        
        logger.info(f"Scanning {len(filenames)} files for accessibility")
        
        for filename in filenames:
            result = self.check_file_accessibility(base_url, filename, common_paths)
            if result:
                results.append(result)
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
        
        accessible_files = [r for r in results if r['total_found'] > 0]
        logger.info(f"Accessibility scan complete: {len(accessible_files)}/{len(filenames)} files found")
        
        return results
    
    def deep_reconnaissance(self, base_url, filename):
        """
        Perform deep reconnaissance on uploaded file
        
        Args:
            base_url (str): Base URL
            filename (str): Uploaded filename
            
        Returns:
            dict: Comprehensive reconnaissance results
        """
        logger.info(f"Starting deep reconnaissance: {filename}")
        
        # Extended path list for deep scan
        extended_paths = [
            '', 'uploads/', 'upload/', 'files/', 'file/', 'attachments/',
            'media/', 'images/', 'temp/', 'tmp/', 'data/', 'assets/',
            'wp-content/uploads/', 'admin/uploads/', 'public/uploads/',
            'var/uploads/', 'htdocs/uploads/', 'public_html/uploads/',
            'uploads/files/', 'files/uploads/', 'media/uploads/',
            'user/uploads/', 'users/uploads/', 'profile/uploads/'
        ]
        
        # Check basic accessibility
        access_result = self.check_file_accessibility(base_url, filename, extended_paths)
        
        reconnaissance_data = {
            'filename': filename,
            'accessibility': access_result,
            'execution_tests': [],
            'security_headers': {},
            'fingerprinting': {}
        }
        
        # Test execution for accessible URLs
        for url_info in access_result['accessible_urls']:
            if url_info['accessible']:
                exec_result = self.verify_execution(url_info['url'])
                if exec_result:
                    reconnaissance_data['execution_tests'].append(exec_result)
                
                # Check security headers
                headers = self._analyze_security_headers(url_info['url'])
                reconnaissance_data['security_headers'][url_info['url']] = headers
        
        return reconnaissance_data
    
    def _check_execution(self, response, identifier):
        """Check if response indicates server-side code execution"""
        if response.status_code != 200:
            return False
            
        content = response.text.lower()
        content_type = response.headers.get('content-type', '').lower()
        
        # PHP execution indicators
        php_indicators = [
            'php version', 'php upload test', 'server_software',
            '<!-- migr8 php test payload -->', 'upload test successful'
        ]
        
        # ASPX execution indicators
        aspx_indicators = [
            'aspx upload test', '.net framework', 'server variables',
            'migr8 aspx test payload', 'runat="server"'
        ]
        
        # Generic execution indicators
        execution_indicators = [
            'current time:', 'upload directory:', 'system:',
            'server:', 'framework:', 'operating system:'
        ]
        
        # Check for indicators
        if any(indicator in content for indicator in php_indicators + aspx_indicators + execution_indicators):
            return True
            
        # Check if it's executed code vs. raw file content
        if content_type.startswith('text/html') and 'migr8' in content:
            return True
            
        return False
    
    def _analyze_security_headers(self, url):
        """Analyze security-related HTTP headers"""
        try:
            response = self.session.head(url, timeout=self.timeout)
            headers = response.headers
            
            security_headers = {
                'x-frame-options': headers.get('x-frame-options'),
                'x-content-type-options': headers.get('x-content-type-options'),
                'x-xss-protection': headers.get('x-xss-protection'),
                'content-security-policy': headers.get('content-security-policy'),
                'strict-transport-security': headers.get('strict-transport-security'),
                'server': headers.get('server'),
                'x-powered-by': headers.get('x-powered-by')
            }
            
            return {k: v for k, v in security_headers.items() if v is not None}
            
        except Exception as e:
            logger.debug(f"Could not analyze headers for {url}: {str(e)}")
            return {}
    
    def close(self):
        """Close the session"""
        self.session.close()
'''

with open("migr8/core/recon_scanner.py", 'w') as f:
    f.write(recon_scanner_code)
print("Created: migr8/core/recon_scanner.py")