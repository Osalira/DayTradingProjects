#!/usr/bin/env python
import re
import sys
import os

def fix_jmeter_file(file_path):
    """
    Fix token headers in JMeter test file by replacing:
    - Header named 'token' with 'Authorization'
    - Header value '${tokenVar}' with 'Bearer ${tokenVar}'
    """
    try:
        # Read the JMeter test file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all HeaderManager sections that contain token headers
        pattern = r'(<elementProp name="" elementType="Header">\s*<stringProp name="Header\.name">)token(</stringProp>\s*<stringProp name="Header\.value">\$\{[^}]+\})(</stringProp>)'
        replacement = r'\1Authorization\2</stringProp>'
        modified_content = re.sub(pattern, replacement, content)
        
        # Now update the token value to add Bearer prefix
        pattern = r'(<stringProp name="Header\.name">Authorization</stringProp>\s*<stringProp name="Header\.value">)(\$\{[^}]+\})(</stringProp>)'
        replacement = r'\1Bearer \2\3'
        modified_content = re.sub(pattern, replacement, modified_content)
        
        # Count how many header fixes were made
        header_name_fixes = content.count('<stringProp name="Header.name">token</stringProp>') - modified_content.count('<stringProp name="Header.name">token</stringProp>')
        
        # Create backup file
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Successfully processed {file_path}")
        print(f"Made {header_name_fixes} header fixes (token -> Authorization with Bearer prefix)")
        print(f"Backup saved to {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing JMeter file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_jmeter_auth.py <path_to_jmeter_file>")
        sys.exit(1)
    
    jmeter_file = sys.argv[1]
    if not os.path.exists(jmeter_file):
        print(f"File {jmeter_file} not found")
        sys.exit(1)
    
    success = fix_jmeter_file(jmeter_file)
    if success:
        print("\nFix completed. Please review the changes before running the test.")
    else:
        print("\nFailed to fix the JMeter file. Please check the error message above.")
    sys.exit(0 if success else 1) 