import json
#from langchain_core.messages import HumanMessage, SystemMessage
from app.core.graph import *


# Build app

tools = [
    web_search_tool,
    search_football_events_tool,
    get_stadium_info_tool,
    search_train_schedule_tool,  
    search_hotels_tool,
    get_current_date_tool,
]


prompt = """
I am based in Hannover, Germany and want to plan a football-focused trip between
February 1-14, 2026.

Cities of interest:
- Munich
- Frankfurt
- Berlin

Please:
1. Find football matches I could attend in those cities
2. Identify the stadiums where the matches are played
3. Suggest train or bus travel options from Hannover to the stadiums, including departure and arrival times
4. Recommend affordable hotels near the stadiums
5. Provide stadium transport tips
6. Generate a simple travel itinerary

You MUST return the final answer as valid JSON.
Do not include explanations or markdown.
The JSON must follow this schema exactly:

{
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
      "from": "Hannover",
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

"""

app_sports_travel_agent = build_graph_one_tool(tools)
output, history = app_call(app_sports_travel_agent, prompt)
structured_output = json.loads(output)
print(structured_output)
