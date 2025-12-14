# Calendar Scoring System - Example

## Scenario Setup

**Today:** Tuesday, January 14, 2025  
**New Request:** Client wants to see **Piso B** (Apartment B)  
**Property Availability:** 
- Piso B: Only available Tuesdays and Thursdays (CRITICAL/Scarce - <10 hours/week)

## Current Calendar State (Before New Request)

```
WEEK: January 13-17, 2025

┌─────────────────────────────────────────────────────────────────┐
│ MONDAY 13                    TUESDAY 14 (TODAY)                │
├─────────────────────────────────────────────────────────────────┤
│ 09:00 - 09:30  FREE           09:00 - 09:30  FREE              │
│ 09:30 - 10:00  FREE           09:30 - 10:00  FREE              │
│ 10:00 - 10:30  FREE           10:00 - 10:30  Piso A (Client 1) │
│ 10:30 - 11:00  FREE           10:30 - 11:00  Piso A (Client 1) │
│ 11:00 - 11:30  FREE           11:00 - 11:30  FREE              │
│ 11:30 - 12:00  FREE           11:30 - 12:00  FREE              │
│ 12:00 - 12:30  FREE           12:00 - 12:30  FREE              │
│ 12:30 - 13:00  FREE           12:30 - 13:00  FREE              │
│ ────────────────── LUNCH ────────────────────                   │
│ 14:00 - 14:30  FREE           14:00 - 14:30  FREE              │
│ 14:30 - 15:00  FREE           14:30 - 15:00  FREE              │
│ 15:00 - 15:30  FREE           15:00 - 15:30  FREE              │
│ 15:30 - 16:00  FREE           15:30 - 16:00  FREE              │
│ 16:00 - 16:30  FREE           16:00 - 16:30  FREE              │
│ 16:30 - 17:00  FREE           16:30 - 17:00  FREE              │
│ 17:00 - 17:30  FREE           17:00 - 17:30  FREE              │
│ 17:30 - 18:00  FREE           17:30 - 18:00  FREE              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WEDNESDAY 15                  THURSDAY 16                       │
├─────────────────────────────────────────────────────────────────┤
│ 09:00 - 09:30  FREE           09:00 - 09:30  FREE              │
│ 09:30 - 10:00  FREE           09:30 - 10:00  FREE              │
│ 10:00 - 10:30  FREE           10:00 - 10:30  Piso B (Client 2) │
│ 10:30 - 11:00  FREE           10:30 - 11:00  Piso B (Client 2) │
│ 11:00 - 11:30  FREE           11:00 - 11:30  FREE              │
│ 11:30 - 12:00  FREE           11:30 - 12:00  FREE              │
│ 12:00 - 12:30  FREE           12:00 - 12:30  FREE              │
│ 12:30 - 13:00  FREE           12:30 - 13:00  FREE              │
│ ────────────────── LUNCH ────────────────────                   │
│ 14:00 - 14:30  FREE           14:00 - 14:30  FREE              │
│ 14:30 - 15:00  FREE           14:30 - 15:00  FREE              │
│ 15:00 - 15:30  FREE           15:00 - 15:30  FREE              │
│ 15:30 - 16:00  FREE           15:30 - 16:00  FREE              │
│ 16:00 - 16:30  FREE           16:00 - 16:30  FREE              │
│ 16:30 - 17:00  FREE           16:30 - 17:00  FREE              │
│ 17:00 - 17:30  FREE           17:00 - 17:30  FREE              │
│ 17:30 - 18:00  FREE           17:30 - 18:00  FREE              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ FRIDAY 17                                                       │
├─────────────────────────────────────────────────────────────────┤
│ 09:00 - 09:30  FREE                                            │
│ 09:30 - 10:00  FREE                                            │
│ 10:00 - 10:30  FREE                                            │
│ ... (all day FREE)                                             │
└─────────────────────────────────────────────────────────────────┘
```

**Notes:**
- Today (Tuesday): Morning has Piso A visit (10:00-11:00)
- Thursday: Morning has Piso B visit (10:00-11:00) - **Same property!**
- Piso B is CRITICAL (only available Tuesdays and Thursdays)

---

## New Request: Client wants to see Piso B

**Available options:**

### Option 1: Tuesday 14 (TODAY) - 09:30 (Morning, first slot)
### Option 2: Tuesday 14 (TODAY) - 16:00 (Afternoon, first slot)  
### Option 3: Thursday 16 - 10:30 (Adjacent to existing Piso B visit)
### Option 4: Thursday 16 - 09:30 (Morning, first slot)

---

## Scoring Calculations

### Option 1: Tuesday 14 - 09:30 (TODAY Morning)

**Analysis:**
- ✅ **Urgencia HOY**: +50 (Only TODAY bonus)
- ✅ **Efecto Ancla**: +20 (First slot of morning - 09:30)
- ✅ **Bloque Limpio**: +10 (Morning is mostly empty except 10:00-11:00)
- ❌ **Cambio Intra-Turno**: -50 (Changing from Piso A at 10:00 to different property mid-morning)
- ❌ **Canibalización**: 0 (Not using exclusive day)
- ✅ **Property scarcity**: 0 (Not penalizing scarce property usage)

**Calculation:**
```
+50 (Urgencia HOY)
+20 (Efecto Ancla)
+10 (Bloque Limpio - morning mostly free)
-50 (Cambio Intra-Turno - different property after 10:00)
─────────────────────
= +30 PUNTOS
```

**Result:** ⚠️ **+30 points** - Penalized for changing properties mid-morning

---

### Option 2: Tuesday 14 - 16:00 (TODAY Afternoon)

**Analysis:**
- ✅ **Urgencia HOY**: +50 (Only TODAY bonus)
- ✅ **Efecto Ancla**: +20 (First slot of afternoon - 16:00)
- ✅ **Bloque Limpio**: +10 (Afternoon is completely empty)
- ✅ **Cambio de Turno**: -10 (Changing property after lunch break)
- ❌ **Canibalización**: 0 (Not using exclusive day)

**Calculation:**
```
+50 (Urgencia HOY)
+20 (Efecto Ancla)
+10 (Bloque Limpio - afternoon completely free)
-10 (Cambio de Turno - different property after lunch)
─────────────────────
= +70 PUNTOS
```

**Result:** 🥇 **+70 points** - BEST option for TODAY

---

### Option 3: Thursday 16 - 10:30 (Adjacent to existing Piso B visit)

**Analysis:**
- ❌ **Urgencia HOY**: 0 (Not today)
- ❌ **Efecto Ancla**: 0 (Not first slot)
- ❌ **Bloque Limpio**: 0 (Morning has visit at 10:00-11:00)
- ✅ **Cluster Perfecto**: +100 (Adjacent to existing Piso B visit - MAXIMUM EFFICIENCY!)
- ❌ **Canibalización**: 0 (Not using exclusive day)

**Calculation:**
```
+100 (Cluster Perfecto - adjacent to same property visit)
─────────────────────
= +100 PUNTOS
```

**Result:** 🏆 **+100 points** - BEST OVERALL (efficiency wins!)

---

### Option 4: Thursday 16 - 09:30 (Morning, first slot)

**Analysis:**
- ❌ **Urgencia HOY**: 0 (Not today)
- ✅ **Efecto Ancla**: +20 (First slot of morning - 09:30)
- ❌ **Bloque Limpio**: 0 (Morning has visit at 10:00-11:00)
- ❌ **Canibalización**: 0 (Not using exclusive day)

**Calculation:**
```
+20 (Efecto Ancla)
─────────────────────
= +20 PUNTOS
```

**Result:** ⚠️ **+20 points** - Decent but not optimal

---

## Final Ranking & Recommendation

```
Rank  Score  Option                     Reason
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1    +100   Thursday 16 - 10:30       Cluster Perfecto (efficiency!)
 2    +70    Tuesday 14 - 16:00        Urgencia HOY + afternoon clean
 3    +30    Tuesday 14 - 09:30        Urgencia HOY but intra-turno penalty
 4    +20    Thursday 16 - 09:30       Only Efecto Ancla
```

---

## AI Response Examples

### If choosing Option 1 (Cluster Perfecto - Thursday):
```
"I see you're interested in Piso B. I have a viewing session for that 
same property on Thursday morning at 10:00. Would you be able to join 
that session at 10:30? This way we can maximize efficiency and you can 
see the property with another interested client."
```

### If choosing Option 2 (TODAY afternoon):
```
"Great news! I have availability TODAY afternoon. Would 16:00 work for 
you? It's the first slot of the afternoon, and I have the rest of the 
afternoon free, so we won't be rushed."
```

### If TODAY is critical but efficiency matters:
```
"Perfect timing! I have two great options for you:

1. TODAY at 16:00 - immediate viewing
2. Thursday at 10:30 - I'm already showing Piso B to another client 
   at 10:00, so this would be very efficient for me

Which works better for you?"
```

---

## Alternative Scenario: Property Conflict

### If Piso B was also scheduled on Tuesday 14 at 16:00:

**Option:** Thursday 16 - 10:30 (Cluster)

**New Calculation:**
```
+100 (Cluster Perfecto)
-200 (Canibalización - trying to use Tuesday exclusive slot that's already taken)
─────────────────────
= -100 PUNTOS ❌ REJECTED
```

**AI Response:**
```
"I'm sorry, but Tuesday at 16:00 is already booked for Piso B. However, 
I have availability on Thursday at 10:30, right after another viewing 
of the same property at 10:00. This would be perfect - we can do both 
viewings efficiently. Does Thursday work for you?"
```

---

## Key Insights from This Example

1. **Cluster Perfecto (+100) beats Urgencia HOY (+50)** - Efficiency is prioritized over urgency if the difference is significant
2. **TODAY bonus only applies to TODAY** - Tomorrow gets no time bonus
3. **Changing properties mid-session gets penalized** - Intra-turno (-50) is worse than cambio turno (-10)
4. **First slots are always good** - Efecto Ancla (+20) is consistent
5. **Clean blocks are rewarded** - Empty morning/afternoon gets +10

