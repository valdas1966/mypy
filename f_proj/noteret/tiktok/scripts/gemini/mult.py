import os
import json
import re


# Path to the script to duplicate
path_script = r"C:\Users\user\Desktop\noteret\tiktok\scripts\gemini\gemini_api.py"
# Path to the folder containing the service account JSON key files
path_keys = r"C:\Users\user\Desktop\noteret\tiktok\scripts\gemini\keys"
# Path to the output folder for the generated script files
path_output = r"C:\Users\user\Desktop\noteret\tiktok\scripts\gemini\output"


# Read source script content
with open(path_script, 'r') as f:
    script_content = f.read()

# Get i_0_base filename without extension and add regex pattern for cat value
pattern_cat = r'cat\s*=\s*\d+'
base_name = os.path.splitext(os.path.basename(path_script))[0]

# Process each JSON key file
for i, json_file in enumerate(os.listdir(path_keys)):
    if not json_file.endswith('.json'):
        continue
        
    json_path = os.path.join(path_keys, json_file)
    
    # Read project ID from JSON
    with open(json_path, 'r') as f:
        key_data = json.load(f)
        project_id = key_data.get('project_id')
        
    if not project_id:
        continue
        
    # Create new script content with replacements
    new_content = script_content
    
    # Replace service account key old_path
    new_content = re.sub(
        r'service_account_key_path\s*=\s*r?"[^"]*"',
        f'service_account_key_path = r"{json_path}"',
        new_content
    )
    
    # Replace project ID
    new_content = re.sub(
        r'project_id\s*=\s*"[^"]*"', 
        f'project_id = "{project_id}"',
        new_content
    )
    
    # Generate output filename with index
    output_filename = f"{base_name}_{i}.py"
    output_path = os.path.join(path_output, output_filename)
    
    # Write new script file
    with open(output_path, 'w') as f:
        f.write(new_content)
