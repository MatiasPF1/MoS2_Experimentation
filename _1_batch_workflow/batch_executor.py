"""
Batch Workflow Executor Module
Handles the complete workflow: folder creation, file generation, and incostem execution
"""
import os
import subprocess
import shutil
from pathlib import Path


def create_batch_folders(base_path, batch_num):
    """
    Creates the batch folder structure:
    batch_X/
        inputs/
            main/
            labels/
        outputs/
            main/
            labels/
    """
    batch_folder = os.path.join(base_path, f"batch_{batch_num}") # This is the batch_X folder
    
    #1=Define all the required folder, ones specified in the graphical workflow
    folders = {
        'batch': batch_folder,
        'inputs': os.path.join(batch_folder, 'inputs'),
        'inputs_main': os.path.join(batch_folder, 'inputs', 'main'),
        'inputs_labels': os.path.join(batch_folder, 'inputs', 'labels'),
        'outputs': os.path.join(batch_folder, 'outputs'),
        'outputs_main': os.path.join(batch_folder, 'outputs', 'main'),
        'outputs_labels': os.path.join(batch_folder, 'outputs', 'labels')
    }
    
    #2=Create all folders
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    return folders


def copy_incostem_files(batch_folder):
    """
    Copies incostem.exe and libfftw3f-3.dll to the batch folder
    """
    #1-Get the _1_batch_workflow directory (where this script is located)
    workflow_dir = Path(__file__).parent.resolve()
    
    incostem_src = workflow_dir / "incostem.exe"
    dll_src = workflow_dir / "libfftw3f-3.dll"
    
    incostem_dest = os.path.join(batch_folder, "incostem.exe") # Destination path for incostem.exe
    dll_dest = os.path.join(batch_folder, "libfftw3f-3.dll")   # Destination path for DLL
    
    #2- Try and except for the copy procces 
    try:
        if incostem_src.exists():
            shutil.copy2(str(incostem_src), incostem_dest)
        else:
            return False
            
        if dll_src.exists():
            shutil.copy2(str(dll_src), dll_dest)
        else:
            return False
        
        return True
        
    except Exception as e:
        print(f"Error copying incostem files: {e}") 
        return False


def execute_incostem_file(batch_folder, param_file_path):
    """
    Case 1: 
    Executes incostem.exe for a single param file
    """
    
    #1-Get the path to incostem.exe and  handle missing file
    incostem_path = os.path.join(batch_folder, "incostem.exe")
    
    if not os.path.exists(incostem_path):
        return {
            "success": False,
            "message": f"incostem.exe not found in {batch_folder}",
            "file": param_file_path
        }
        
        
    #2- Execute incostem with the param file content piped in
    try:
        # Read the param file content
        with open(param_file_path, 'rb') as f:
            params_content = f.read()
        
        # Execute incostem (mimics: Get-Content file.param | .\incostem.exe), that was what worked in powershell
        result = subprocess.run(
            [incostem_path],
            input=params_content,
            capture_output=True,
            cwd=batch_folder,  # Run in batch folder
            timeout=300,  # 5 minute timeout
            shell=False
        )
        
    #3- Handle the result, returns a dictionary with success status and message
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully generated STEM image",
                "file": os.path.basename(param_file_path)
            }
        else:
            error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else "Unknown error"
            return {
                "success": False,
                "message": f"Execution failed: {error_msg}",
                "file": os.path.basename(param_file_path)
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Execution timeout (exceeded 5 minutes)",
            "file": os.path.basename(param_file_path)
        }
    except PermissionError as e:
        return {
            "success": False,
            "message": f"Permission error: {str(e)}",
            "file": os.path.basename(param_file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "file": os.path.basename(param_file_path)
        }
    finally:
        # Ensure cleanup
        import gc
        gc.collect()


def execute_batch(folders, progress_callback=None):
    """
    Case 2:
    Executes incostem for all main image param files in the batch
    """
    
    batch_folder = folders['batch'] # This is the batch_X folder
    inputs_main = folders['inputs_main'] # This is the inputs/main/ folder
    
    #1-Find all .param files in inputs/main/ and handle no files found
    param_files = [f for f in os.listdir(inputs_main) if f.endswith('.param')]
    
    if not param_files:
        return {
            "success": False,
            "message": "No .param files found in inputs/main/",
            "results": []
        }
    
    results = []
    total = len(param_files) # Total number of param files to process 
    
    
    
    #2-Verify incostem.exe exists before execution
    incostem_exe = os.path.join(batch_folder, 'incostem.exe')
    if not os.path.exists(incostem_exe):
        return {
            "success": False,
            "message": "incostem.exe not found in batch folder",
            "results": []
        }
        
        
    #3-Execute incostem for each param file, with optional progress callback
    for idx, param_file in enumerate(param_files, 1): # We will execute the file one by one with the function created before 
        param_path = os.path.join(inputs_main, param_file)
        if progress_callback:
            progress_callback(idx, total, param_file)
        result = execute_incostem_file(batch_folder, param_path) 
        results.append(result)
    successful = sum(1 for r in results if r['success'])
    
    #4-Return summary of execution results
    return {
        "success": successful > 0,
        "message": f"Completed {successful}/{total} images",
        "results": results,
        "successful": successful,
        "total": total
    }


def organize_output_files(folders):
    """
    Moves generated TIF files to appropriate output folders
    Main images → outputs/main/
    Label maps → outputs/labels/
    
    Args:
        folders: Dictionary of folder paths from create_batch_folders
    """
    batch_folder = folders['batch']
    outputs_main = folders['outputs_main']
    outputs_labels = folders['outputs_labels']
    
    #1-Find all .tif files in batch folder
    tif_files = [f for f in os.listdir(batch_folder) if f.endswith('.tif')]
    
    #2-Move files to appropriate output folders
    for tif_file in tif_files:
        src = os.path.join(batch_folder, tif_file)
        
        # Check if it's a label map (contains keywords)
        is_label = any(keyword in tif_file for keyword in 
                      ['metal_Doped', 'metal_vacancy', '1Doped', '2Doped', '1vacancy', '2vacancy'])
        
        
        #3-Determine destination folder
        dest_folder = outputs_labels if is_label else outputs_main
        dest = os.path.join(dest_folder, tif_file)
        
        #4-Move the file and handle exceptions
        try:
            shutil.move(src, dest)
        except Exception as e: 
            print(f"Warning: Could not move {tif_file}: {e}")
    
    print(f"Organized output TIF files into outputs/main/ and outputs/labels/")
