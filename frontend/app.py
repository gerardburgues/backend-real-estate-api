import streamlit as st
import requests
import json

st.set_page_config(page_title="Real Estate API Tester", page_icon="🏠", layout="wide")

st.title("🏠 Real Estate Tool Calls API Tester")
st.markdown("Test the FastAPI endpoints for Vapi integration")

# API Base URL
api_url = st.sidebar.text_input("API Base URL", value="http://localhost:8000", help="Change this if your API is running on a different host/port")

# Initialize session state for responses
if "responses" not in st.session_state:
    st.session_state.responses = []

def make_request(endpoint, method="POST", data=None):
    """Make HTTP request to API endpoint"""
    try:
        url = f"{api_url}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        return {
            "status": "success",
            "status_code": response.status_code,
            "data": response.json() if response.content else {}
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Could not connect to API. Make sure the FastAPI server is running."
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timed out."
        }
    except requests.exceptions.HTTPError as e:
        try:
            error_data = response.json()
            return {
                "status": "error",
                "status_code": response.status_code,
                "message": error_data.get("detail", str(e))
            }
        except:
            return {
                "status": "error",
                "status_code": response.status_code,
                "message": str(e)
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input")
    
    # Text field for apartment search query
    query = st.text_area(
        "Apartment Search Query",
        placeholder="Enter your apartment search query here...\nExample: I'm looking for a 2 bedroom apartment near the beach in Miami",
        height=100,
        help="Enter a description of what you're looking for in an apartment"
    )
    
    st.markdown("---")
    
    # Buttons
    st.subheader("🚀 Test Endpoints")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🔍 Find Apartment", type="primary", use_container_width=True):
            if not query.strip():
                st.warning("Please enter a search query first")
            else:
                with st.spinner("Searching for apartment..."):
                    result = make_request("/tool/find-apartment", data={"query": query})
                    st.session_state.responses.append({
                        "endpoint": "Find Apartment",
                        "request": {"query": query},
                        "response": result
                    })
                    if result["status"] == "success":
                        st.success("✅ Request successful!")
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    with col_btn2:
        if st.button("👤 Add User", use_container_width=True):
            with st.spinner("Adding user..."):
                result = make_request("/tool/add-user", data={"user_id": "test_user"})
                st.session_state.responses.append({
                    "endpoint": "Add User",
                    "request": {"user_id": "test_user"},
                    "response": result
                })
                if result["status"] == "success":
                    st.success("✅ Request successful!")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    col_btn3, col_btn4 = st.columns(2)
    
    with col_btn3:
        if st.button("📅 Add Appointment", use_container_width=True):
            with st.spinner("Adding appointment..."):
                result = make_request("/tool/add-appointment", data={"appointment_id": "test_appointment"})
                st.session_state.responses.append({
                    "endpoint": "Add Appointment",
                    "request": {"appointment_id": "test_appointment"},
                    "response": result
                })
                if result["status"] == "success":
                    st.success("✅ Request successful!")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    with col_btn4:
        if st.button("❤️ Health Check", use_container_width=True):
            with st.spinner("Checking health..."):
                result = make_request("/health", method="GET")
                st.session_state.responses.append({
                    "endpoint": "Health Check",
                    "request": None,
                    "response": result
                })
                if result["status"] == "success":
                    st.success("✅ API is healthy!")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")

with col2:
    st.header("📊 Responses")
    
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.responses = []
        st.rerun()
    
    if st.session_state.responses:
        # Show latest response first
        for i, response_data in enumerate(reversed(st.session_state.responses[-10:])):  # Show last 10
            with st.expander(f"{response_data['endpoint']} - {response_data['response'].get('status', 'unknown').upper()}", expanded=(i == 0)):
                st.markdown("**Request:**")
                if response_data['request']:
                    st.json(response_data['request'])
                else:
                    st.text("GET request (no body)")
                
                st.markdown("**Response:**")
                if response_data['response']['status'] == "success":
                    st.json(response_data['response'].get('data', {}))
                    if 'status_code' in response_data['response']:
                        st.caption(f"Status Code: {response_data['response']['status_code']}")
                else:
                    st.error(response_data['response'].get('message', 'Unknown error'))
                    if 'status_code' in response_data['response']:
                        st.caption(f"Status Code: {response_data['response']['status_code']}")
    else:
        st.info("👈 Make a request to see responses here")

# Footer
st.markdown("---")
st.caption("💡 Make sure your FastAPI server is running before testing endpoints")

