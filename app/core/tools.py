from langchain.tools import tool
from langchain_tavily import TavilySearch
from datetime import date
from amadeus import Client
from app.config.settings import (
    TAVILY_API_KEY,
    AMADEUS_CLIENT_ID,
    AMADEUS_CLIENT_SECRET,
)


tavily = TavilySearch(max_results=3)

amadeus_client = Client(
    client_id=AMADEUS_CLIENT_ID,
    client_secret=AMADEUS_CLIENT_SECRET,
    hostname="test",
)


@tool
def web_search_tool(query: str):
    """Search the web for sports events, stadium info, or travel tips."""
    return tavily.run(query)



@tool
def search_football_events_tool(city: str, date_range: str):
    """
    Finds upcoming football (soccer) matches in a given city and date range.
    Useful for locating Bundesliga or international matches when planning sports travel.
    """
    query = f"football matches in {city} during {date_range}"
    return tavily.run(query)


@tool
def get_stadium_info_tool(stadium_or_city: str):
    """
    Provides stadium information, nearby transport options, and tips for match day travel.
    """
    query = f"{stadium_or_city} football stadium transport train metro nearby attractions"
    return tavily.run(query)


@tool
def search_train_schedule_tool(origin_city: str, destination_city: str, arrival_time: str):
    """
    Searches for train or bus options between two German cities.
    
    origin_city: where you start
    destination_city: where you want to go
    arrival_time: desired arrival time at the stadium (YYYY-MM-DD HH:MM)
    
    Returns: a list of suitable train/bus options.
    """
    query = (
        f"Train or bus schedule from {origin_city} to {destination_city} "
        f"so I arrive by {arrival_time}. Include departure time, duration, and arrival time."
    )
    return tavily.run(query)


@tool
def get_current_date_tool():
    """Returns the current date in 'YYYY-MM-DD' format. Useful for finding flights/hotels relative to today."""
    return date.today().isoformat()


@tool
def search_hotels_tool(city_code: str, check_in_date: str, check_out_date: str, adults: int = 1):
    """
    Searches for available hotel options in a specific city for given dates using Amadeus.
    Requires the IATA city code (e.g., 'PAR', 'BER') and dates in 'YYYY-MM-DD' format. Use get_current_date_tool first if dates are relative.
    """

    print(
        f"DEBUG: Calling Amadeus Hotel Search - City: {city_code}, Check-in: {check_in_date}, Check-out: {check_out_date}, Adults: {adults}"
    )
    # Call Amadeus API - Hotel Search (find hotels by city)
    hotel_list_response = amadeus_client.reference_data.locations.hotels.by_city.get(
        cityCode=city_code, radius=50, radiusUnit="KM"
    )

    if not hotel_list_response.data or len(hotel_list_response.data) == 0:
        return f"No hotels found listed in Amadeus for city code {city_code}."

    # Get hotel IDs from the response (limit to first 5 for offers search)
    hotel_ids = [hotel["hotelId"] for hotel in hotel_list_response.data[:5]]

    # Now search for offers for these specific hotels
    hotel_offer_response = amadeus_client.shopping.hotel_offers_search.get(
        hotelIds=",".join(hotel_ids),
        checkInDate=check_in_date,
        checkOutDate=check_out_date,
        adults=adults, # we need to pass the number of adults
        bestRateOnly=True,  # Try to get simpler results
    )

    # Process the response (simplified)
    if hotel_offer_response.data and len(hotel_offer_response.data) > 0:
        results = []
        for offer in hotel_offer_response.data[:5]:  # Limit to showing 3 offers
            hotel_name = offer.get("hotel", {}).get("name", "N/A")
            price = offer.get("offers", [{}])[0].get("price", {}).get("total", "N/A")
            currency = offer.get("offers", [{}])[0].get("price", {}).get("currency", "")
            results.append(f"Hotel: {hotel_name}, Price: {price} {currency} (approx)")
        return "Found hotel options:\n- " + "\n- ".join(results)
    else:
        return f"No available hotel offers found for the dates in {city_code} among the checked hotels."