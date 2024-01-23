import pandas as pds
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json
import numpy as np
import datetime

# Define and initialize program varriables

client = MongoClient("localhost", 27017)
database = client["db_Airbnb"]
csv_file_path = "Dateset_Listing.csv"
collection_name = "Collection_Property_Listings"

print("Loading AirBnb listing details into database \n ")


# function used to import csv file into database
def mongoimport(csv_file_path):
    data = pds.read_csv(csv_file_path, low_memory=False)
    data_to_upload = json.loads(data.to_json(orient='records'))
    database[collection_name].delete_many({})
    database[collection_name].insert_many(data_to_upload)
    return database[collection_name].count_documents({})


# Calling funtion to import file to database
# num = mongoimport(csv_file_path)

def _get_property_type_percent(cityName):
    # print("\nPlease enter City name to know more about property \n")
    #
    # cityName = input("Enter City = ")

    city_property_result = list(database[collection_name].aggregate([
        {"$match": {"Neighbourhood Group Cleansed": {'$ne': None}, "City": cityName}},
        {"$group": {"_id": {"PropertyType": "$Property Type"}, "PropertyCount": {'$sum': 1}}}
    ]))

    x = []
    y = []

    for docs in city_property_result:
        x.append(docs['_id']['PropertyType'])
        y.append(float(docs['PropertyCount']))

    plt.pie(y, labels=x, autopct='%1.1f%%')
    plt.axis('equal')
    plt.legend()
    plt.legend(frameon=True, loc='lower right')
    plt.title('% of property type for ' + cityName + ' city ')
    plt.show()


def _best_neighborhood(cityName, property_type):
    aggregation_result_neighbourhood = list(database[collection_name].aggregate([
        {"$match": {"Neighbourhood Group Cleansed": {'$ne': None}, "City": cityName, "Property Type": property_type}},
        {"$group": {"_id": {"Neighbourhood Group Cleansed": "$Neighbourhood Group Cleansed", "Room Type": "$Room Type"},
                    "Price": {"$avg": "$Price"}}},
        {"$sort": {"_id.Neighbourhood Group Cleansed": 1, "_id.Price": -1, "_id.Room Type": 1}},
    ]))

    # for docs in aggregation_result_neighbourhood:
    #     print(docs)

    neighbourhood_set = set()
    for result in aggregation_result_neighbourhood:
        neighbourhood = result["_id"]["Neighbourhood Group Cleansed"]
        neighbourhood_set.add(neighbourhood)
    neighbourhood_list = list(neighbourhood_set)
    # print(len(neighbourhood_set))
    private_room_list = [0 for i in range(len(neighbourhood_set))]
    entire_home_list = [0 for i in range(len(neighbourhood_set))]
    shared_room = [0 for i in range(len(neighbourhood_set))]
    neighbourhood_list_inorder = []
    current_neighbourhood = ''
    current_index = 0

    for result in aggregation_result_neighbourhood:
        # print(result)
        if current_neighbourhood == '':
            current_neighbourhood = result["_id"]["Neighbourhood Group Cleansed"]
            neighbourhood_list_inorder.append(result["_id"]["Neighbourhood Group Cleansed"])
        if current_neighbourhood != result["_id"]["Neighbourhood Group Cleansed"]:
            # print("not same")
            current_neighbourhood = result["_id"]["Neighbourhood Group Cleansed"]
            current_index += 1
            neighbourhood_list_inorder.append(result["_id"]["Neighbourhood Group Cleansed"])
        # print(current_neighbourhood)
        # print(current_index)
        # print(str(private_room_list))
        # print(str(entire_home_list))
        # print(str(shared_room))
        if result["_id"]["Room Type"] == "Private room":
            private_room_list[current_index] = float(result["Price"])
        elif result["_id"]["Room Type"] == "Entire home/apt":
            entire_home_list[current_index] = float(result["Price"])
        elif result["_id"]["Room Type"] == "Shared room":
            shared_room[current_index] = float(result["Price"])
    # print(neighbourhood_list_inorder)

    x = np.arange(len(neighbourhood_list))
    width = 0.2

    # plot data in grouped manner of bar type
    plt.bar(x - 0.2, private_room_list, width, color='cyan')
    plt.bar(x, entire_home_list, width, color='orange')
    plt.bar(x + 0.2, shared_room, width, color='green')
    # for neighbourhood_name in neighbourhood_list:
    plt.xticks(x, neighbourhood_list_inorder)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.xlabel("Neighbourhood")
    plt.ylabel("Average Price")
    plt.legend(["Private Room", "Entire home", "Shared room"])
    plt.title("Analysis of best neighbourhood based on average price and room type")
    plt.show()


def _get_popular_host(cityName, Neighbourhood):
    aggregation_result_hostlist = list(database[collection_name].aggregate([
        {"$match": {"Neighbourhood Group Cleansed": {'$ne': None}, "City": cityName,
                    "Neighbourhood Group Cleansed": Neighbourhood}},
        {"$match": {"Review Scores Rating": 100, "Cancellation Policy": "flexible",
                    "Host Response Time": "within an hour"}},
        {"$group": {"_id": {"Neighbourhood Group Cleansed": "$Neighbourhood Group Cleansed", "Host Name": "$Host Name",
                            "Name": "$Name"}}},
        {"$limit": 5}
    ]))
    if len(aggregation_result_hostlist) == 0:
        print("\nThere are no popular hosts that meets the criteria")
    else:
        print("The most popular are: ")
        for idx, r in enumerate(aggregation_result_hostlist):
            print(str(idx + 1) + "." + r["_id"]["Host Name"])


def _host_listing_info(cityName):
    Host_count = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$group": {"_id": "$Host ID", "count": {"$sum": 1}}}
    ]))
    Total_host = len(Host_count)
    if Total_host == 0:
        print("No host is available")
    print("Total number of hosts listed : " + str(len(Host_count)))
    Host_multiple_listing = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$group": {"_id": {"Host ID": "$Host ID"}, "count": {"$sum": "$Host Listings Count"}}},
        {"$match": {"count": {"$gte": 2}}},
    ]))
    host_with_multiple_listing = len(Host_multiple_listing)

    print("Number of hosts having multiple properties listed : " + str(len(Host_multiple_listing)))

    percent_host_with_multiple_listing = "{:.2f}".format((host_with_multiple_listing / Total_host) * 100)

    print("\n" + str(
        percent_host_with_multiple_listing) + " percent of hosts listed have multiple properties with Airbnb in " + cityName + " city")

    # startdate = datetime.date(2013,1,1).isoformat()
    # print(startdate)
    # endDate = datetime.date(2014,1,1).isoformat()
    # print(endDate)
    years = ["2012", "2013", "2014", "2015", "2016"]
    host_enrolled_peryear = []
    host_count_2012 = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$match": {"Host Since": {"$regex": "2012"}}}
    ]))
    host_enrolled_peryear.insert(0, len(host_count_2012))
    host_count_2013 = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$match": {"Host Since": {"$regex": "2013"}}}
    ]))
    # print(len(host_count_2013))
    host_enrolled_peryear.insert(1, len(host_count_2013))
    host_count_2014 = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$match": {"Host Since": {"$regex": "2014"}}}
    ]))
    # print(len(host_count_2014))
    host_enrolled_peryear.insert(2, len(host_count_2014))
    host_count_2015 = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$match": {"Host Since": {"$regex": "2015"}}}
    ]))
    # print(len(host_count_2015))
    host_enrolled_peryear.insert(3, len(host_count_2015))
    host_count_2016 = list(database[collection_name].aggregate([
        {"$match": {"Host ID": {'$ne': None}, "City": cityName}},
        {"$match": {"Host Since": {"$regex": "2016"}}}
    ]))
    # print(len(host_count_2016))
    host_enrolled_peryear.insert(4, len(host_count_2016))

    tick_label = ["2012", "2013", "2014", "2015", "2016"]

    # plt.bar(years, host_enrolled_peryear, tick_label=tick_label,
    #         width=0.8, color=['Pink'])
    plt.scatter(years, host_enrolled_peryear, c="blue")
    plt.xlabel('Years')
    plt.ylabel('Host listed')
    plt.title('Number of host listing by year')
    plt.show()


if __name__ == "__main__":
    num = mongoimport(csv_file_path)
    if num <= 0:
        print("No listing founds")

    print("Total property listings :" + str(num) + " available in the database now for you")

    while True:
        print("\nAnalysis Topics\n")
        print("1. Show all the different property types and the highest percent of property type for given city")
        print("2. Show the best neighbourhood based on average price and room type for given city and property type")
        print(
            "3. List 5 most popular hosts for given neighbourhood based on factors like amenities provided, host response time, host review ratings and cancellation policies")
        print(
            "4. Get the percent of hosts which have multiple properties listed in airbnb and the number of hosts joining Airbnb each year from 2012 to 2016")
        print("5. Exit ")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            print("Show all the different property types and the highest percent of property type for given city")
            city_list = ["Seattle", "New York"]

            print("\nPlease enter the city name from the cities listed below: \n")

            for idx, city in enumerate(city_list):
                print(str(idx + 1) + ". " + city + "\n")

            city_name = ''
            while True:
                city_name = input("Enter city name: ")
                if city_name in city_list:
                    break
                else:
                    print(
                        "You may have misspelled a city or may have entered a city not in the list. Please try again.")

            _get_property_type_percent(city_name)

        elif choice == 2:
            print("Show the best neighbourhood based on average price and room type for given city and property type")

            city_list = ["Seattle", "New York"]
            print("\nPlease enter the city name from the cities listed below: \n")
            for idx, city in enumerate(city_list):
                print(str(idx + 1) + ". " + city + "\n")

            city_name = ''
            while True:
                city_name = input("Enter city name: ")
                if city_name in city_list:
                    break
                else:
                    print(
                        "You may have misspelled a city or may have entered a city not in the list. Please try again.")

            print("Selected city is " + city_name + ". Now enter a property type from the property types listed below:")

            city_property_result = list(database[collection_name].aggregate([
                {"$match": {"Neighbourhood Group Cleansed": {'$ne': None}, "City": city_name}},
                {"$group": {"_id": {"PropertyType": "$Property Type"}, "PropertyCount": {'$sum': 1}}},
                {"$match": {"PropertyCount": {"$gte": 100}}},
            ]))

            if len(city_property_result) <= 0:
                print(
                    "There is not enough data for the different property types in your selected city " + city_name + ". Please choose another city or another analysis.")
                continue

            for idx, property in enumerate(city_property_result):
                print(str(idx + 1) + "." + property["_id"]["PropertyType"] + "\n")
            property_type = ''
            while True:
                property_type = input("Enter the property type: ")
                if property_type in city_property_result:
                    break
                else:
                    print(
                        "You may have misspelled a property type or may have entered a property type not in the list. Please try again.")

            _best_neighborhood(city_name, property_type)

        elif choice == 3:
            print(
                "List 5 most popular hosts for given neighbourhood based on factors like amenities provided, host response time, host review ratings and cancellation policies")

            city_list = ["Seattle", "New York"]
            print("\nPlease enter the city name from the cities listed below: \n")
            for idx, city in enumerate(city_list):
                print(str(idx + 1) + ". " + city + "\n")

            city_name = ""
            while True:
                city_name = input("Enter city name: ")
                if city_name in city_list:
                    break
                else:
                    print(
                        "You may have misspelled a city or may have entered a city not in the list. Please try again.")
            print("Selected city is " + city_name + ". Now enter a neighbourhood from the list below:")

            city_neighbourhood_result = list(database[collection_name].aggregate([
                {"$match": {"Neighbourhood Group Cleansed": {'$ne': None}, "City": city_name}},
                {"$group": {"_id": {"Neighbourhood Group Cleansed": "$Neighbourhood Group Cleansed"}}},
            ]))
            for idx, neighbourhood in enumerate(city_neighbourhood_result):
                print(str(idx + 1) + "." + neighbourhood["_id"]["Neighbourhood Group Cleansed"])

            selected_neighbourhood = ''
            while True:
                selected_neighbourhood = input("Enter neighbourhood name: ")
                if selected_neighbourhood in city_neighbourhood_result:
                    break
                else:
                    print(
                        "You may have misspelled a neighbourhood or may have entered a neighbourhood not in the list. Please try again.")

            _get_popular_host(city_name, selected_neighbourhood)

        elif choice == 4:
            print(
                "Get the percent of hosts which have multiple properties listed in airbnb and the number of hosts joining Airbnb each year from 2012 to 2016")

            city_list = ["Seattle", "New York"]
            print("\nPlease enter the city name from the cities listed below: \n")
            for idx, city in enumerate(city_list):
                print(str(idx + 1) + ". " + city + "\n")

            city_name = ""
            while True:
                city_name = input("Enter city name: ")
                if city_name in city_list:
                    break
                else:
                    print(
                        "You may have misspelled a city or may have entered a city not in the list. Please try again.")
            print("Selected city is " + city_name + ". Now enter a neighbourhood from the list below:")

            _host_listing_info(city_name)

        elif choice == 5:
            break
        else:
            print("Please enter a valid input from 1 to 5 in the list above")