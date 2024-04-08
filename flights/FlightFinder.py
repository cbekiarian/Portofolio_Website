import requests
from datetime import datetime, timedelta
import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get('TEQUILA_KEY')

class SearchFlights:
    def __init__(self, origin, destination, max_price):
        self.origin_code = self.get_destination_code(origin)
        self.destination_code = self.get_destination_code(destination)
        self.flights_found = self.find_flights(self.origin_code, self.destination_code, max_price)

    def get_destination_code(self, city_name):
        # Get IATA code for that city name
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]

        try:
            code = results[0]["code"]
        except:

            return None
        return code

    def find_flights(self, origin_code, destination_code, max_price):

        #check flights  with the specified information
        flight = self.check_flights(
            origin_code,
            destination_code,
            max_price= max_price
        )
        if flight != None:
            return flight
        else:
            return None


    def check_flights(self, origin_city_code, destination_city_code, max_price):

        # Set the search limit from tomorrow to 6 months later
        tomorrow = datetime.now() + timedelta(days=1)
        six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_month_from_today.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 1,
            "nights_in_dst_to": 10,
            "flight_type": "round",
            "max_stopovers": 0,
            "price_to": max_price,
            "curr": "EUR",
            "one_for_city": 0
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )
        try:
            data = response.json()["data"]
        except:
            return None
        loops = 10
        flight_data = []
        if len(data)< loops :
            loops = len(data)
        for i in range(0,loops):

            flight_data.append(FlightData(
                price=data[i]["price"],
                origin_city=data[i]["route"][0]["cityFrom"],
                origin_airport=data[i]["route"][0]["flyFrom"],
                destination_city=data[i]["route"][0]["cityTo"],
                destination_airport=data[i]["route"][0]["flyTo"],
                departure_date=data[i]["route"][0]["local_departure"].split("T")[0],
                return_date=data[i]["route"][1]["local_departure"].split("T")[0]
                )
            )

        return flight_data
class FlightData:
    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, departure_date, return_date):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.departure_date = departure_date
        self.return_date = return_date


