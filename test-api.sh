#!/bin/bash

# FastAPI Real Estate API - Test Script
# Replace YOUR_VERCEL_URL with your actual Vercel deployment URL
# Example: https://backend-real-estate-api.vercel.app

API_URL="${API_URL:-https://backend-real-estate-api.vercel.app}"

echo "Testing FastAPI Real Estate API at: $API_URL"
echo "================================================"
echo ""

# Test 1: Health Check
echo "1. Testing Health Check (GET /health)..."
curl -X GET "$API_URL/health" \
  -H "Content-Type: application/json" \
  -w "\nStatus Code: %{http_code}\n"
echo -e "\n"

# Test 2: Find Apartment
echo "2. Testing Find Apartment (POST /tool/find-apartment)..."
curl -X POST "$API_URL/tool/find-apartment" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I am looking for a 2 bedroom apartment near the beach in Miami"
  }' \
  -w "\nStatus Code: %{http_code}\n"
echo -e "\n"

# Test 3: Add User
echo "3. Testing Add User (POST /tool/add-user)..."
curl -X POST "$API_URL/tool/add-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123"
  }' \
  -w "\nStatus Code: %{http_code}\n"
echo -e "\n"

# Test 4: Add Appointment
echo "4. Testing Add Appointment (POST /tool/add-appointment)..."
curl -X POST "$API_URL/tool/add-appointment" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "appt_456"
  }' \
  -w "\nStatus Code: %{http_code}\n"
echo -e "\n"

echo "================================================"
echo "All tests completed!"
echo ""
echo "To use a different URL, set API_URL environment variable:"
echo "  export API_URL=https://your-custom-url.vercel.app"
echo "  ./test-api.sh"

