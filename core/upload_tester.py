"""
Upload Tester Module for Migr8 Framework
Handles uploading arbitrary files to target endpoints and analyzing responses
"""

import requests
import os
import time
from urllib.parse import urljoin
from utils.logger import logger
from utils.bypasses import UPLOAD_FIELD_NAMES, USER_AGENTS, BYPASS_EXTENSIONS
import random

class UploadTester:
    """Test file uploads to target endpoints"""

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })

    def generate_unique_filename(self, original_filename):
        """Generate unique filename with timestamp"""
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(original_filename)
        return f"{name}_{timestamp}{ext}"

    def test_upload(self, target_url, file_path, content_type=None, field_name=None):
        """
        Upload file to target URL and return response details

        Args:
            target_url (str): Upload endpoint URL
            file_path (str): Path to file to upload
            content_type (str): Custom Content-Type header
            field_name (str): Form field name for upload

        Returns:
            dict: Upload result details
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        # Generate unique filename
        original_filename = os.path.basename(file_path)
        unique_filename = self.generate_unique_filename(original_filename)

        logger.info(f"Testing upload: {unique_filename} -> {target_url}")

        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Determine field name
            if not field_name:
                field_name = self._detect_upload_field(target_url)

            # Prepare files for upload
            files = {
                field_name: (unique_filename, file_content, content_type)
            }

            # Additional form data
            data = {
                'submit': 'Upload',
                'action': 'upload',
                'MAX_FILE_SIZE': '10485760'  # 10MB
            }

            # Make upload request
            response = self.session.post(
                target_url,
                files=files,
                data=data,
                timeout=self.timeout,
                allow_redirects=True
            )

            result = {
                'filename': unique_filename,
                'original_filename': original_filename,
                'status_code': response.status_code,
                'response_length': len(response.content),
                'content_type': response.headers.get('content-type', ''),
                'location': response.headers.get('location', ''),
                'response_text': response.text[:500],  # First 500 chars
                'success': self._analyze_upload_success(response),
                'field_name': field_name
            }

            if result['success']:
                logger.success(f"Upload successful: {unique_filename} (Status: {response.status_code})")
            else:
                logger.error(f"Upload failed: {unique_filename} (Status: {response.status_code})")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Upload request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            return None

    def test_multiple_extensions(self, target_url, base_file_path, extensions=None):
        """
        Test upload with multiple file extensions

        Args:
            target_url (str): Upload endpoint URL
            base_file_path (str): Base file to modify extensions
            extensions (list): List of extensions to test

        Returns:
            list: Results for each extension tested
        """
        if not extensions:
            extensions = BYPASS_EXTENSIONS[:10]  # Test first 10 extensions

        results = []
        base_name = os.path.splitext(base_file_path)[0]

        logger.info(f"Testing {len(extensions)} extensions for upload bypass")

        for ext in extensions:
            # Create temporary file with new extension
            temp_file = f"{base_name}{ext}"

            try:
                # Copy original file content
                with open(base_file_path, 'rb') as src:
                    content = src.read()

                with open(temp_file, 'wb') as dst:
                    dst.write(content)

                # Test upload
                result = self.test_upload(target_url, temp_file)
                if result:
                    result['tested_extension'] = ext
                    results.append(result)

                # Cleanup
                if os.path.exists(temp_file):
                    os.remove(temp_file)

            except Exception as e:
                logger.error(f"Error testing extension {ext}: {str(e)}")
                continue

        successful_uploads = [r for r in results if r.get('success')]
        logger.info(f"Extension bypass test complete: {len(successful_uploads)}/{len(extensions)} successful")

        return results

    def _detect_upload_field(self, target_url):
        """Try to detect the correct upload field name"""
        try:
            response = self.session.get(target_url, timeout=self.timeout)
            content = response.text.lower()

            # Look for common field names in HTML
            for field_name in UPLOAD_FIELD_NAMES:
                if f'name="{field_name}"' in content or f"name='{field_name}'" in content:
                    logger.info(f"Detected upload field: {field_name}")
                    return field_name

        except Exception as e:
            logger.debug(f"Could not detect upload field: {str(e)}")

        # Default to most common field name
        return 'file'

    def _analyze_upload_success(self, response):
        """Analyze response to determine if upload was successful"""
        status_code = response.status_code
        content = response.text.lower()

        # Success indicators
        success_indicators = [
            'upload successful', 'file uploaded', 'upload complete',
            'successfully uploaded', 'file saved', 'upload ok'
        ]

        # Error indicators
        error_indicators = [
            'upload failed', 'error', 'invalid file', 'not allowed',
            'forbidden', 'access denied', 'file type not supported'
        ]

        # Check status code
        if status_code in [200, 201, 302]:
            # Check content for success/error messages
            has_success = any(indicator in content for indicator in success_indicators)
            has_error = any(indicator in content for indicator in error_indicators)

            if has_success and not has_error:
                return True
            elif not has_error:  # No explicit error, assume success
                return True

        return False

    def close(self):
        """Close the session"""
        self.session.close()
