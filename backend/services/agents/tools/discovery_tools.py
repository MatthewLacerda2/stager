from typing import List, Dict, Any

def search_library_objects(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Searches the asset pool using semantic text matching.
    
    Args:
        query: Plain English description of the desired object (e.g., "mid-century modern wooden chair").
        limit: Max results to return.
    
    Returns:
        A concise JSON list of matched assets containing only id, name, and a brief summary.
    """
    pass

def search_scene_objects(query: str) -> List[Dict[str, Any]]:
    """
    Semantically searches instances (scene_objects and group_objects) currently instantiated inside the active scene.
    
    Args:
        query: Description of what to find in the current layout.
    
    Returns:
        A list of matching scene objects, their current IDs, names, parent groups, and global transform coordinates.
    """
    pass

def describe_scene() -> str:
    """
    Programmatically generates a structured text summary of the objects placements in the scene.
    
    Returns:
        A text payload detailing total object counts, group hierarchies, active camera framing, lighting setup, and general layout bounding boxes.
    """
    pass
