# API Testing Commands

Quick curl commands to test your FastAPI endpoints. Replace `YOUR_VERCEL_URL` with your actual deployment URL (e.g., `https://backend-real-estate-api.vercel.app`).

## Health Check

```bash
curl -X GET "YOUR_VERCEL_URL/health"
```

## Find Apartment

```bash
curl -X POST "YOUR_VERCEL_URL/tool/find-apartment" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I am looking for a 2 bedroom apartment near the beach in Miami"
  }'
```

## Add User

```bash
curl -X POST "YOUR_VERCEL_URL/tool/add-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123"
  }'
```

## Add Appointment

```bash
curl -X POST "YOUR_VERCEL_URL/tool/add-appointment" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "appt_456"
  }'
```

## Test Script

You can also use the provided test script:

```bash
# Make it executable
chmod +x test-api.sh

# Run with default URL
./test-api.sh

# Or with custom URL
export API_URL=https://your-custom-url.vercel.app
./test-api.sh
```

