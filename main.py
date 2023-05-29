from send_prompt import replace_handlebars, get_llm_response
from get_flights import make_duffel_request
import datetime

FLIGHT_TESTING_MODE = False


def get_todays_date() -> str:
    today = datetime.date.today()
    iso_date = today.isoformat()
    return iso_date


def query_llm(request, current_location):
    prompt = replace_handlebars("prompts/flight_booking_request.txt",
                                request=request,
                                current_location=current_location,
                                current_date=get_todays_date())

    if not FLIGHT_TESTING_MODE:
        return get_llm_response(prompt)
    else:
        # This is the LLM output that we use for testing mode
        return {
            "origin": ["EWR", "JFK", "LGA"],
            "destination": ["SFO", "SJC", "OAK"],
            "departure_date": "2023-05-30",
            "return_date": "2023-06-04",
            "preferred_departure_time": None,
            "preferred_return_time": None,
            "class_of_service": ["BUSINESS"],
            "preferred_carriers": ["UA", "DL"]
        }


if __name__ == '__main__':
    response = query_llm(
        "Get me to paris on the first flight tomorrow, business class on United",
        "New York, NY")

    origin = response["origin"]
    destination = response["destination"]
    departure_date = response["departure_date"]
    return_date = response["return_date"]
    preferred_departure_time = response["preferred_departure_time"]
    preferred_return_time = response["preferred_return_time"]
    class_of_service = response["class_of_service"][0]
    preferred_carriers = response["preferred_carriers"]

    print(origin)
    print(destination)
    print(departure_date)
    print(return_date)
    print(preferred_departure_time)
    print(preferred_return_time)
    print(class_of_service)
    print(preferred_carriers)

    itinerary_offers = make_duffel_request(
        origin,
        destination,
        departure_date,
        preferred_departure_time,
        return_date,
        preferred_return_time,
        class_of_service,
        preferred_carriers
    )

    for offer in itinerary_offers:
        print(offer)
        print()
