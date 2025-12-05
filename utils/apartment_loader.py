import json
from pathlib import Path
from typing import List, Dict
from fastapi import HTTPException


def load_apartments() -> List[Dict]:
    """
    Load apartments from JSON file
    
    Returns:
        List of apartment dictionaries
        
    Raises:
        HTTPException: If file not found or invalid JSON
    """
    apartments_file = Path(__file__).parent.parent / "apartments.json"
    
    try:
        with open(apartments_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail="apartments.json file not found"
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Invalid JSON in apartments.json: {str(e)}"
        )

