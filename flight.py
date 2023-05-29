from typing import List
import datetime


class FlightSegment:
    """
    One take-off and landing.
    """

    def __init__(
            self,
            carrier_code: str,
            origin_airport: str,
            destination_airport: str,
            flight_number: str,
            departing_at: str,
            arriving_at: str,
            duration: float,
            aircraft: str):
        self.carrier_code = carrier_code
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.flight_number = flight_number
        self.departing_at = departing_at
        self.arriving_at = arriving_at
        self.duration = duration
        self.aircraft = aircraft

    def __str__(self):
        human_readable_departure = convert_iso_to_human(self.departing_at)
        human_readable_arrival = convert_iso_to_human(self.arriving_at)
        flight_no = "" if self.flight_number is None else self.flight_number

        return \
                f"{self.carrier_code} {flight_no:5s} | {self.origin_airport} to " + \
                f"{self.destination_airport} | {human_readable_departure} to {human_readable_arrival}"


class FlightLeg:
    """
    One direction of travel, potentially with connections
    """

    def __init__(self, segments: List[FlightSegment]):
        self.segments = segments
        self.origin = segments[0].origin_airport
        self.destination = segments[-1].destination_airport

    def __str__(self):
        return f"{self.origin} to {self.destination}\n" + \
            "\n".join(["\t Flight " + f"{i + 1}: " + str(segment) for i, segment in enumerate(self.segments)])


class ItineraryOffer:

    def __init__(self, total_amount: float, tax_amount: float, currency: str, legs: List[FlightLeg]):
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.currency = currency
        self.legs = legs

    def __str__(self):
        return f"Itinerary | Total Cost: {self.total_amount} {self.currency}\n" + "\n".join(
            [str(leg) for leg in self.legs])


def convert_iso_to_human(iso_datetime: str) -> str:
    datetime_obj = datetime.datetime.fromisoformat(iso_datetime)
    human_datetime = datetime_obj.strftime("%B %d, %Y at %H:%M")
    return human_datetime
