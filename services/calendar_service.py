"""
Calendar Service with Scoring Logic

Implements the scoring system from the Notion document:
- Cluster Perfecto: +100 (adjacent to same property visit)
- Urgencia HOY: +50 (only for TODAY)
- Efecto Ancla: +20 (first slot of morning/afternoon)
- Bloque Limpio: +10 (completely empty morning/afternoon)
- Cambio de Turno: -10 (changing property after lunch)
- Cambio Intra-Turno: -50 (changing property mid-morning/afternoon)
- Romper el Día: -80 (isolated slot)
- Canibalización: -200 (using exclusive day for normal property)
"""
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Scoring constants
SCORE_CLUSTER_PERFECTO = 100
SCORE_URGENCIA_HOY = 50
SCORE_EFECTO_ANCLA = 20
SCORE_BLOQUE_LIMPIO = 10
SCORE_CAMBIO_TURNO = -10
SCORE_CAMBIO_INTRA_TURNO = -50
SCORE_ROMPER_DIA = -80
SCORE_CANIBALIZACION = -200

# Time slots configuration
MORNING_START = "09:00"
MORNING_END = "13:00"
AFTERNOON_START = "14:00"
AFTERNOON_END = "18:00"
LUNCH_START = "13:00"
LUNCH_END = "14:00"

# First slots of morning/afternoon
FIRST_MORNING_SLOT = "09:30"
FIRST_AFTERNOON_SLOT = "16:00"


class CalendarService:
    """Service for managing calendar and scoring available time slots"""
    
    def __init__(self):
        # In-memory calendar storage
        # Structure: {date: {time_slot: appointment}}
        self.appointments: Dict[str, Dict[str, Dict]] = {}
        # Property availability metadata
        # Structure: {property_id: {available_days: [], hours_per_week: int, scarcity_level: str}}
        self.property_metadata: Dict[int, Dict] = {}
    
    def get_time_slots(self, start_date: date, days: int = 7) -> List[str]:
        """Generate time slots for a given date range"""
        slots = []
        current_time = datetime.strptime(MORNING_START, "%H:%M").time()
        end_time = datetime.strptime(AFTERNOON_END, "%H:%M").time()
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            # Skip lunch break
            if time_str >= LUNCH_START and time_str < LUNCH_END:
                current_time = datetime.strptime(AFTERNOON_START, "%H:%M").time()
                continue
            
            slots.append(time_str)
            current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=30)).time()
        
        return slots
    
    def get_appointments_for_date(self, date_str: str) -> Dict[str, Dict]:
        """Get all appointments for a specific date"""
        return self.appointments.get(date_str, {})
    
    def add_appointment(self, date_str: str, time_slot: str, apartment_id: int, client_id: Optional[str] = None):
        """Add an appointment to the calendar"""
        if date_str not in self.appointments:
            self.appointments[date_str] = {}
        
        self.appointments[date_str][time_slot] = {
            "apartment_id": apartment_id,
            "client_id": client_id,
            "date": date_str,
            "time": time_slot
        }
        logger.info(f"Added appointment: {date_str} {time_slot} - Apartment {apartment_id}", extra={"auth_id": "system"})
    
    def is_slot_available(self, date_str: str, time_slot: str) -> bool:
        """Check if a time slot is available"""
        appointments = self.get_appointments_for_date(date_str)
        return time_slot not in appointments
    
    def get_adjacent_appointments(self, date_str: str, time_slot: str, apartment_id: int) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Get appointments immediately before and after the given time slot for the same apartment"""
        appointments = self.get_appointments_for_date(date_str)
        slots = sorted(self.get_time_slots(date.fromisoformat(date_str), 1))
        
        try:
            current_index = slots.index(time_slot)
        except ValueError:
            return None, None
        
        prev_appt = None
        next_appt = None
        
        # Check previous slot
        if current_index > 0:
            prev_slot = slots[current_index - 1]
            prev_appt = appointments.get(prev_slot)
            if prev_appt and prev_appt.get("apartment_id") == apartment_id:
                pass  # Found adjacent appointment before
            else:
                prev_appt = None
        
        # Check next slot
        if current_index < len(slots) - 1:
            next_slot = slots[current_index + 1]
            next_appt = appointments.get(next_slot)
            if next_appt and next_appt.get("apartment_id") == apartment_id:
                pass  # Found adjacent appointment after
            else:
                next_appt = None
        
        return prev_appt, next_appt
    
    def is_cluster_perfecto(self, date_str: str, time_slot: str, apartment_id: int) -> bool:
        """Check if slot is adjacent to another visit of the same property"""
        prev_appt, next_appt = self.get_adjacent_appointments(date_str, time_slot, apartment_id)
        return prev_appt is not None or next_appt is not None
    
    def is_efecto_ancla(self, time_slot: str) -> bool:
        """Check if slot is the first slot of morning or afternoon"""
        return time_slot == FIRST_MORNING_SLOT or time_slot == FIRST_AFTERNOON_SLOT
    
    def is_bloque_limpio(self, date_str: str, time_slot: str, period: str) -> bool:
        """Check if the morning or afternoon block is completely empty"""
        appointments = self.get_appointments_for_date(date_str)
        slots = self.get_time_slots(date.fromisoformat(date_str), 1)
        
        if period == "morning":
            period_slots = [s for s in slots if MORNING_START <= s < LUNCH_START]
        else:  # afternoon
            period_slots = [s for s in slots if AFTERNOON_START <= s <= AFTERNOON_END]
        
        # Check if any slot in the period has an appointment
        for slot in period_slots:
            if slot in appointments:
                return False
        
        return True
    
    def get_period(self, time_slot: str) -> str:
        """Get period (morning/afternoon) for a time slot"""
        if MORNING_START <= time_slot < LUNCH_START:
            return "morning"
        elif AFTERNOON_START <= time_slot <= AFTERNOON_END:
            return "afternoon"
        return "unknown"
    
    def has_appointment_in_period(self, date_str: str, period: str, exclude_slot: Optional[str] = None) -> bool:
        """Check if there are appointments in a period"""
        appointments = self.get_appointments_for_date(date_str)
        slots = self.get_time_slots(date.fromisoformat(date_str), 1)
        
        if period == "morning":
            period_slots = [s for s in slots if MORNING_START <= s < LUNCH_START]
        else:  # afternoon
            period_slots = [s for s in slots if AFTERNOON_START <= s <= AFTERNOON_END]
        
        for slot in period_slots:
            if slot == exclude_slot:
                continue
            if slot in appointments:
                return True
        
        return False
    
    def has_different_property_in_period(self, date_str: str, period: str, apartment_id: int, exclude_slot: Optional[str] = None) -> bool:
        """Check if there are appointments for different properties in a period"""
        appointments = self.get_appointments_for_date(date_str)
        slots = self.get_time_slots(date.fromisoformat(date_str), 1)
        
        if period == "morning":
            period_slots = [s for s in slots if MORNING_START <= s < LUNCH_START]
        else:  # afternoon
            period_slots = [s for s in slots if AFTERNOON_START <= s <= AFTERNOON_END]
        
        for slot in period_slots:
            if slot == exclude_slot:
                continue
            appt = appointments.get(slot)
            if appt and appt.get("apartment_id") != apartment_id:
                return True
        
        return False
    
    def is_romper_dia(self, date_str: str, time_slot: str) -> bool:
        """Check if slot breaks the day (isolated slot)"""
        appointments = self.get_appointments_for_date(date_str)
        slots = self.get_time_slots(date.fromisoformat(date_str), 1)
        
        try:
            current_index = slots.index(time_slot)
        except ValueError:
            return False
        
        # Check if it's isolated (no appointments before or after in the same period)
        period = self.get_period(time_slot)
        has_before = False
        has_after = False
        
        # Check slots before in same period
        for i in range(current_index - 1, -1, -1):
            if self.get_period(slots[i]) != period:
                break
            if slots[i] in appointments:
                has_before = True
                break
        
        # Check slots after in same period
        for i in range(current_index + 1, len(slots)):
            if self.get_period(slots[i]) != period:
                break
            if slots[i] in appointments:
                has_after = True
                break
        
        # Isolated if it has appointments both before and after, or it's surrounded by appointments
        if has_before and has_after:
            return True
        
        return False
    
    def score_slot(
        self,
        date_str: str,
        time_slot: str,
        apartment_id: int,
        is_today: bool
    ) -> Dict:
        """
        Score a time slot based on all criteria
        
        Returns:
            Dict with score breakdown and total score
        """
        breakdown = {
            "cluster_perfecto": 0,
            "urgencia_hoy": 0,
            "efecto_ancla": 0,
            "bloque_limpio": 0,
            "cambio_turno": 0,
            "cambio_intra_turno": 0,
            "romper_dia": 0,
            "canibalizacion": 0
        }
        
        # Cluster Perfecto: +100
        if self.is_cluster_perfecto(date_str, time_slot, apartment_id):
            breakdown["cluster_perfecto"] = SCORE_CLUSTER_PERFECTO
        
        # Urgencia HOY: +50 (only for today)
        if is_today:
            breakdown["urgencia_hoy"] = SCORE_URGENCIA_HOY
        
        # Efecto Ancla: +20 (first slot of morning/afternoon)
        if self.is_efecto_ancla(time_slot):
            breakdown["efecto_ancla"] = SCORE_EFECTO_ANCLA
        
        # Bloque Limpio: +10 (completely empty morning/afternoon)
        period = self.get_period(time_slot)
        if self.is_bloque_limpio(date_str, time_slot, period):
            breakdown["bloque_limpio"] = SCORE_BLOQUE_LIMPIO
        
        # Cambio de Turno: -10 (changing property after lunch)
        if period == "afternoon" and time_slot == FIRST_AFTERNOON_SLOT:
            if self.has_different_property_in_period(date_str, "morning", apartment_id):
                breakdown["cambio_turno"] = SCORE_CAMBIO_TURNO
        
        # Cambio Intra-Turno: -50 (changing property mid-morning/afternoon)
        # This applies when there's a different property appointment in the same period
        # and this slot is not the first slot of the period
        appointments = self.get_appointments_for_date(date_str)
        slots = self.get_time_slots(date.fromisoformat(date_str), 1)
        
        try:
            current_index = slots.index(time_slot)
        except ValueError:
            current_index = -1
        
        if current_index >= 0:
            # Check if there's a different property in the same period BEFORE this slot
            has_different_before = False
            for i in range(current_index):
                if i < len(slots):
                    slot = slots[i]
                    if self.get_period(slot) != period:
                        break
                    appt = appointments.get(slot)
                    if appt and appt.get("apartment_id") != apartment_id:
                        has_different_before = True
                        break
            
            # Only penalize if there's a different property before AND it's not the first slot
            if has_different_before and not self.is_efecto_ancla(time_slot):
                breakdown["cambio_intra_turno"] = SCORE_CAMBIO_INTRA_TURNO
        
        # Romper el Día: -80 (isolated slot)
        if self.is_romper_dia(date_str, time_slot):
            breakdown["romper_dia"] = SCORE_ROMPER_DIA
        
        # Canibalización: -200 (using exclusive day for normal property)
        # This would require property metadata to determine if it's an exclusive day
        # For now, we'll skip this as it requires property availability configuration
        
        total_score = sum(breakdown.values())
        
        return {
            "score": total_score,
            "breakdown": breakdown
        }
    
    def find_available_slots(
        self,
        apartment_id: int,
        start_date: Optional[date] = None,
        days: int = 7
    ) -> List[Dict]:
        """
        Find all available slots for a property and score them
        
        Args:
            apartment_id: Property ID to find slots for
            start_date: Start date for search (defaults to today)
            days: Number of days to search ahead
        
        Returns:
            List of available slots with scores, sorted by score (highest first)
        """
        if start_date is None:
            start_date = date.today()
        
        today = date.today()
        available_slots = []
        all_slots = self.get_time_slots(start_date, days)
        
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)
            date_str = current_date.isoformat()
            is_today = current_date == today
            
            # Get appointments for this date
            appointments = self.get_appointments_for_date(date_str)
            
            # Check each time slot
            for time_slot in all_slots:
                # Skip if slot is already booked
                if time_slot in appointments:
                    continue
                
                # Score the slot
                scoring_result = self.score_slot(date_str, time_slot, apartment_id, is_today)
                
                available_slots.append({
                    "date": date_str,
                    "time": time_slot,
                    "is_today": is_today,
                    "score": scoring_result["score"],
                    "breakdown": scoring_result["breakdown"]
                })
        
        # Sort by score (highest first)
        available_slots.sort(key=lambda x: x["score"], reverse=True)
        
        return available_slots
    
    def set_property_metadata(
        self,
        apartment_id: int,
        available_days: List[str],
        hours_per_week: int,
        scarcity_level: str
    ):
        """Set property availability metadata"""
        self.property_metadata[apartment_id] = {
            "available_days": available_days,
            "hours_per_week": hours_per_week,
            "scarcity_level": scarcity_level
        }


# Global calendar service instance
calendar_service = CalendarService()

