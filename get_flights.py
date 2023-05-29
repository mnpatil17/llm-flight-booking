import json
from typing import List, Dict, Optional
from pathlib import Path
import requests

from flight import ItineraryOffer, FlightLeg, FlightSegment

DUFFEL_CREATE_OFFER_REQUEST_URL = "https://api.duffel.com/air/offer_requests"

#
# Times of day
#

MORNING = {
    "from": "06:00",
    "to": "11:59"
}

AFTERNOON = {
    "from": "12:00",
    "to": "17:59"
}

EVENING = {
    "from": "18:00",
    "to": "23:59"
}

NIGHT = {
    "from": "00:00",
    "to": "05:59"
}


def extract_offers_from_json(offers: Dict) -> List[ItineraryOffer]:
    itinerary_offers = []
    for offer in offers:
        # Get the financial information
        tax_amount = float(offer["tax_amount"])
        total_amount = float(offer["total_amount"])
        currency = offer["total_currency"]
        flight_legs = []
        for flight_slice in offer["slices"]:
            segment_objects = []
            for segment in flight_slice["segments"]:
                carrier = segment["operating_carrier"]["iata_code"]
                flight_number = segment["operating_carrier_flight_number"]
                origin_code = segment["origin"]["iata_code"]
                destination_code = segment["destination"]["iata_code"]
                departing_at = segment["departing_at"]
                arriving_at = segment["arriving_at"]
                duration = segment["duration"]
                aircraft = segment["aircraft"]
                segment_objects.append(FlightSegment(carrier, origin_code, destination_code, flight_number,
                                                     departing_at, arriving_at, duration, aircraft))

            flight_legs.append(FlightLeg(segment_objects))
        offer = ItineraryOffer(total_amount, tax_amount, currency, flight_legs)
        itinerary_offers.append(offer)

    return itinerary_offers


def make_duffel_request(
        origin_airports: List[str],
        destination_airports: List[str],
        departure_date: str,
        departure_time_range: Optional[str],
        return_date: Optional[str],
        return_time_range: Optional[str],
        class_of_service: str,
        preferred_carriers: List[str]
):
    # Construct the slices for the query
    slices = [
        create_slice(
            origin_airports[0],
            destination_airports[0],
            departure_date,
            get_time_preference_dict(departure_time_range))
    ]
    if return_date is not None:
        slices.append(
            create_slice(
                destination_airports[0],
                origin_airports[0],
                return_date,
                get_time_preference_dict(return_time_range))
        )

    headers = {
        "Duffel-Version": "v1",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {get_duffel_api_key()}"
    }

    payload = {
        "data": {
            "cabin_class": class_of_service.lower(),
            "passengers": [{
                "type": "adult"
            }],
            "slices": slices,
            "max_connections": 1,
        }
    }

    try:
        response = requests.post(
            DUFFEL_CREATE_OFFER_REQUEST_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        offers = dict(response.json())["data"]["offers"]
        return extract_offers_from_json(offers)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def create_slice(start: str, end: str, flight_date: str, flight_time_range: Dict[str, str]) -> Dict:
    return {
        "origin": start,
        "destination": end,
        "departure_date": flight_date,
        "departure_time": flight_time_range,
        "arrival_time": None
    }


def get_time_preference_dict(time_string: str) -> Dict:
    if time_string == "MORNING":
        return MORNING
    elif time_string == "AFTERNOON":
        return AFTERNOON
    elif time_string == "EVENING":
        return EVENING
    elif time_string == "NIGHT":
        return NIGHT
    else:
        return {
            "from": "00:00",
            "to": "23:59"
        }


def get_duffel_api_key() -> str:
    # Define the path to the API key file
    api_key_file = Path.home() / ".tokens" / "duffel.token"

    # Read the API key from the file
    with api_key_file.open() as f:
        api_key = f.read().strip()

    return api_key
