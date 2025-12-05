# Quick API Test Commands

Your API is deployed at: **https://backend-real-estate-api-an4a.vercel.app**

## ✅ Test 1: Health Check

```bash
curl https://backend-real-estate-api-an4a.vercel.app/health
```

Expected response:
```json
{"status":"healthy"}
```

## ✅ Test 2: View API Documentation

Open in browser:
```
https://backend-real-estate-api-an4a.vercel.app/docs
```

This will show the interactive Swagger UI where you can test all endpoints.

## ✅ Test 3: Find Apartment (requires GEMINI_API_KEY)

```bash
curl -X POST "https://backend-real-estate-api-an4a.vercel.app/tool/find-apartment" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I am looking for a 2 bedroom apartment near the beach in Miami"
  }'
```

## ✅ Test 4: Add User

```bash
curl -X POST "https://backend-real-estate-api-an4a.vercel.app/tool/add-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123"
  }'
```

Expected response:
```json
{"status":"success","message":"added user to app"}
```

## ✅ Test 5: Add Appointment

```bash
curl -X POST "https://backend-real-estate-api-an4a.vercel.app/tool/add-appointment" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "appt_456"
  }'
```

Expected response:
```json
{"status":"success","message":"added appointment to calendar"}
```

## 🎯 Quick Verification Checklist

- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] `/docs` page loads in browser
- [ ] Add User endpoint works (doesn't need API key)
- [ ] Add Appointment endpoint works (doesn't need API key)
- [ ] Find Apartment endpoint works (if GEMINI_API_KEY is configured)

If the Find Apartment endpoint returns an error about missing API key, make sure you added `GEMINI_API_KEY` in Vercel's Environment Variables.

