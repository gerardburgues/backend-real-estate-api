import json
import re
import os
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import HTTPException
from google.genai import types
from google import genai
from models.schemas import FindApartmentResponse, ApartmentData, GeminiApartmentResponse

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
            FindApartmentResponse with exists flag and apartment_id
            
        Raises:
            HTTPException: If API call fails
        """
        try:
            apartments_str = json.dumps(apartments, indent=2)
            
            # Format context using template from prompt.md
            context = self.context_template.format(
                query=query,
                apartments_list=apartments_str
            )
            
            # print("before running the config (async)")
        
            
            # Pass Pydantic model directly to Gemini for structured output
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=context,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    max_output_tokens=300,
                    response_schema=GeminiApartmentResponse,
                    response_mime_type="application/json",
                    #thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            print("response: ", response)
            
            # Check if max tokens was reached
            max_tokens_reached = False
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    # Check for finish_reason in various possible formats
                    finish_reason = None
                    if hasattr(candidate, 'finish_reason'):
                        finish_reason = candidate.finish_reason
                    elif hasattr(candidate, 'finishReason'):
                        finish_reason = candidate.finishReason
                    
                    # Check if finish reason indicates max tokens
                    if finish_reason:
                        finish_reason_str = str(finish_reason).upper()
                        max_tokens_reached = 'MAX_TOKENS' in finish_reason_str or finish_reason_str == 'MAX_TOKENS'
            except Exception:
                # If we can't determine, assume not reached
                max_tokens_reached = False
            
            # Parse structured JSON response
            try:
                # Check if Gemini SDK already parsed the response
                if hasattr(response, 'parsed') and response.parsed is not None:
                    gemini_response = response.parsed
                    print(f"Using parsed response: {gemini_response}")
                else:
                    # Fallback to parsing text manually
                    response_text = response.text.strip() if response.text else "{}"
                    response_data = json.loads(response_text)
                    # Create response from Gemini's structured data (only exists and apartment_id)
                    gemini_response = GeminiApartmentResponse(**response_data)
                    print(f"Manually parsed response: {gemini_response}")
                
                # Build response dict
                exists = gemini_response.exists
                apartment_ids = gemini_response.apartment_ids or []
                
                # If max tokens reached, set exists to False but keep apartment_ids
                if max_tokens_reached:
                    exists = False
                
                # Verify apartments actually exist in the list and populate data
                if exists and apartment_ids:
                    # AI said exists=True, verify and populate apartment data
                    found_apartments = []
                    for apt_id in apartment_ids:
                        for apt in apartments:
                            if apt.get("id") == apt_id:
                                found_apartments.append(apt)
                                break
                    
                    if found_apartments:
                        # Apartments exist, return basic info with status and qualification
                        print(f"Returning {len(found_apartments)} apartment(s): exists=True, apartment_ids={apartment_ids}")
                        basic_apartments = []
                        for apt in found_apartments:
                            # Filter qualification to only include allow_pets and minimum_salary
                            qualification = apt.get("qualification", {})
                            filtered_qualification = {}
                            if qualification:
                                if "allow_pets" in qualification:
                                    filtered_qualification["allow_pets"] = qualification["allow_pets"]
                                if "minimum_salary" in qualification:
                                    filtered_qualification["minimum_salary"] = qualification["minimum_salary"]
                            
                            basic_apartments.append({
                                "id": apt.get("id"),
                                "name": apt.get("name"),
                                "street": apt.get("street"),
                                "city": apt.get("city"),
                                "neighbourhood": apt.get("neighbourhood"),
                                "ref_code": apt.get("id"),
                                "price": apt.get("price"),
                                "available": apt.get("status") == "open",
                                "qualification": filtered_qualification if filtered_qualification else None
                            })
                        return {
                            "exists": True,
                            "apartments": basic_apartments,
                            "message": None
                        }
                    else:
                        # AI said exists but no apartments found in list
                        print(f"No apartments found: exists=False, apartment_ids={apartment_ids}")
                        return {
                            "exists": False,
                            "apartment_ids": apartment_ids,
                            "apartments": [],
                            "message": "No matching apartments found"
                        }
                else:
                    # AI said exists=False or no apartment_ids
                    print(f"No apartments found: exists=False, apartment_ids={apartment_ids}")
                    return {
                        "exists": False,
                        "apartment_ids": [],
                        "apartments": [],
                        "message": "No matching apartments found"
                    }
                
            except (json.JSONDecodeError, ValueError) as e:
                # Fallback: if JSON parsing fails, try to extract from text
                print(f"Failed to parse structured response: {e}")
                apartment_id_str = response.text.strip() if response.text else ""
                apartment_id = self._extract_apartment_id_with_fallback(apartment_id_str, apartments)
                
                exists = False
                found_apartments = []
                apartment_ids = []
                
                if apartment_id is not None:
                    apartment_ids = [apartment_id]
                    for apartment in apartments:
                        if apartment.get("id") == apartment_id:
                            exists = True
                            found_apartments = [apartment]
                            break
                
                # If max tokens reached, treat as not found
                if max_tokens_reached:
                    exists = False
                    found_apartments = []
                
                # Return response as dict with apartment data if found, or null with message if not
                if exists and found_apartments:
                    # Return basic info with status and qualification
                    basic_apartments = []
                    for apt in found_apartments:
                        # Filter qualification to only include allow_pets and minimum_salary
                        qualification = apt.get("qualification", {})
                        filtered_qualification = {}
                        if qualification:
                            if "allow_pets" in qualification:
                                filtered_qualification["allow_pets"] = qualification["allow_pets"]
                            if "minimum_salary" in qualification:
                                filtered_qualification["minimum_salary"] = qualification["minimum_salary"]
                        
                        basic_apartments.append({
                            "id": apt.get("id"),
                            "name": apt.get("name"),
                            "street": apt.get("street"),
                            "city": apt.get("city"),
                            "neighbourhood": apt.get("neighbourhood"),
                            "ref_code": apt.get("id"),
                            "price": apt.get("price"),
                            "available": apt.get("status") == "open",
                            "qualification": filtered_qualification if filtered_qualification else None
                        })
                    return {
                        "exists": True,
                        "apartments": basic_apartments,
                        "message": None
                    }
                else:
                    return {
                        "exists": False,
                        "apartments": [],
                        "message": "No matching apartments found"
                    }
        
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=f"Configuration error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error calling Gemini API: {str(e)}"
            )
    
    def _extract_apartment_id(self, response_text: str, apartments: List[Dict]) -> Optional[int]:
        """
        Extract apartment ID from LLM response (only valid IDs)
        
        Args:
            response_text: The text response from the LLM
            apartments: List of apartments to validate IDs against
            
        Returns:
            Valid apartment ID, or None if no valid ID found
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
        
        # Return None if no valid apartment ID found
        return None
    
    def _extract_apartment_id_with_fallback(self, response_text: str, apartments: List[Dict]) -> Optional[int]:
        """
        Extract apartment ID from LLM response (returns any number found, even if not in list)
        
        Args:
            response_text: The text response from the LLM
            apartments: List of apartments (used for validation, but will return ID even if not found)
            
        Returns:
            Apartment ID from response (even if not in list), or None if no number found
        """
        # Extract all numbers from the response
        numbers = re.findall(r'\d+', response_text)
        
        # Return the first number found (even if it doesn't exist in the list)
        for num_str in numbers:
            try:
                candidate_id = int(num_str)
                return candidate_id
            except ValueError:
                continue
        
        # Return None if no number found
        return None

