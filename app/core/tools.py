from langchain.tools import tool
from langchain_tavily import TavilySearch
from datetime import date
from app.config.settings import (
    TAVILY_API_KEY
)


tavily = TavilySearch(max_results=3)


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

