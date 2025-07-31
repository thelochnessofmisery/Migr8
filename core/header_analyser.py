"""
Header Analyser Module for Migr8 Framework
Fetches and analyzes HTTP headers for security-related information
"""

import requests
from urllib.parse import urljoin
from utils.logger import logger
from utils.bypasses import USER_AGENTS
import random

class HeaderAnalyser:
    """Analyze HTTP headers for security information and server fingerprinting"""

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })

    def analyze_headers(self, url):
        """
        Analyze HTTP headers for security information

        Args:
            url (str): URL to analyze

        Returns:
            dict: Header analysis results
        """
        logger.info(f"Analyzing headers for: {url}")

        try:
            # Make HEAD request first (more efficient)
            head_response = self.session.head(url, timeout=self.timeout, allow_redirects=True)

            # If HEAD fails, try GET
            if head_response.status_code >= 400:
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            else:
                response = head_response

            headers = dict(response.headers)

            analysis = {
                'url': url,
                'status_code': response.status_code,
                'headers': headers,
                'security_analysis': self._analyze_security_headers(headers),
                'server_info': self._extract_server_info(headers),
                'upload_restrictions': self._analyze_upload_restrictions(headers),
                'vulnerabilities': self._identify_vulnerabilities(headers),
                'recommendations': []
            }

            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(analysis)

            self._log_analysis_summary(analysis)

            return analysis

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch headers: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during header analysis: {str(e)}")
            return None

    def _analyze_security_headers(self, headers):
        """Analyze security-related headers"""
        security_headers = {
            'x-frame-options': {
                'present': 'x-frame-options' in headers,
                'value': headers.get('x-frame-options'),
                'secure': False
            },
            'x-content-type-options': {
                'present': 'x-content-type-options' in headers,
                'value': headers.get('x-content-type-options'),
                'secure': False
            },
            'x-xss-protection': {
                'present': 'x-xss-protection' in headers,
                'value': headers.get('x-xss-protection'),
                'secure': False
            },
            'content-security-policy': {
                'present': 'content-security-policy' in headers,
                'value': headers.get('content-security-policy'),
                'secure': False
            },
            'strict-transport-security': {
                'present': 'strict-transport-security' in headers,
                'value': headers.get('strict-transport-security'),
                'secure': False
            },
            'referrer-policy': {
                'present': 'referrer-policy' in headers,
                'value': headers.get('referrer-policy'),
                'secure': False
            }
        }

        # Evaluate security header values
        if security_headers['x-frame-options']['present']:
            value = security_headers['x-frame-options']['value'].lower()
            security_headers['x-frame-options']['secure'] = value in ['deny', 'sameorigin']

        if security_headers['x-content-type-options']['present']:
            value = security_headers['x-content-type-options']['value'].lower()
            security_headers['x-content-type-options']['secure'] = 'nosniff' in value

        if security_headers['x-xss-protection']['present']:
            value = security_headers['x-xss-protection']['value']
            security_headers['x-xss-protection']['secure'] = '1' in value

        if security_headers['content-security-policy']['present']:
            security_headers['content-security-policy']['secure'] = True

        if security_headers['strict-transport-security']['present']:
            security_headers['strict-transport-security']['secure'] = True

        if security_headers['referrer-policy']['present']:
            security_headers['referrer-policy']['secure'] = True

        return security_headers

    def _extract_server_info(self, headers):
        """Extract server and technology information"""
        server_info = {
            'server': headers.get('server', 'Unknown'),
            'powered_by': headers.get('x-powered-by'),
            'framework': None,
            'language': None,
            'web_server': None
        }

        # Analyze server header
        server = server_info['server'].lower()
        if 'apache' in server:
            server_info['web_server'] = 'Apache'
        elif 'nginx' in server:
            server_info['web_server'] = 'Nginx'
        elif 'iis' in server or 'microsoft' in server:
            server_info['web_server'] = 'IIS'
        elif 'cloudflare' in server:
            server_info['web_server'] = 'Cloudflare'

        # Analyze X-Powered-By header
        powered_by = server_info['powered_by']
        if powered_by:
            powered_by_lower = powered_by.lower()
            if 'php' in powered_by_lower:
                server_info['language'] = 'PHP'
            elif 'asp.net' in powered_by_lower:
                server_info['language'] = 'ASP.NET'
                server_info['framework'] = 'ASP.NET'
            elif 'express' in powered_by_lower:
                server_info['framework'] = 'Express.js'
                server_info['language'] = 'Node.js'

        # Check other headers for technology indicators
        for header_name, header_value in headers.items():
            header_name_lower = header_name.lower()
            header_value_lower = str(header_value).lower()

            if 'php' in header_value_lower:
                server_info['language'] = 'PHP'
            elif 'aspnet' in header_name_lower or 'asp.net' in header_value_lower:
                server_info['language'] = 'ASP.NET'
                server_info['framework'] = 'ASP.NET'

        return server_info

    def _analyze_upload_restrictions(self, headers):
        """Analyze headers that might indicate upload restrictions"""
        restrictions = {
            'max_file_size': None,
            'allowed_types': [],
            'csrf_protection': False,
            'authentication_required': False
        }

        # Check for content length restrictions
        content_length = headers.get('content-length')
        if content_length:
            restrictions['max_file_size'] = int(content_length)

        # Check for CSRF protection
        csrf_headers = ['x-csrf-token', 'x-xsrf-token', 'csrf-token']
        for csrf_header in csrf_headers:
            if csrf_header in headers:
                restrictions['csrf_protection'] = True
                break

        # Check for authentication requirements
        auth_headers = ['www-authenticate', 'authorization']
        for auth_header in auth_headers:
            if auth_header in headers:
                restrictions['authentication_required'] = True
                break

        return restrictions

    def _identify_vulnerabilities(self, headers):
        """Identify potential vulnerabilities based on headers"""
        vulnerabilities = []

        # Missing security headers
        if 'x-frame-options' not in headers:
            vulnerabilities.append({
                'type': 'Missing Security Header',
                'description': 'X-Frame-Options header missing - clickjacking possible',
                'severity': 'Medium'
            })

        if 'x-content-type-options' not in headers:
            vulnerabilities.append({
                'type': 'Missing Security Header',
                'description': 'X-Content-Type-Options header missing - MIME type sniffing possible',
                'severity': 'Low'
            })

        if 'content-security-policy' not in headers:
            vulnerabilities.append({
                'type': 'Missing Security Header',
                'description': 'Content-Security-Policy header missing - XSS protection reduced',
                'severity': 'Medium'
            })

        # Information disclosure
        if 'server' in headers:
            vulnerabilities.append({
                'type': 'Information Disclosure',
                'description': f'Server version disclosed: {headers["server"]}',
                'severity': 'Low'
            })

        if 'x-powered-by' in headers:
            vulnerabilities.append({
                'type': 'Information Disclosure',
                'description': f'Technology stack disclosed: {headers["x-powered-by"]}',
                'severity': 'Low'
            })

        return vulnerabilities

    def _generate_recommendations(self, analysis):
        """Generate security recommendations based on analysis"""
        recommendations = []

        security_headers = analysis['security_analysis']

        # Security header recommendations
        for header_name, header_info in security_headers.items():
            if not header_info['present']:
                recommendations.append(f"Add {header_name.replace('-', ' ').title()} header")
            elif not header_info['secure']:
                recommendations.append(f"Improve {header_name.replace('-', ' ').title()} header configuration")

        # Server information recommendations
        server_info = analysis['server_info']
        if server_info['powered_by']:
            recommendations.append("Remove X-Powered-By header to reduce information disclosure")

        if 'Unknown' not in server_info['server']:
            recommendations.append("Consider hiding server version information")

        return recommendations

    def _log_analysis_summary(self, analysis):
        """Log summary of header analysis"""
        logger.info(f"Header analysis complete for {analysis['url']}")

        # Log server info
        server_info = analysis['server_info']
        if server_info['web_server']:
            logger.info(f"Web Server: {server_info['web_server']}")
        if server_info['language']:
            logger.info(f"Language: {server_info['language']}")

        # Log security status
        security_headers = analysis['security_analysis']
        secure_headers = sum(1 for h in security_headers.values() if h['present'] and h['secure'])
        total_headers = len(security_headers)
        logger.info(f"Security Headers: {secure_headers}/{total_headers} properly configured")

        # Log vulnerabilities
        vuln_count = len(analysis['vulnerabilities'])
        if vuln_count > 0:
            logger.warning(f"Found {vuln_count} potential vulnerabilities")
        else:
            logger.success("No obvious vulnerabilities found in headers")

    def compare_headers(self, urls):
        """
        Compare headers across multiple URLs

        Args:
            urls (list): List of URLs to compare

        Returns:
            dict: Comparison results
        """
        logger.info(f"Comparing headers across {len(urls)} URLs")

        analyses = []
        for url in urls:
            analysis = self.analyze_headers(url)
            if analysis:
                analyses.append(analysis)

        comparison = {
            'analyses': analyses,
            'common_headers': self._find_common_headers(analyses),
            'security_comparison': self._compare_security_headers(analyses)
        }

        return comparison

    def _find_common_headers(self, analyses):
        """Find headers common across all analyzed URLs"""
        if not analyses:
            return []

        common_headers = set(analyses[0]['headers'].keys())
        for analysis in analyses[1:]:
            common_headers &= set(analysis['headers'].keys())

        return list(common_headers)

    def _compare_security_headers(self, analyses):
        """Compare security header implementation across URLs"""
        comparison = {}

        for analysis in analyses:
            url = analysis['url']
            security_headers = analysis['security_analysis']

            comparison[url] = {
                'secure_headers': sum(1 for h in security_headers.values() if h['present'] and h['secure']),
                'total_headers': len(security_headers),
                'vulnerabilities': len(analysis['vulnerabilities'])
            }

        return comparison

    def close(self):
        """Close the session"""
        self.session.close()
