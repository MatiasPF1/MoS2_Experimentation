"""
Handles the complete workflow: folder creation, file generation, and incostem execution in params/xyz files
for
-->
1-Stem Images
2-Label Maps 
3-To Do: For pre_Proccesing 
"""
import os
import subprocess
import shutil
from pathlib import Path



########################      #-1 Create Batch_Folders   ##########################################


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
    
                #Define all the required folder, ones specified in the graphical workflow
    folders = {
        'batch': batch_folder, # Main Folder Holding Everything
        
        'inputs': os.path.join(batch_folder, 'inputs'), # Inputs Folder Holding STEM and Labels XYZ/Params
        'inputs_main': os.path.join(batch_folder, 'inputs', 'main'),
        'inputs_labels': os.path.join(batch_folder, 'inputs', 'labels'),
        
        'outputs': os.path.join(batch_folder, 'outputs'), # Outputs Folder Holding STEM and Labels TiFs
        'outputs_main': os.path.join(batch_folder, 'outputs', 'main'),
        'outputs_labels': os.path.join(batch_folder, 'outputs', 'labels')
    }
    
                #Create all folders with its path 
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    return folders



 ################   #2- Copy the executable files to the batch   #################################


def copy_incostem_files(batch_folder):
    """
    Copies incostem.exe and libfftw3f-3.dll to the batch folder
    """
    #1-Get the batch_workflow directory (where this script is located)
    workflow_dir = Path(__file__).parent.resolve()
    
    #2- Define source and destination paths of the files to copy 
    incostem_src = workflow_dir / "incostem.exe"
    dll_src = workflow_dir / "libfftw3f-3.dll"
    
    #3- Define destination paths in the batch folder
    incostem_dest = os.path.join(batch_folder, "incostem.exe") # Destination path for incostem.exe
    dll_dest = os.path.join(batch_folder, "libfftw3f-3.dll")   # Destination path for DLL
    
    #4- Try and except for the copy process(Exception for possible later errors in the future)
    try:
        if not incostem_src.exists():
            raise FileNotFoundError(f"incostem.exe not found at {incostem_src}")
    
        if not dll_src.exists():
            raise FileNotFoundError(f"libfftw3f-3.dll not found at {dll_src}")
        shutil.copy2(str(incostem_src), incostem_dest)
        shutil.copy2(str(dll_src), dll_dest)
        return True
    
    except Exception as e:
        print(f"Failed to copy files: {e}")
        return False





############## 3- Execute incostem for a single param File ###########################

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
        
        # Execute incostem (mimics: Get-Content file.param | .\incostem.exe), that was what worked in powershell when i tried to run incostem
        result = subprocess.run(
            [incostem_path],
            input=params_content,  # Pipe the content of the param file
            capture_output=True, # Capture stdout and stderr
            cwd=batch_folder,  # Run in batch folder
            timeout=300,  # 5 minute timeout
            shell=False   # No shell needed
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
            
    # - This except handles if the procces time exceeds the timeout limit 
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Execution timeout (exceeded 5 minutes)",
            "file": os.path.basename(param_file_path)
        }
    # - This except handles if the param file is not found
    except PermissionError as e:
        return {
            "success": False,
            "message": f"Permission error: {str(e)}",
            "file": os.path.basename(param_file_path)
        }
    # - This except handles any other general exception
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "file": os.path.basename(param_file_path)
        }
    #- Finally block to ensure cleanup
    finally:
        import gc
        gc.collect()



############## #4-Main Function to Execute Incostem For All Param Files in an Folder #######################

def _execute_param_files(batch_folder, input_folder, file_type="images"):
    """
    Args:
        batch_folder: Path to batch folder containing incostem.exe
        input_folder: Path to folder containing .param files
        file_type: Description for return message (e.g., "images", "label images")
    
    Returns:
        dict: Execution results with success status and statistics
    """
    
    
    #1-Find all .param files + handle no files found
    param_files = []
    for f in os.listdir(input_folder):
        if f.endswith('.param'):
            param_files.append(f)
    
    if not param_files:
        return {
            "success": False,
            "message": f"No .param files found in {os.path.basename(input_folder)}/",
            "results": []
        }
    
    #2-Verify incostem.exe exists before execution
    incostem_exe = os.path.join(batch_folder, 'incostem.exe')
    if not os.path.exists(incostem_exe):
        return {
            "success": False,
            "message": "incostem.exe not found in batch folder",
            "results": []
        }
    
    #3-Execute incostem for each param file
    results = []
    for param_file in param_files:
        param_path = os.path.join(input_folder, param_file) # Full path to param file
        result = execute_incostem_file(batch_folder, param_path) # Execute incostem
        results.append(result) # Collect result
    
    successful = sum(1 for r in results if r['success']) # Count successful executions
    total = len(param_files) # Total number of param files
    
    #4-Return summary of execution results
    return {
        "success": successful > 0,
        "message": f"Completed {successful}/{total} {file_type}",
        "results": results,
        "successful": successful,
        "total": total
    }

#4.1-Execute for Input Folder
def execute_batch(folders):
    """
    Executes incostem for all main image param files in the batch
    """
    return _execute_param_files(folders['batch'], folders['inputs_main'], "images")


#4.2-Execute for Label Folder
def execute_labels(folders):
    """
    Executes incostem for all label param files in the batch
    """
    return _execute_param_files(folders['batch'], folders['inputs_labels'], "label images")



################   5- Organize output files into appropriate folders  ###########################

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
    label_keywords = ['metal_Doped', 'metal_vacancy', '1Doped', '2Doped', '1vacancy', '2vacancy']
    
    for tif_file in tif_files:
        src = os.path.join(batch_folder, tif_file)
        
        # Check if it's a label map (contains keywords)
        is_label = any(keyword in tif_file for keyword in label_keywords)
        
        # Determine destination folder and move file
        dest_folder = outputs_labels if is_label else outputs_main
        dest = os.path.join(dest_folder, tif_file)
        
        try:
            shutil.move(src, dest)
        except Exception:
            pass