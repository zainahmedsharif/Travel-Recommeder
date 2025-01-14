
from datetime import datetime  # For working with dates and times
from amadeus import Client, ResponseError  # For interacting with the Amadeus API
from langchain.prompts import PromptTemplate  # For creating the LLM prompt
from langchain.tools import Tool  # For defining the flight_inspiration_tool
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os
load_dotenv()

amadeus = Client(
     client_id=os.getenv('AMADEUS_KEY'),
     client_secret=os.getenv('AMADEUS_SECRET')
 )
#print

llm = ChatOpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))


def fetch_flight_inspirations(origin, departure_date=None, max_price=None):
    """
    Fetches possible destinations with indicative prices using Amadeus Flight Inspiration Search API.
    """
    try:
        # Prepare parameters based on the API's requirements
        params = {"origin": origin}
        if departure_date:
            params["departureDate"] = departure_date  # Use camelCase
        if max_price:
            params["maxPrice"] = max_price  # Correct camelCase for maxPrice

        # Call the Amadeus API
        response = amadeus.shopping.flight_destinations.get(**params)

        # Check and parse the response
        if response.status_code == 200:
            destinations = response.data
            return [
                {
                    "destination": destination["destination"],
                    "price": destination["price"]["total"],
                    "departure_date": destination.get("departureDate", "N/A")
                }
                for destination in destinations
            ]
        else:
            print(f"Unexpected response: {response.status_code} - {response.body}")
            return {"error": f"Unexpected API response: {response.status_code}"}

    except ResponseError as error:
        print(f"Error fetching flight inspirations: {error}")
        return {"error": f"Amadeus API error: {error}"}

def extract_flight_inspiration_parameters(user_query):
    """
    Uses the LLM to extract parameters for the Flight Inspiration Search API from the user's query.
    """
    today_date = datetime.today().strftime("%Y-%m-%d")

    prompt = PromptTemplate(
        input_variables=["query", "today_date"],
        template="""
Extract flight search parameters for inspiration from the following user query.
Return the response as a strict JSON object with the keys: origin, departure_date, max_price.

- The 'origin' key must contain a valid IATA code (e.g., 'JFK').
- The 'departure_date' key must be in 'YYYY-MM-DD' format only. Resolve relative terms like 'next week' into an exact date.
- The 'max_price' key is optional. If not mentioned, return null.

DO NOT include any additional text or comments in the response.

User Query: {query}
Today's Date: {today_date}
"""
    )

    formatted_prompt = prompt.format(query=user_query, today_date=today_date)
    response = llm.predict(formatted_prompt)
    response = eval(response.replace('null', 'None'))  # Convert JSON-like string to Python dict
    
    return response

def llm_agent_query_inspirations(user_query):
    """
    Integrates the LLM for parameter extraction and fetches flight inspirations using Amadeus API.
    """
    # Step 1: Extract parameters from user query
    params = extract_flight_inspiration_parameters(user_query)
    
    # Validate extracted parameters
    required_keys = ['origin', 'departure_date']
    if not all(params.get(key) for key in required_keys):
        return {"error": "Missing required parameters in query. Please provide origin and departure date."}
    print(params)

    # Step 2: Fetch flight inspirations
    inspirations = fetch_flight_inspirations(
        origin=params['origin'],
        departure_date=params['departure_date'],
        max_price=params.get('max_price')
    )

    return inspirations

# Define the Flight Inspiration Tool
flight_inspiration_tool = Tool(
    name="Flight Inspiration Search",
    func=llm_agent_query_inspirations,
    description=(
        "Fetch possible travel destinations with indicative prices based on user queries. "
        "Provide origin, departure date, and optionally, a maximum price. "
        "Returns a list of destinations with prices and dates."
    )
)