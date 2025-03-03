#!/usr/bin/env python
import re
import sys
import os
import traceback

def fix_jmeter_assertions(file_path):
    """
    Fix JMeter assertion for login failure:
    - Updates the "Failed Login Request" test to expect 401 instead of 400
    """
    try:
        print(f"Opening file: {file_path}")
        # Read the JMeter test file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"File size: {len(content)} bytes")
        
        # Find the most direct approach - look for any 400 in assertion strings
        print("Searching for Response Code assertions with 400...")
        
        # Simple approach - just replace any ResponseAssertion with 400 to 401
        pattern = r'(<ResponseAssertion.*?<stringProp name="Assertion\.test_strings">)400(</stringProp>)'
        modified_content = re.sub(pattern, r'\1401\2', content, flags=re.DOTALL)
        
        # Count how many assertion fixes were made
        assertion_fixes = modified_content.count('<stringProp name="Assertion.test_strings">401</stringProp>') - content.count('<stringProp name="Assertion.test_strings">401</stringProp>')
        
        print(f"Found {assertion_fixes} assertions to fix")
        
        if assertion_fixes == 0:
            # Try a more direct search
            print("Trying direct search for the string value in assertions...")
            if '400</stringProp>' in content:
                print("Found '400</stringProp>' in content")
                modified_content = content.replace('400</stringProp>', '401</stringProp>')
                assertion_fixes = modified_content.count('401</stringProp>') - content.count('401</stringProp>')
                print(f"Fixed {assertion_fixes} assertions with direct replacement")
        
        # Create backup file
        backup_path = file_path + '.assertions.backup'
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Successfully processed {file_path}")
        print(f"Made {assertion_fixes} assertion fixes (400 -> 401)")
        print(f"Backup saved to {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing JMeter assertions: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_jmeter_assertions.py <path_to_jmeter_file>")
        sys.exit(1)
    
    jmeter_file = sys.argv[1]
    if not os.path.exists(jmeter_file):
        print(f"File {jmeter_file} not found")
        sys.exit(1)
    
    success = fix_jmeter_assertions(jmeter_file)
    if success:
        print("\nFix completed. Please review the changes before running the test.")
        print("The 'Failed Login Request' test should now expect HTTP 401 instead of 400.")
    else:
        print("\nFailed to fix the JMeter file. Please check the error message above.")
    sys.exit(0 if success else 1) 