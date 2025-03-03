#!/usr/bin/env python
import re
import sys
import os

def selectively_fix_assertions(file_path):
    """
    Selectively fix JMeter assertions:
    - Restore the Failed Register Request to expect 400 
    - Keep the Failed Login Request expecting 401
    """
    try:
        print(f"Opening file: {file_path}")
        # Read the JMeter test file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # First, identify the Failed Register section
        register_pattern = re.compile(r'<HTTPSamplerProxy.*?Failed Register Request.*?</HTTPSamplerProxy>', re.DOTALL)
        register_match = register_pattern.search(content)
        
        if not register_match:
            print("Could not find the Failed Register Request in the file")
            return False
        
        # Get the section that follows the Failed Register Request (which should contain its assertions)
        register_end_pos = register_match.end()
        next_section = content[register_end_pos:register_end_pos + 5000]  # Look at the next chunk
        
        # Find the Response Assertion in this section and fix it back to 400
        fixed_section = re.sub(
            r'(<stringProp name="Assertion\.test_strings">)401(</stringProp>)',
            r'\1400\2',
            next_section
        )
        
        # Replace this section in the content
        modified_content = content[:register_end_pos] + fixed_section + content[register_end_pos + len(next_section):]
        
        # Count changes
        register_fixes = fixed_section.count('400</stringProp>') - next_section.count('400</stringProp>')
        
        print(f"Fixed {register_fixes} assertions for Failed Register Request")
        
        # Create backup file
        backup_path = file_path + '.selective.backup'
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Successfully processed {file_path}")
        print(f"Backup saved to {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing JMeter assertions: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_selective_assertions.py <path_to_jmeter_file>")
        sys.exit(1)
    
    jmeter_file = sys.argv[1]
    if not os.path.exists(jmeter_file):
        print(f"File {jmeter_file} not found")
        sys.exit(1)
    
    success = selectively_fix_assertions(jmeter_file)
    if success:
        print("\nSelective fix completed. Please review the changes before running the test.")
        print("The Failed Register Request should now expect HTTP 400 while Failed Login Request still expects HTTP 401.")
    else:
        print("\nFailed to fix the JMeter file. Please check the error message above.")
    sys.exit(0 if success else 1) 