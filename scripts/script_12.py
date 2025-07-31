# Create path_bruteforce.py core module
path_bruteforce_code = '''"""
Path Bruteforce Module for Migr8 Framework
Perform recursive directory brute forcing using configurable wordlist files
"""

import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from ..utils.logger import logger
from ..utils.bypasses import USER_AGENTS
import random
import time

class PathBruteforce:
    """Brute force common upload directories using wordlist files"""
    
    def __init__(self, timeout=30, max_threads=10):
        self.timeout = timeout
        self.max_threads = max_threads
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
        self.found_directories = []
        self.found_files = []
        self.lock = threading.Lock()
    
    def bruteforce_directories(self, base_url, wordlist_file=None, recursive=False):
        """
        Brute force directories using wordlist file
        
        Args:
            base_url (str): Base URL to test
            wordlist_file (str): Path to wordlist file (optional)
            recursive (bool): Perform recursive enumeration
            
        Returns:
            dict: Directory bruteforce results
        """
        logger.info(f"Starting directory bruteforce: {base_url}")
        
        # Load wordlist
        directories = self._load_wordlist(wordlist_file)
        if not directories:
            logger.error("No directories loaded from wordlist")
            return None
        
        logger.info(f"Loaded {len(directories)} directories from wordlist")
        
        # Initialize results
        results = {
            'base_url': base_url,
            'wordlist_file': wordlist_file or 'default',
            'directories_tested': len(directories),
            'found_directories': [],
            'found_files': [],
            'accessible_paths': [],
            'recursive_results': []
        }
        
        # Perform bruteforce
        found_dirs = self._bruteforce_paths(base_url, directories, 'directory')
        results['found_directories'] = found_dirs
        results['accessible_paths'].extend(found_dirs)
        
        # Recursive enumeration if requested
        if recursive and found_dirs:
            logger.info(f"Starting recursive enumeration on {len(found_dirs)} found directories")
            for found_dir in found_dirs:
                recursive_result = self._recursive_enumerate(found_dir['url'], directories)
                if recursive_result:
                    results['recursive_results'].append(recursive_result)
                    results['accessible_paths'].extend(recursive_result['found_paths'])
        
        # Summary
        total_found = len(results['accessible_paths'])
        logger.info(f"Directory bruteforce complete: {total_found} accessible paths found")
        
        return results
    
    def bruteforce_files(self, base_url, filenames, wordlist_file=None):
        """
        Brute force uploaded files across directories
        
        Args:
            base_url (str): Base URL to test
            filenames (list): List of filenames to search for
            wordlist_file (str): Path to wordlist file (optional)
            
        Returns:
            dict: File bruteforce results
        """
        logger.info(f"Starting file bruteforce for {len(filenames)} files")
        
        # Load wordlist
        directories = self._load_wordlist(wordlist_file)
        if not directories:
            logger.error("No directories loaded from wordlist")
            return None
        
        results = {
            'base_url': base_url,
            'filenames': filenames,
            'directories_tested': len(directories),
            'found_files': [],
            'file_locations': {}
        }
        
        # Test each file in each directory
        all_test_urls = []
        for directory in directories:
            for filename in filenames:
                test_url = urljoin(base_url.rstrip('/') + '/', directory.rstrip('/') + '/' + filename)
                all_test_urls.append({
                    'url': test_url,
                    'directory': directory,
                    'filename': filename
                })
        
        logger.info(f"Testing {len(all_test_urls)} file/directory combinations")
        
        # Perform concurrent file testing
        found_files = self._bruteforce_files_concurrent(all_test_urls)
        results['found_files'] = found_files
        
        # Organize results by filename
        for found_file in found_files:
            filename = found_file['filename']
            if filename not in results['file_locations']:
                results['file_locations'][filename] = []
            results['file_locations'][filename].append(found_file)
        
        # Summary
        total_found = len(found_files)
        logger.info(f"File bruteforce complete: {total_found} files found")
        
        return results
    
    def _load_wordlist(self, wordlist_file):
        """Load directories from wordlist file"""
        if not wordlist_file:
            # Use default wordlist
            default_wordlist = os.path.join(os.path.dirname(__file__), '..', 'wordlists', 'common_dirs.txt')
            wordlist_file = default_wordlist
        
        if not os.path.exists(wordlist_file):
            logger.error(f"Wordlist file not found: {wordlist_file}")
            return []
        
        try:
            with open(wordlist_file, 'r') as f:
                lines = f.readlines()
            
            # Filter and clean directories
            directories = []
            for line in lines:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    directories.append(line)
            
            logger.info(f"Loaded {len(directories)} directories from {wordlist_file}")
            return directories
            
        except Exception as e:
            logger.error(f"Failed to load wordlist: {str(e)}")
            return []
    
    def _bruteforce_paths(self, base_url, paths, path_type='directory'):
        """Brute force paths with concurrent requests"""
        logger.info(f"Testing {len(paths)} {path_type}s")
        
        found_paths = []
        
        def test_path(path):
            test_url = urljoin(base_url.rstrip('/') + '/', path.rstrip('/') + '/')
            
            try:
                response = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)
                
                # Consider various status codes as accessible
                if response.status_code in [200, 301, 302, 403]:
                    result = {
                        'path': path,
                        'url': test_url,
                        'status_code': response.status_code,
                        'content_length': len(response.content),
                        'content_type': response.headers.get('content-type', ''),
                        'accessible': response.status_code in [200, 301, 302],
                        'protected': response.status_code == 403
                    }
                    
                    with self.lock:
                        found_paths.append(result)
                    
                    status_msg = "accessible" if result['accessible'] else "protected"
                    logger.success(f"Found {path_type}: {path} ({status_msg})")
                
            except requests.exceptions.RequestException:
                # Silently ignore failed requests to reduce noise
                pass
            except Exception as e:
                logger.debug(f"Error testing {path}: {str(e)}")
        
        # Use ThreadPoolExecutor for concurrent testing
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(test_path, path) for path in paths]
            
            # Process completed futures
            for i, future in enumerate(as_completed(futures)):
                try:
                    future.result()
                except Exception as e:
                    logger.debug(f"Thread error: {str(e)}")
                
                # Progress indicator
                if (i + 1) % 50 == 0:
                    logger.info(f"Tested {i + 1}/{len(paths)} {path_type}s")
        
        return found_paths
    
    def _bruteforce_files_concurrent(self, test_urls):
        """Brute force files with concurrent requests"""
        found_files = []
        
        def test_file_url(url_info):
            try:
                response = self.session.get(url_info['url'], timeout=self.timeout)
                
                if response.status_code == 200:
                    # Additional check to ensure it's actually a file, not a directory listing
                    content_type = response.headers.get('content-type', '').lower()
                    
                    result = {
                        'filename': url_info['filename'],
                        'directory': url_info['directory'],
                        'url': url_info['url'],
                        'status_code': response.status_code,
                        'content_length': len(response.content),
                        'content_type': content_type,
                        'executed': self._check_file_execution(response, url_info['filename'])
                    }
                    
                    with self.lock:
                        found_files.append(result)
                    
                    exec_status = " (executed)" if result['executed'] else ""
                    logger.success(f"Found file: {url_info['filename']} in {url_info['directory']}{exec_status}")
                
            except requests.exceptions.RequestException:
                pass  # Silently ignore failed requests
            except Exception as e:
                logger.debug(f"Error testing {url_info['url']}: {str(e)}")
        
        # Concurrent file testing
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(test_file_url, url_info) for url_info in test_urls]
            
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.debug(f"Thread error: {str(e)}")
                
                completed += 1
                if completed % 100 == 0:
                    logger.info(f"Tested {completed}/{len(test_urls)} file locations")
        
        return found_files
    
    def _recursive_enumerate(self, base_url, directories, max_depth=2, current_depth=0):
        """Recursively enumerate subdirectories"""
        if current_depth >= max_depth:
            return None
        
        logger.info(f"Recursive enumeration at depth {current_depth + 1}: {base_url}")
        
        # Test directories at this level
        found_paths = self._bruteforce_paths(base_url, directories, 'subdirectory')
        
        result = {
            'base_url': base_url,
            'depth': current_depth + 1,
            'found_paths': found_paths,
            'recursive_results': []
        }
        
        # Recurse into found accessible directories
        for found_path in found_paths:
            if found_path['accessible'] and current_depth < max_depth - 1:
                recursive_result = self._recursive_enumerate(
                    found_path['url'], 
                    directories, 
                    max_depth, 
                    current_depth + 1
                )
                if recursive_result:
                    result['recursive_results'].append(recursive_result)
        
        return result
    
    def _check_file_execution(self, response, filename):
        """Check if file shows signs of server-side execution"""
        if response.status_code != 200:
            return False
        
        content = response.text.lower()
        content_type = response.headers.get('content-type', '').lower()
        
        # Check for execution indicators based on file type
        if filename.endswith('.php'):
            php_indicators = [
                'php version', 'server_software', 'migr8 php test',
                'current time:', 'upload directory:'
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
                'migr8', 'upload test', 'execution successful',
                'server:', 'framework:', 'current time:'
            ]
            return any(indicator in content for indicator in generic_indicators)
        
        return False
    
    def smart_enumeration(self, base_url, uploaded_files, wordlist_file=None):
        """
        Smart enumeration that combines directory and file discovery
        
        Args:
            base_url (str): Base URL to enumerate
            uploaded_files (list): List of uploaded filenames to search for
            wordlist_file (str): Custom wordlist file path
            
        Returns:
            dict: Combined enumeration results
        """
        logger.info("Starting smart enumeration")
        
        # Phase 1: Directory discovery
        dir_results = self.bruteforce_directories(base_url, wordlist_file, recursive=True)
        
        # Phase 2: File discovery in found directories
        if dir_results and dir_results['accessible_paths']:
            # Extract directory paths from accessible paths
            directory_paths = []
            for path_info in dir_results['accessible_paths']:
                if path_info['accessible']:
                    # Extract relative path from URL
                    relative_path = path_info['url'].replace(base_url.rstrip('/'), '').strip('/')
                    if relative_path:
                        directory_paths.append(relative_path + '/')
                    else:
                        directory_paths.append('')
            
            # Search for uploaded files in discovered directories
            file_results = self.bruteforce_files(base_url, uploaded_files, None)  # Use discovered dirs
            
            combined_results = {
                'enumeration_type': 'smart',
                'directory_results': dir_results,
                'file_results': file_results,
                'summary': {
                    'directories_found': len(dir_results['accessible_paths']),
                    'files_found': len(file_results['found_files']) if file_results else 0,
                    'total_accessible_resources': len(dir_results['accessible_paths']) + (len(file_results['found_files']) if file_results else 0)
                }
            }
            
            logger.info("Smart enumeration complete")
            return combined_results
        
        else:
            logger.warning("No accessible directories found for file enumeration")
            return {
                'enumeration_type': 'smart',
                'directory_results': dir_results,
                'file_results': None,
                'summary': {
                    'directories_found': 0,
                    'files_found': 0,
                    'total_accessible_resources': 0
                }
            }
    
    def close(self):
        """Close the session"""
        self.session.close()
'''

with open("migr8/core/path_bruteforce.py", 'w') as f:
    f.write(path_bruteforce_code)
print("Created: migr8/core/path_bruteforce.py")