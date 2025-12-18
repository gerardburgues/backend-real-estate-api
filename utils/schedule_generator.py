import random
from datetime import datetime, timedelta
from typing import Dict, List

# Seed for consistent mock data across requests
SCHEDULE_SEED = 42

def generate_all_schedules(apartments: List[dict]) -> Dict[int, List[str]]:
    """
    Generate busy slots for all apartments.
    Returns a dict mapping apartment_id -> list of busy slot strings.
    """
    random.seed(SCHEDULE_SEED)
    
    schedules = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for apt in apartments:
        apt_id = apt.get("id")
        busy_slots = []
        
        # Generate slots for 7 days
        for day_offset in range(7):
            current_day = today + timedelta(days=day_offset)
            
            # Generate slots from 9:00 to 18:00 (30-min intervals)
            # 9:00, 9:30, 10:00, ... 17:30 = 18 slots per day
            for hour in range(9, 18):
                for minute in [0, 30]:
                    slot_time = current_day.replace(hour=hour, minute=minute)
                    slot_str = slot_time.strftime("%d-%m-%Y %H:%M")
                    
                    # Randomly mark ~40% of slots as busy
                    if random.random() < 0.4:
                        busy_slots.append(slot_str)
        
        schedules[apt_id] = busy_slots
    
    return schedules


def get_available_slots(apartment_id: int, apartments: List[dict]) -> List[str]:
    """
    Get available (free) slots for a specific apartment.
    """
    all_schedules = generate_all_schedules(apartments)
    busy_slots = set(all_schedules.get(apartment_id, []))
    
    available_slots = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Generate all possible slots for 7 days
    for day_offset in range(7):
        current_day = today + timedelta(days=day_offset)
        
        for hour in range(9, 18):
            for minute in [0, 30]:
                slot_time = current_day.replace(hour=hour, minute=minute)
                slot_str = slot_time.strftime("%d-%m-%Y %H:%M")
                
                if slot_str not in busy_slots:
                    available_slots.append(slot_str)
    
    return available_slots


def get_all_busy_schedules_for_html(apartments: List[dict]) -> Dict[int, dict]:
    """
    Get busy schedules formatted for HTML display.
    Returns dict with apartment info and busy slots organized by date.
    """
    all_schedules = generate_all_schedules(apartments)
    
    result = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for apt in apartments:
        apt_id = apt.get("id")
        apt_name = apt.get("name")
        busy_slots = set(all_schedules.get(apt_id, []))
        
        # Organize by date
        days_data = {}
        for day_offset in range(7):
            current_day = today + timedelta(days=day_offset)
            day_key = current_day.strftime("%d-%m-%Y")
            day_label = current_day.strftime("%a %d")
            
            slots = []
            for hour in range(9, 18):
                for minute in [0, 30]:
                    slot_time = current_day.replace(hour=hour, minute=minute)
                    slot_str = slot_time.strftime("%d-%m-%Y %H:%M")
                    time_label = slot_time.strftime("%H:%M")
                    
                    slots.append({
                        "time": time_label,
                        "busy": slot_str in busy_slots
                    })
            
            days_data[day_key] = {
                "label": day_label,
                "slots": slots
            }
        
        result[apt_id] = {
            "name": apt_name,
            "city": apt.get("city"),
            "days": days_data
        }
    
    return result

