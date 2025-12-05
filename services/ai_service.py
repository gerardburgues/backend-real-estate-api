import json
import re
import os
from pathlib import Path
from typing import List, Dict
from fastapi import HTTPException
from google.genai import types
from google import genai

class AIService:
    """Service for handling AI operations using Google Gemini"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AI Service with Gemini client
        
        Args:
            api_key: Google Gemini API key. If not provided, will try to get from env
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-lite"
        self._load_prompts()
    
    def _load_prompts(self):
        """Load prompts from prompt.md file"""
        prompt_file = Path(__file__).parent / "prompt.md"
        with open(prompt_file, "r") as f:
            content = f.read()
            # Extract system instruction
            system_start = content.find("## System Instruction") + len("## System Instruction")
            context_start = content.find("## Context Template")
            system_end = context_start if context_start > system_start else len(content)
            self.system_instruction = content[system_start:system_end].strip()
            
            # Extract context template
            context_start = content.find("## Context Template") + len("## Context Template")
            self.context_template = content[context_start:].strip()
        
    async def find_best_apartment(self, query: str, apartments: List[Dict]) -> Dict:
        """
        Use Gemini LLM to find the best matching apartment based on user query
        
        Args:
            query: User's apartment search query
            apartments: List of apartment dictionaries to search from
            
        Returns:
            Dictionary of the best matching apartment
            
        Raises:
            HTTPException: If API call fails or no matching apartment found
        """
        try:
            apartments_str = json.dumps(apartments, indent=2)
            
            # Format context using template from prompt.md
            context = self.context_template.format(
                query=query,
                apartments_list=apartments_str
            )
            
            # print("before running the config (async)")
            print("context: ", context)
            print("system_instruction: ", self.system_instruction)
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=context,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    max_output_tokens=10,
                    # thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            print("response: ", response)   
            apartment_id_str = response.text.strip()
            
            # Try to extract ID number (handle cases where LLM adds extra text)
            apartment_id = self._extract_apartment_id(apartment_id_str, apartments)
            
            # Find apartment by ID
            for apartment in apartments:
                if apartment.get("id") == apartment_id:
                    return apartment
            
            # Fallback: return first apartment if ID not found
            return apartments[0]
        
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=f"Configuration error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error calling Gemini API: {str(e)}"
            )
    
    def _extract_apartment_id(self, response_text: str, apartments: List[Dict]) -> int:
        """
        Extract apartment ID from LLM response
        
        Args:
            response_text: The text response from the LLM
            apartments: List of apartments to validate IDs against
            
        Returns:
            Valid apartment ID, or first apartment's ID as fallback
        """
        # Extract all numbers from the response
        numbers = re.findall(r'\d+', response_text)
        
        # Try to find a matching apartment ID
        valid_ids = {apt.get("id") for apt in apartments if apt.get("id")}
        
        for num_str in numbers:
            try:
                candidate_id = int(num_str)
                if candidate_id in valid_ids:
                    return candidate_id
            except ValueError:
                continue
        
        # Fallback: return first apartment's ID
        return apartments[0].get("id") if apartments else None

