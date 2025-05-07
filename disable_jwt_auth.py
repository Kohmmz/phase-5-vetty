#!/usr/bin/env python3
"""
Script to disable JWT authentication in a Flask application.
This script comments out JWT-related code and replaces get_jwt_identity() calls
with hardcoded user data to allow testing without authentication.
"""

import os
import re
import sys
import shutil
import argparse
import glob

def create_backup(file_path):
    """Create a backup of the file if it doesn't exist already"""
    backup_path = f"{file_path}.bak"
    if not os.path.exists(backup_path):
        print(f"Creating backup: {backup_path}")
        shutil.copy2(file_path, backup_path)
    return backup_path

def restore_from_backup(file_path):
    """Restore file from backup if backup exists"""
    backup_path = f"{file_path}.bak"
    if os.path.exists(backup_path):
        print(f"Restoring from backup: {file_path}")
        shutil.copy2(backup_path, file_path)
        return True
    return False

def disable_jwt_in_file(file_path):
    """
    Disable JWT in a single file by:
    1. Commenting out JWT imports
    2. Commenting out @jwt_required() decorators
    3. Replacing get_jwt_identity() calls with hardcoded user data
    4. Commenting out JWTManager initialization
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Add a comment to indicate the file has been modified
    if "JWT DISABLED TEMPORARILY FOR ROUTE TESTING" not in content:
        content = re.sub(
            r'(from flask import .*)',
            r'\1\n# JWT DISABLED TEMPORARILY FOR ROUTE TESTING',
            content
        )
    
    # Comment out JWT imports
    content = re.sub(
        r'(from flask_jwt_extended import [^)]*(?:\([^)]*\)[^)]*)*)(\n)',
        r'# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n# \1\2',
        content
    )
    
    # Comment out single line imports
    content = re.sub(
        r'(from flask_jwt_extended import [^\n]*)',
        r'# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n# \1',
        content
    )
    
    # Comment out jwt = JWTManager() line
    content = re.sub(
        r'(jwt\s*=\s*JWTManager\(\))',
        r'# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n# \1',
        content
    )
    
    # Comment out jwt.init_app(app) line
    content = re.sub(
        r'(jwt\.init_app\(app\))',
        r'# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n# \1',
        content
    )
    
    # Comment out @jwt_required() decorators
    content = re.sub(
        r'(@jwt_required\(\))',
        r'# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n# \1',
        content
    )
    
    # Replace get_jwt_identity() calls with hardcoded user data based on context
    
    # Case 1: current_user = get_jwt_identity()
    content = re.sub(
        r'(\s+)(current_user\s*=\s*get_jwt_identity\(\))',
        r'\1# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n\1# Original: \2\n\1# Using hardcoded user identity for testing without JWT\n\1current_user = {"id": 1, "role": "User"}',
        content
    )
    
    # Case 2: user_id = get_jwt_identity()['id']
    content = re.sub(
        r'(\s+)(user_id\s*=\s*get_jwt_identity\(\)\[[\'\"]id[\'\"]\])',
        r'\1# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n\1# Original: \2\n\1# Using hardcoded user_id for testing without JWT\n\1user_id = 1  # Hardcoded user_id for testing',
        content
    )
    
    # Case 3: current_user_id = get_jwt_identity()
    content = re.sub(
        r'(\s+)(current_user_id\s*=\s*get_jwt_identity\(\))',
        r'\1# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n\1# Original: \2\n\1# Using hardcoded user_id for testing without JWT\n\1current_user_id = 1  # Hardcoded user_id for testing',
        content
    )
    
    # Case 4: identity = get_jwt_identity()
    content = re.sub(
        r'(\s+)(identity\s*=\s*get_jwt_identity\(\))',
        r'\1# JWT DISABLED TEMPORARILY FOR ROUTE TESTING\n\1# Original: \2\n\1# Using hardcoded user identity for testing without JWT\n\1identity = {"id": 1, "role": "User"}',
        content
    )
    
    # Case 5: Any other get_jwt_identity() call
    content = re.sub(
        r'(get_jwt_identity\(\))',
        r'1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID',
        content
    )
    
    # Only write if content has changed
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def process_directory(directory, restore=False):
    """Process all Python files in the directory to disable or restore JWT"""
    modified_files = []
    
    # Process __init__.py first if it exists
    init_file = os.path.join(directory, '__init__.py')
    if os.path.exists(init_file):
        if restore:
            if restore_from_backup(init_file):
                modified_files.append(init_file)
        else:
            create_backup(init_file)
            if disable_jwt_in_file(init_file):
                modified_files.append(init_file)
    
    # Process all route files
    route_files = []
    
    # Check routes directory if it exists
    routes_dir = os.path.join(directory, 'routes')
    if os.path.exists(routes_dir) and os.path.isdir(routes_dir):
        route_files.extend(glob.glob(os.path.join(routes_dir, '*.py')))
    
    # Also check for route files in the main directory
    route_files.extend(glob.glob(os.path.join(directory, '*_route.py')))
    route_files.extend(glob.glob(os.path.join(directory, '*_routes.py')))
    
    for file_path in route_files:
        if restore:
            if restore_from_backup(file_path):
                modified_files.append(file_path)
        else:
            create_backup(file_path)
            if disable_jwt_in_file(file_path):
                modified_files.append(file_path)
    
    return modified_files

def main():
    parser = argparse.ArgumentParser(description='Disable JWT authentication in a Flask application for testing')
    parser.add_argument('--app-dir', default='app', help='Path to the Flask application directory')
    parser.add_argument('--restore', action='store_true', help='Restore original files from backups')
    args = parser.parse_args()
    
    app_dir = os.path.abspath(args.app_dir)
    if not os.path.exists(app_dir):
        print(f"Error: Directory {app_dir} does not exist")
        sys.exit(1)
    
    if args.restore:
        print(f"Restoring JWT authentication from backups in {app_dir}...")
        modified_files = process_directory(app_dir, restore=True)
        if modified_files:
            print(f"Successfully restored {len(modified_files)} files:")
            for file in modified_files:
                print(f"  - {file}")
        else:
            print("No backup files found to restore.")
    else:
        print(f"Disabling JWT authentication in {app_dir}...")
        modified_files = process_directory(app_dir)
        if modified_files:
            print(f"Successfully modified {len(modified_files)} files:")
            for file in modified_files:
                print(f"  - {file}")
            print("\nJWT authentication has been disabled. To restore, run:")
            print(f"python {os.path.basename(__file__)} --restore")
        else:
            print("No files were modified. JWT might already be disabled or no JWT code was found.")

if __name__ == "__main__":
    main()
