import requests
from flight_search import FlightSearch
from sheet import data
from data_manager import DataManager
from pprint import pprint
from flight_data import FlightData
import smtplib
from user import add_user,get_user

data_manager = DataManager()
sheet_data = data
# sheet_data = data_manager.get_destination()
fl = FlightSearch()
flight_data = FlightData()
for index in sheet_data:
    ext = ""
    index["iataCode"] = fl.return_IATA(index["city"])
    res = flight_data.get_flights(index["iataCode"])
    user = get_user()
    if res == None:
        continue
    if index["lowestPrice"] > res["price"]:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            if len(res["route"])>2:
                ext = f"Flight has {len(res["route"])} stop overs,"
                for index in res["route"]:
                    if index["cityTo"] == "Kraków":
                        ext += f"via Krakow,"
                    else:
                        ext += f"via {index["cityTo"]},"
                    print(ext)
            for item in user:

                connection.login(user="xristakos167@gmail.com", password="sqpl gruy raxn hyyh")
                connection.sendmail(from_addr="xristakos167@gmail.com",
                                    to_addrs=item["email"],
                                    msg=f"Subject: New Flight Found \n\n Headline: Low price alert!Only{res["price"]}to "
                                        f"fly from {res["cityFrom"]}-{res["cityCodeFrom"]} to "
                                        f"{res["cityTo"]}-{res["cityCodeTo"]} from"
                                        f" {res["local_departure"].split("T"[0])} to {res["local_arrival"].split("T")[0]}\n"
                                        f"{ext}")
# add_user()
pprint(sheet_data)
# data_manager.sheet_data = sheet_data
# data_manager.update()
