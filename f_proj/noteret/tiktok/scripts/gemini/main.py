#!/usr/bin/env python3
import os
import sys
import subprocess

# Define the folder path directly
folder_path = r'c:\path'

if not os.path.isdir(folder_path):
    print(f"Error: '{folder_path}' is not a valid directory.")
    sys.exit(1)

# List all .py files in the folder (ignoring files that start with __ like __init__.py)
script_files = [f for f in os.listdir(folder_path) 
                if f.endswith(".py") and not f.startswith("__")]

if not script_files:
    print("No Python script files found in the specified folder.")
    sys.exit(0)

processes = []
for script in script_files:
    script_path = os.path.join(folder_path, script)
    print(f"Starting {script_path}...")
    # Launch the script using the same Python interpreter
    p = subprocess.Popen([sys.executable, script_path])
    processes.append(p)

# Optionally, wait for all processes to complete
for p in processes:
    p.wait()

print("All scripts have finished.")
