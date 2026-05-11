import json
import urllib.request
import urllib.error
from typing import List, Tuple, Dict

WORKER_URL = "http://localhost:50051"

def _send_request(endpoint: str, payload: dict) -> dict:
    url = f"{WORKER_URL}{endpoint}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f"Blender Worker Error [{e.code}]: {error_body}")

def run_blender_extract_obj(raw_file_path: str, output_obj_path: str) -> Tuple[str, Dict[str, float]]:
    """Tells the persistent Blender worker to extract and clean the obj, returning bounds."""
    print(f"Sending extract request to Blender worker for {raw_file_path}...")
    result = _send_request("/extract", {
        "input_file": raw_file_path,
        "output_file": output_obj_path
    })
    
    return output_obj_path, result.get("bounds", {})

def run_blender_photoshoot(obj_file_path: str, output_dir: str) -> List[str]:
    """Tells the persistent Blender worker to take 5 screenshots of the obj."""
    print(f"Sending photoshoot request to Blender worker for {obj_file_path}...")
    result = _send_request("/photoshoot", {
        "input_obj": obj_file_path,
        "output_dir": output_dir
    })
    
    return result.get("images", [])
