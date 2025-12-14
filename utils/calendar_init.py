"""
Calendar initialization utility

Creates mock calendar data using the top 3 apartments from apartments.json.
"""
from datetime import date, timedelta
from services.calendar_service import calendar_service
from utils.apartment_loader import load_apartments


def init_mock_calendar():
    """
    Initialize the calendar with mock data using the top 3 apartments.
    
    Scenario:
    - Tuesday: Apartment 1001 (Apartamento Moderno en la Rambla) at 10:00-11:00
    - Thursday: Apartment 1003 (Suite de Lujo en Diagonal) at 10:00-11:00
    - Wednesday: Apartment 1004 (Apartamento Empresarial en Diagonal) at 14:00-15:00
    """
    # Load apartments to get the top 3
    apartments = load_apartments()
    top_3_apartments = apartments[:3] if len(apartments) >= 3 else apartments
    
    if len(top_3_apartments) < 3:
        print(f"Warning: Only {len(top_3_apartments)} apartments found, expected at least 3")
        return
    
    apt_1 = top_3_apartments[0]  # ID 1001
    apt_2 = top_3_apartments[1]  # ID 1003
    apt_3 = top_3_apartments[2]  # ID 1004
    
    today = date.today()
    
    # Find Tuesday of current week
    days_until_tuesday = (1 - today.weekday()) % 7
    if days_until_tuesday == 0 and today.weekday() != 1:
        days_until_tuesday = 7
    tuesday = today + timedelta(days=days_until_tuesday)
    
    # Find Wednesday of current week
    days_until_wednesday = (2 - today.weekday()) % 7
    if days_until_wednesday == 0 and today.weekday() != 2:
        days_until_wednesday = 7
    wednesday = today + timedelta(days=days_until_wednesday)
    
    # Find Thursday of current week
    days_until_thursday = (3 - today.weekday()) % 7
    if days_until_thursday == 0 and today.weekday() != 3:
        days_until_thursday = 7
    thursday = today + timedelta(days=days_until_thursday)
    
    # Add appointments
    # Tuesday: Apartment 1001 (Apartamento Moderno en la Rambla) at 10:00-11:00
    calendar_service.add_appointment(
        date_str=tuesday.isoformat(),
        time_slot="10:00",
        apartment_id=apt_1["id"],
        client_id="client_1"
    )
    calendar_service.add_appointment(
        date_str=tuesday.isoformat(),
        time_slot="10:30",
        apartment_id=apt_1["id"],
        client_id="client_1"
    )
    
    # Wednesday: Apartment 1004 (Apartamento Empresarial en Diagonal) at 14:00-15:00
    calendar_service.add_appointment(
        date_str=wednesday.isoformat(),
        time_slot="14:00",
        apartment_id=apt_3["id"],
        client_id="client_3"
    )
    calendar_service.add_appointment(
        date_str=wednesday.isoformat(),
        time_slot="14:30",
        apartment_id=apt_3["id"],
        client_id="client_3"
    )
    
    # Thursday: Apartment 1003 (Suite de Lujo en Diagonal) at 10:00-11:00
    calendar_service.add_appointment(
        date_str=thursday.isoformat(),
        time_slot="10:00",
        apartment_id=apt_2["id"],
        client_id="client_2"
    )
    calendar_service.add_appointment(
        date_str=thursday.isoformat(),
        time_slot="10:30",
        apartment_id=apt_2["id"],
        client_id="client_2"
    )
    
    # Set property metadata based on apartment characteristics
    # Apartment 1001: Abundant (available all week) - lower price, more accessible
    calendar_service.set_property_metadata(
        apartment_id=apt_1["id"],
        available_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        hours_per_week=35,
        scarcity_level="abundant"
    )
    
    # Apartment 1003: Critical (only Tuesday and Thursday) - luxury apartment, limited availability
    calendar_service.set_property_metadata(
        apartment_id=apt_2["id"],
        available_days=["Tuesday", "Thursday"],
        hours_per_week=8,
        scarcity_level="critical"
    )
    
    # Apartment 1004: Medium (Monday, Wednesday, Friday) - business apartment, moderate availability
    calendar_service.set_property_metadata(
        apartment_id=apt_3["id"],
        available_days=["Monday", "Wednesday", "Friday"],
        hours_per_week=20,
        scarcity_level="medium"
    )
    
    print(f"Calendar initialized with top 3 apartments:")
    print(f"  - {apt_1['name']} (ID: {apt_1['id']}) - Tuesday at 10:00")
    print(f"  - {apt_2['name']} (ID: {apt_2['id']}) - Thursday at 10:00")
    print(f"  - {apt_3['name']} (ID: {apt_3['id']}) - Wednesday at 14:00")


if __name__ == "__main__":
    init_mock_calendar()

