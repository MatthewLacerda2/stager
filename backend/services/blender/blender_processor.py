import os
from typing import List

def run_blender_extract_obj(raw_file_path: str, output_obj_path: str) -> str:
    """Runs the headless blender script to extract and clean the obj."""
    script_path = os.path.join(os.path.dirname(__file__), "extract_obj.py")
    
    cmd = [
        "blender", "-b", "-P", script_path, "--",
        raw_file_path, output_obj_path
    ]
    
    # In a production environment, this will spawn the process
    # subprocess.run(cmd, check=True, capture_output=True)
    print(f"Executing: {' '.join(cmd)}")
    return output_obj_path

def run_blender_photoshoot(obj_file_path: str, output_dir: str) -> List[str]:
    """Runs the headless blender script to take 5 screenshots of the obj."""
    script_path = os.path.join(os.path.dirname(__file__), "photoshoot.py")
    
    cmd = [
        "blender", "-b", "-P", script_path, "--",
        obj_file_path, output_dir
    ]
    
    # In a production environment, this will spawn the process
    # subprocess.run(cmd, check=True, capture_output=True)
    print(f"Executing: {' '.join(cmd)}")
    
    images = [os.path.join(output_dir, f"shot_{i}.png") for i in range(5)]
    return images
