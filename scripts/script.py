import os

# Create the directory structure for Migr8
directories = [
    "migr8",
    "migr8/core",
    "migr8/utils", 
    "migr8/payloads",
    "migr8/wordlists"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Create __init__.py files for Python packages
init_files = [
    "migr8/__init__.py",
    "migr8/core/__init__.py", 
    "migr8/utils/__init__.py"
]

for init_file in init_files:
    with open(init_file, 'w') as f:
        f.write('# Migr8 Upload Vulnerability Reconnaissance Framework\n')
    print(f"Created: {init_file}")