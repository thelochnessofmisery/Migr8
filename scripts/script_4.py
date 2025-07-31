# Create the common_dirs.txt wordlist file
wordlist_content = '''# Common upload directories wordlist for Migr8
# Inspired by SecLists directory enumeration lists

# Standard upload directories
uploads
upload
files
file
attachments
attachment
documents
document
media
images
image
pics
pictures
photo
photos
assets
static
data
temp
tmp
cache

# Framework-specific directories
wp-content/uploads
wp-includes
wp-admin/includes
admin/uploads
administrator/uploads
public/uploads
storage/uploads
app/uploads
var/uploads
var/www/uploads
htdocs/uploads
public_html/uploads

# Language-specific upload paths
uploads/php
uploads/asp
uploads/aspx
uploads/jsp
uploads/cgi-bin
cgi-bin/uploads

# Nested common paths
files/uploads
files/documents
files/images
data/uploads
data/files
media/uploads
media/files
temp/uploads
tmp/files
cache/uploads

# Application directories
upload/files
upload/images
upload/documents
file/upload
attachments/files
documents/upload
images/upload
photos/upload

# Date-based directories (common patterns)
uploads/2023
uploads/2024
uploads/2025
files/2023
files/2024
files/2025
media/2023
media/2024
media/2025

# User directories
uploads/user
uploads/users
files/user
files/users
user/uploads
users/uploads
profile/uploads
profiles/uploads

# CMS-specific paths
drupal/files
joomla/images
wordpress/uploads
magento/media
prestashop/upload
opencart/image

# Web server directories
www/uploads
web/uploads
public/files
private/uploads
secure/uploads
restricted/files

# Backup directories
backup/uploads
backups/files
old/uploads
archive/files
bak/uploads

# Development directories
dev/uploads
test/uploads
staging/uploads
demo/uploads
beta/uploads

# Hidden directories
.uploads
.files
.tmp
.cache
.data

# Special characters and variations
upload%20files
files_upload
upload-files
files-upload
upload.files
files.upload
'''

with open("migr8/wordlists/common_dirs.txt", 'w') as f:
    f.write(wordlist_content)
print("Created: migr8/wordlists/common_dirs.txt")