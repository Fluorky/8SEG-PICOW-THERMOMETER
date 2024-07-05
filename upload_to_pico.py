import os
import subprocess

port = '/dev/tty.usbmodem14101'
local_folder = 'picoWfiles'
files_to_upload = ['thermometer8seg.py', 'config.py', '__init__.py', 'main.py', 'wificonnection.py']

all_files_uploaded = True

for file in files_to_upload:
    local_path = os.path.join(local_folder, file)
    command = f'ampy --port {port} put {local_path} {file}'
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f'Uploaded {file} to {port}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to upload {file} to {port}')
        print(f'Error: {e.stderr}')
        all_files_uploaded = False
    except Exception as e:
        print(f'An unexpected error occurred while uploading {file} to {port}')
        print(f'Error: {str(e)}')
        all_files_uploaded = False

if all_files_uploaded:
    print("All files uploaded successfully.")
else:
    print("Some files were not uploaded successfully.")
