"""
STEM Executor Module
Executes incostem.exe with XYZ and params files to generate STEM images
"""
import os
import subprocess # To Execute incostem.exe
import base64 # For Decoding File Contents
from pathlib import Path # For Path Manipulations


def execute_incostem(xyz_content, params_content, xyz_filename, params_filename):
    script_dir = Path(__file__).parent.resolve() # Directory of this script
    incostem_path = script_dir / "incostem.exe" # Path to incostem.exe
    
    # Chcker for : Incostem.exe doest not exist 
    if not incostem_path.exists():
        return {
            "success": False,
            "message": f"incostem.exe not found at {incostem_path}",
            "output": ""
        }
    
    try:
        ###### 1) Assigning the XYZ and Params File in the Same Directory as this Script ######
        
        
        # 1-Decode base64 content (format: "data:application/octet-stream;base64,<content>")
        xyz_data = xyz_content.split(',')[1] if ',' in xyz_content else xyz_content
        params_data = params_content.split(',')[1] if ',' in params_content else params_content
        
        # 2-Decode from base64
        xyz_decoded = base64.b64decode(xyz_data)
        params_decoded = base64.b64decode(params_data)
        
        # 3-Save files to the _2_computem_stem_generation directory
        xyz_file_path = script_dir / xyz_filename
        params_file_path = script_dir / params_filename
        
        
        
        ###### 2) Saving the XYZ and Params Files in the Same Directory as this Script ######
        
        
        with open(xyz_file_path, 'wb') as f: # Save XYZ file
            f.write(xyz_decoded)
        
        with open(params_file_path, 'wb') as f: # Save Params file
            f.write(params_decoded)
            
        
        ###### 3) Execute incostem.exe with Params file piped as stdin (Like in Powershell) ######
        
        
        # This mimics the Terminal Command: Get-Content <params_file> | .\incostem.exe
        result = subprocess.run(
            [str(incostem_path)],
            input=params_decoded,  # Pipe the params content as stdin
            capture_output=True,
            text=False,  # Use bytes mode since params might be binary
            cwd=str(script_dir),  # Set working directory
            timeout=300  # 5 minute timeout, so it doesn't hang indefinitely
        )
        
        
        ###### 4) Check if execution was successful ######
        
        
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"STEM images generated successfully! Output files saved in {script_dir}",
                "output": result.stdout.decode('utf-8', errors='ignore') if result.stdout else "",
                "xyz_file": str(xyz_file_path),
                "params_file": str(params_file_path)
            }
        else:
            return {
                "success": False,
                "message": f"incostem.exe execution failed (exit code: {result.returncode})",
                "output": result.stderr.decode('utf-8', errors='ignore') if result.stderr else ""
            }
            
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Execution timeout (exceeded 5 minutes)",
            "output": ""
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during execution: {str(e)}",
            "output": ""
        }
