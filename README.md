# Real Estate Tool Calls API

FastAPI application for Vapi integration with three tool call endpoints for real estate operations.

## Features

- **Find Apartment**: Uses Google Gemini LLM to intelligently match user queries with available apartments
- **Add User**: Simple endpoint to add users to the application
- **Add Appointment**: Simple endpoint to add appointments to calendar

## Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- Google Gemini API Key

### Local Development

1. Clone the repository and navigate to the project directory

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t real-estate-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e GEMINI_API_KEY=your_api_key_here real-estate-api
```

Or use Docker Compose:
```bash
# Set GEMINI_API_KEY in .env file first
docker-compose up --build
```

## API Endpoints

### POST /tool/find-apartment

Find the best matching apartment based on user query using Gemini LLM.

**Request Body:**
```json
{
  "query": "I'm looking for a 2 bedroom apartment near the beach in Miami"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Sunset View Apartments",
  "street": "123 Ocean Boulevard",
  "city": "Miami",
  "state": "FL",
  "zipcode": "33139",
  "price": 2500,
  "bedrooms": 2,
  "bathrooms": 2,
  "sqft": 1200,
  "description": "Beautiful ocean view apartment with modern amenities"
}
```

### POST /tool/add-user

Add a user to the application.

**Request Body:**
```json
{
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "added user to app"
}
```

### POST /tool/add-appointment

Add an appointment to the calendar.

**Request Body:**
```json
{
  "appointment_id": "optional_appointment_id"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "added appointment to calendar"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Apartments Data

Apartments are stored in `apartments.json`. You can modify this file to add, remove, or update apartment listings. The file contains an array of apartment objects with the following fields:

- `id`: Unique identifier
- `name`: Apartment complex name
- `street`: Street address
- `city`: City name
- `state`: State abbreviation
- `zipcode`: ZIP code
- `price`: Monthly rent price
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `sqft`: Square footage
- `description`: Apartment description

## Environment Variables

- `GEMINI_API_KEY`: Required. Your Google Gemini API key
- `PORT`: Optional. Server port (default: 8000)

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing with Streamlit

A Streamlit app is included in the `frontend/` folder for easy local testing of all endpoints:

1. Make sure the FastAPI server is running:
```bash
python app.py
# or
python main.py
```

2. In a separate terminal, run the Streamlit app:
```bash
cd frontend
streamlit run app.py
```

3. The app will open in your browser at `http://localhost:8501`

The Streamlit app provides:
- Text field for entering apartment search queries
- Buttons to test all four endpoints (Find Apartment, Add User, Add Appointment, Health Check)
- Response viewer showing request/response data
- Configurable API base URL in the sidebar

**Note:** The Streamlit frontend is for local development only and is not deployed to Vercel.

## Vapi Integration

This API is designed to work with Vapi for voice AI conversations. Each endpoint can be registered as a tool in your Vapi configuration.

