# Display the complete directory structure
import os

def display_tree(path, prefix="", is_last=True):
    """Display directory tree structure"""
    items = []
    if os.path.isdir(path):
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return
    
    items = [item for item in items if not item.startswith('.') or item in ['.htaccess']]
    
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last_item = i == len(items) - 1
        
        current_prefix = "└── " if is_last_item else "├── "
        print(f"{prefix}{current_prefix}{item}")
        
        if os.path.isdir(item_path):
            next_prefix = prefix + ("    " if is_last_item else "│   ")
            display_tree(item_path, next_prefix, is_last_item)

print("Migr8 Framework - Complete Directory Structure:")
print("=" * 50)
print("migr8/")
display_tree("migr8", "")

print("\n" + "=" * 50)
print("Directory Structure Summary:")
print("- 7 Core modules in core/")
print("- 2 Utility modules in utils/") 
print("- 3 Sample payloads in payloads/")
print("- 1 Wordlist file in wordlists/")
print("- Main CLI interface (main.py)")
print("- Setup and documentation files")