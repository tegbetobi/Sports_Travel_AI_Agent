from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel
from typing import List
from app.core.graph import *
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from app.core.graph import *

app = FastAPI(title="Sports Travel Planner API")

tools = [
    web_search_tool,
    search_football_events_tool,
    get_stadium_info_tool,
    search_train_schedule_tool,
    search_hotels_tool,
    get_current_date_tool,
]

graph_app = build_graph_one_tool(tools)


class TripRequest(BaseModel):
    origin: str
    destinations: List[str]        # Example: ["Munich", "Berlin", "Frankfurt"]
    start_date: str                # Format: "YYYY-MM-DD"
    end_date: str                  # Format: "YYYY-MM-DD"


@app.post("/plan")
def plan_trip(request: TripRequest):
    dest_list = "\n- ".join(request.destinations)
    schema = {
        "matches": [
            {
                "city": "Munich",
                "date": "2026-02-07",
                "competition": "Bundesliga",
                "home_team": "Bayern Munich",
                "away_team": "Borussia Dortmund",
                "stadium": "Allianz Arena"
            }
        ],
        "transport": [
            {
                "from": request.origin,
                "to": "Munich",
                "mode": "train",
                "departure_time": "07:30",
                "arrival_time": "11:45",
                "duration": "4h 15m"
            }
        ],
        "hotels": [
            {
                "name": "Hotel XYZ",
                "city": "Munich",
                "distance_to_stadium": "1.2 km",
                "price_estimate": "€90/night"
            }
        ],
        "stadium_tips": [
            "Arrive 90 minutes early",
            "Use U-Bahn line U6 to Allianz Arena"
        ],
        "itinerary": [
            {
                "date": "2026-02-07",
                "plan": "Morning train → hotel check-in → match → dinner"
            }
        ]
    }


    system_prompt = f"""
I am based in {request.origin}, Germany and want to plan a football-focused trip between
{request.start_date} and {request.end_date}.

Cities of interest:
- {dest_list}

 Please:
            1. Find football matches I could attend in those cities
            2. Identify the stadiums where the matches are played
            3. Suggest train or bus travel options from {request.origin} to the stadiums, including departure and arrival times
            4. Recommend affordable hotels near the stadiums
            5. Provide stadium transport tips
            6. Generate a simple travel itinerary

You MUST return strictly valid JSON following this schema exactly:
{json.dumps(schema, indent=2)}
Do not include explanations or markdown.
Do not wrap JSON in code blocks.
"""

    output, _ = app_call(graph_app, system_prompt) # call langGraph app
    return json.loads(output)  # return parsed JSON
