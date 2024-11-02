# deploy.py

import os
import subprocess
import sys

def run_command(command):
    """Execute shell command and return output"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def deploy_package():
    # Configuration
    REMOTE_USER = "pravin"
    REMOTE_HOST = "192.168.0.169"
    REMOTE_PATH = "/home/pravin/Documents/pythonproj/whl/"
    PACKAGE_NAME = "retail_sales_report"
    
    try:
        print("1. Building wheel package...")
        code, out, err = run_command("python setup.py bdist_wheel")
        if code != 0:
            raise Exception(f"Failed to build wheel: {err}")
        
        # Get the wheel file name
        wheel_file = f"dist/{PACKAGE_NAME}-0.1-py3-none-any.whl"
        if not os.path.exists(wheel_file):
            raise Exception("Wheel file not found")
            
        print("2. Copying wheel to remote system...")
        scp_command = f"scp {wheel_file} {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}"
        code, out, err = run_command(scp_command)
        if code != 0:
            raise Exception(f"Failed to copy wheel: {err}")
            
        print("3. Installing package on remote system...")
        ssh_command = f"ssh {REMOTE_USER}@{REMOTE_HOST} 'cd {REMOTE_PATH} && pip install {PACKAGE_NAME}-0.1-py3-none-any.whl --force-reinstall'"
        code, out, err = run_command(ssh_command)
        if code != 0:
            raise Exception(f"Failed to install package: {err}")
            
        print("4. Testing installation...")
        test_command = f"ssh {REMOTE_USER}@{REMOTE_HOST} 'retail_sales_report --version'"
        code, out, err = run_command(test_command)
        if code != 0:
            raise Exception(f"Package installation test failed: {err}")
            
        print("Deployment completed successfully!")
        
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    deploy_package()