# Check Schedule API Documentation

## Endpoint

`POST /tool/check-schedule`

## Description

Checks the calendar for available time slots for a specific property and returns a scored list of options. The scoring system prioritizes efficiency and agent convenience based on the rules defined in the Notion document.

## Request

```json
{
  "apartment_id": 2,
  "start_date": "2025-01-14",  // Optional, defaults to today (ISO format: YYYY-MM-DD)
  "days": 7                     // Optional, defaults to 7 days ahead
}
```

### Request Parameters

- `apartment_id` (required, int): The ID of the property to check schedule for
- `start_date` (optional, string): Start date for search in ISO format (YYYY-MM-DD). Defaults to today
- `days` (optional, int): Number of days to search ahead. Defaults to 7

## Response

```json
{
  "apartment_id": 2,
  "total_available": 45,
  "best_option": {
    "date": "2025-01-16",
    "time": "10:30",
    "is_today": false,
    "score": 100,
    "breakdown": {
      "cluster_perfecto": 100,
      "urgencia_hoy": 0,
      "efecto_ancla": 0,
      "bloque_limpio": 0,
      "cambio_turno": 0,
      "cambio_intra_turno": 0,
      "romper_dia": 0,
      "canibalizacion": 0
    }
  },
  "available_slots": [
    {
      "date": "2025-01-16",
      "time": "10:30",
      "is_today": false,
      "score": 100,
      "breakdown": {
        "cluster_perfecto": 100,
        "urgencia_hoy": 0,
        "efecto_ancla": 0,
        "bloque_limpio": 0,
        "cambio_turno": 0,
        "cambio_intra_turno": 0,
        "romper_dia": 0,
        "canibalizacion": 0
      }
    },
    {
      "date": "2025-01-14",
      "time": "16:00",
      "is_today": true,
      "score": 70,
      "breakdown": {
        "cluster_perfecto": 0,
        "urgencia_hoy": 50,
        "efecto_ancla": 20,
        "bloque_limpio": 10,
        "cambio_turno": -10,
        "cambio_intra_turno": 0,
        "romper_dia": 0,
        "canibalizacion": 0
      }
    }
    // ... more slots sorted by score (highest first)
  ]
}
```

### Response Fields

- `apartment_id` (int): The property ID that was queried
- `total_available` (int): Total number of available slots found
- `best_option` (AvailableSlot, nullable): The slot with the highest score
- `available_slots` (array): List of all available slots, sorted by score (highest first)

#### AvailableSlot Object

- `date` (string): Date in ISO format (YYYY-MM-DD)
- `time` (string): Time slot in HH:MM format
- `is_today` (boolean): Whether this slot is today
- `score` (int): Total score for this slot
- `breakdown` (object): Score breakdown showing individual components

#### Score Breakdown

The breakdown shows how the score was calculated:

- `cluster_perfecto` (+100): Adjacent to a visit of the same property (maximum efficiency)
- `urgencia_hoy` (+50): Only time-based bonus - applies only if slot is TODAY
- `efecto_ancla` (+20): First slot of morning (09:30) or afternoon (16:00)
- `bloque_limpio` (+10): Morning or afternoon completely empty
- `cambio_turno` (-10): Changing property after lunch (16:00)
- `cambio_intra_turno` (-50): Changing property mid-morning/afternoon
- `romper_dia` (-80): Isolated slot (e.g., 13:00)
- `canibalizacion` (-200): Using exclusive day slot for normal property

## Example Usage

### Using curl

```bash
curl -X POST "http://localhost:8000/tool/check-schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "apartment_id": 2,
    "days": 7
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/tool/check-schedule",
    json={
        "apartment_id": 2,
        "start_date": "2025-01-14",
        "days": 7
    }
)

data = response.json()
print(f"Best option: {data['best_option']['date']} at {data['best_option']['time']}")
print(f"Score: {data['best_option']['score']}")
```

## Error Responses

### 404 - Apartment Not Found

```json
{
  "detail": "Apartment with ID 999 not found"
}
```

### 400 - Invalid Date Format

```json
{
  "detail": "Invalid date format. Expected YYYY-MM-DD, got 2025/01/14"
}
```

## Scoring System Overview

The scoring system prioritizes:

1. **Efficiency** (Cluster Perfecto): Grouping visits to the same property together
2. **Urgency** (only TODAY): Selling today is the only thing that justifies bothering the agent
3. **Convenience**: First slots and clean blocks are preferred
4. **Avoid penalties**: Minimize property changes, isolated slots, etc.

**Key principle**: Only TODAY gets a time bonus (+50). Tomorrow and later days don't get urgency points, reducing pressure to prioritize tomorrow when later dates are logistically better.

## Notes

- Time slots are 30 minutes each
- Working hours: 09:00-13:00 (morning), 14:00-18:00 (afternoon)
- Lunch break: 13:00-14:00 (no slots available)
- First slots: 09:30 (morning), 16:00 (afternoon)

