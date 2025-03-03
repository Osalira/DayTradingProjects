#!/usr/bin/env python
import re
import sys
import os

def fix_jmeter_file(file_path):
    """
    Fix token extraction in JMeter test file by replacing $.data.token with $.token
    and ensuring Authorization headers are set correctly for endpoints.
    Also fixes port number issues.
    """
    try:
        # Read the JMeter test file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace $.data.token with $.token in JSON extractors
        pattern_json_path = r'(name="JSONPostProcessor\.jsonPathExprs">)\$\.data\.token</stringProp>'
        replacement = r'\1$.token</stringProp>'
        modified_content = re.sub(pattern_json_path, replacement, content)
        
        # Count how many JSON path fixes were made
        json_path_fixes = content.count('$.data.token') - modified_content.count('$.data.token')
        
        # Fix the port number in HTTP requests (from default 80 to 4000)
        # Pattern looks for HTTPSampler.port lines with empty values or non-4000 values
        port_pattern = r'<stringProp name="HTTPSampler\.port">(?!4000)[^<]*</stringProp>'
        port_replacement = r'<stringProp name="HTTPSampler.port">4000</stringProp>'
        modified_content = re.sub(port_pattern, port_replacement, modified_content)
        
        # Make sure BASE_PORT variable is set to 4000
        base_port_pattern = r'<stringProp name="Argument\.value">(\$\{BASE_PORT\})</stringProp>'
        base_port_replacement = r'<stringProp name="Argument.value">4000</stringProp>'
        modified_content = re.sub(base_port_pattern, base_port_replacement, modified_content)
        
        # Create backup file
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Successfully processed {file_path}")
        print(f"Made {json_path_fixes} JSONPath fixes")
        print("Fixed port numbers to use 4000 instead of default port")
        print(f"Backup saved to {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing JMeter file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_jmeter.py <path_to_jmeter_file>")
        sys.exit(1)
    
    jmeter_file = sys.argv[1]
    if not os.path.exists(jmeter_file):
        print(f"File {jmeter_file} not found")
        sys.exit(1)
    
    success = fix_jmeter_file(jmeter_file)
    if success:
        print("\nFix completed. Please review the changes before running the test.")
        print("You may still need to manually add Authorization headers where they're missing.")
    else:
        print("\nFailed to fix the JMeter file. Please check the error message above.")
    sys.exit(0 if success else 1) 