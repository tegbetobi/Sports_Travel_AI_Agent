import streamlit as st
import requests
import json

from app.config.settings import *
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)


st.set_page_config(
    page_title="Sports Travel Planner",
    layout="centered"
)

st.title("⚽ Sports Travel Planner")
st.write("Plan football trips with matches, transport, hotels, and itineraries.")

# Backend config
API_URL = "http://127.0.0.1:8000/plan"

GERMAN_CITIES = ["Berlin","Hamburg","Munich","Cologne","Frankfurt","Stuttgart","Düsseldorf","Dortmund","Essen","Leipzig","Bremen","Dresden",
"Hanover","Nuremberg","Duisburg","Bochum","Wuppertal","Bielefeld","Bonn","Münster","Karlsruhe","Mannheim","Augsburg","Wiesbaden","Gelsenkirchen","Mönchengladbach",
"Braunschweig","Chemnitz","Kiel","Aachen",
]

#user input
with st.form("trip_form"):
    origin = st.text_input("Your current city", placeholder="Hannover")

    selected_cities = st.multiselect("Select destination cities (Germany)",options=GERMAN_CITIES,)
    custom_cities = st.text_input("Other destination cities (comma-separated)",placeholder="e.g. Paris, Barcelona, Milan")

    extra_cities = [
    city.strip()
    for city in custom_cities.split(",")
    if city.strip()]

    destinations = list(set(selected_cities + extra_cities))

    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    submit = st.form_submit_button("Plan My Trip")


# submit request
if submit:
    if not origin or not destinations:
        st.error("Please provide an origin and at least one destination.")
    elif start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        payload = {
            "origin": origin,
            "destinations": destinations,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        try:
            logger.info("Sending trip planning request")
            response = requests.post(API_URL, json=payload, timeout=120)

            if response.status_code == 200:
                data = response.json()
                logger.info("Received response from backend")
                st.success("Trip plan generated!")

                st.subheader("Matches")
                for m in data.get("matches", []):
                    st.markdown(
                        f"**{m['home_team']} vs {m['away_team']}**  \n"
                        f"{m['competition']} — {m['date']}  \n"
                        f"{m['stadium']} ({m['city']})"
                    )

                st.subheader("Transport")
                for t in data.get("transport", []):
                    st.markdown(
                        f"**{t['from']} → {t['to']}**  \n"
                        f"{t['departure_time']} → {t['arrival_time']} ({t['duration']})"
                    )

                st.subheader("Hotels")
                for h in data.get("hotels", []):
                    st.markdown(
                        f"**{h['name']}** ({h['city']})  \n"
                        f"{h['distance_to_stadium']} — {h['price_estimate']}"
                    )

                st.subheader("Stadium Tips")
                for tip in data.get("stadium_tips", []):
                    st.markdown(f"- {tip}")

                st.subheader("Itinerary")
                for i in data.get("itinerary", []):
                    st.markdown(f"**{i['date']}** — {i['plan']}")

                with st.expander("Raw JSON"):
                    st.json(data)

            else:
                logger.error(f"Backend error: {response.text}")
                st.error("Backend returned an error.")

        except Exception as e:
            logger.exception("Failed to call backend")
            st.error(str(CustomException("Failed to communicate with backend")))
