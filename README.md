**Project Title: Airbnb Rental System Data Analysis**

**SUMMARY**

***Developed Data analysis and recommendation system of Airbnb Rental System using Python libraties Pandas, PyMongo, Matplotlib and MongoDB Database***

**I. PROBLEM**

  Airbnb Rental System Data Analysis - In this project I worked on an analysis of the Airbnb rental system of two cities; New York and Seattle. The following is the analysis that I performed on the data:
  
   1.Show the different property types available for a particular city and determine which property type has highest percent in that city
  
  2. Show the best neighborhood based on the average price and room type for a given city and property type
     
  3. List the 5 top popular hosts for a given neighborhood based on multiple factors for each year
     
  4. Get the percentage of number of hosts which have multiple properties listed in Airbnb and show number of hosts joined Airbnb each year
     
  5. Find the percentage change in the average price of Airbnb in a city each year
     
  I used a public dataset obtained from opendatasoft for the cities New York and Seattle.
  
**II. SOFTWARE DESIGN AND IMPLEMENTATION**

A. Software Design and NoSQL-Database and Tools Used
To implement this Project I used the MongoDB NoSQL database. The project started with the selection of a dataset. After obtaining the dataset from a public dataset, I imported the Airbnb dataset in a .csv file. Then, I created a database named db_Airbnb and a collection named Collection_property_listing with MongoDB. Using the pandas library, the csv dataset file was imported inside MongoDB in a newly created   db_Airbnb database. The MongoDB database is connected to Python using a tool called pymongo. Then, I cleansed the dataset, removing any duplicate records present. For each analysis, the data required is fetched from the MongoDB database by writing a MongoDB query using functions like aggregate pipeline, sort, match, avg, regex etc. Once data is fetched in Python, it is displayed in the form of tables and different types of graphs using python libraries.
Tools used –
  1. Python 3.0
  2. Pymongo tool
  3. Different Python libraries such as pandas, matplotlib, sklearn.linear_model, numpy, json
B. Parts that you have implemented
I created a menu-driven Python code which takes the user’s input on which analysis they would like to view. For each analysis, the data required is fetched from the MongoDB database by writing a MongoDB query using functions like aggregate pipeline, sort, match, avg, regex etc. Once the data is fetched in Python, it is displayed in the form of tables and different types of graphs using python libraries.

**III. PROJECT OUTCOME**

1. Show the different property types available for a particular city and determine which property type has the highest percent in that city – In this analysis, the city is first grabbed from the user. After which, the data of each property type for a particular city is fetched from MongoDB. This data is then used to display a pie chart showing the percentage count of each property type for a particular city. From this analysis, the user can get a clear idea about what property types are available in a particular city and which property type has the highest percentage. Based on that data, a user can easily see which property type listing will appear most frequently in that city.

    ![image](https://github.com/kkhade1/MongoDB/assets/107223444/0aa3eb3f-6f99-491d-a205-677c31fd2b75)

2. Show the best neighborhood based on the average price and room type for a given city and property type - In this analysis, the city is first grabbed from the user. A query is run to retrieve all the different property types in the selected city. After the neighborhood is selected, another query is run to retrieve the data. I then sorted the data according to the
average price and different room type. This data is then used to display a graph showing the average price in each neighborhood of a particular city based on 3 different room types: private room, entire room or shared room. Based on this data, a user can easily get an idea about the average price of a particular room type as per the user’s requirement in each neighborhood in the city. The user can then make an informed choice on which neighborhood or property type best meets their requirements.

    ![image](https://github.com/kkhade1/MongoDB/assets/107223444/0855243b-06f8-425b-a682-ff61aca94c89)

3. List the 5 top popular hosts for a given neighborhood based on multiple factors – Similar to the above analysis, the city and neighborhood is retrieved from the user. A query is run to retrieve the most popular hosts based on key criteria such as amenities provided, host response time, host review ratings, and cancellation policies for each year. I verified few important factors such as:
  1. Amenities provided by the host like TV, internet, washer, dryer
  2. Host response time should be minimum. In this case, that will be within an hour
  3. Host review ratings must be greater than 90
  4. Cancellation policy must be flexible
This data was then sorted and only the top 5 hosts (in each year) were finalized. The name of property, property type, room type and average price of popular host is displayed in a table. Based on this analysis, users will get to know the list of best hosts in a particular neighborhood and city.

     ![image](https://github.com/kkhade1/MongoDB/assets/107223444/3ff16184-5a23-4e94-a03b-a84b5a0a905a)

     ![image](https://github.com/kkhade1/MongoDB/assets/107223444/c8dc5a21-b6a7-4406-8a75-ef3e27880f55)

4. Get the percentage of hosts which have multiple properties listed in Airbnb and show the number of hosts joining Airbnb each year – In this analysis, the city is first grabbed from the user. A query is run to retrieve the required data for all the hosts in the selected city who have more than 1 property listed in Airbnb. The percentage of hosts is calculated and displayed on the user display. Then another query is run to retrieve data on the hosts each year. This data is then displayed in a graph showing the number of hosts joining each year.This analysis will give users an idea about Airbnb’s popularity. An increasing number of hosts joining Airbnb would mean an increase in the number of people using Airbnb. A high percentage of hosts listing multiple properties also means that hosts are happy doing business with Airbnb and are happy with the rules and policies. This would also directly relate to increasing profit for Airbnb and its hosts.

     ![image](https://github.com/kkhade1/MongoDB/assets/107223444/c4fe14bd-5c7a-444e-a498-41288c158399)

     ![image](https://github.com/kkhade1/MongoDB/assets/107223444/6830bbbd-973e-4380-b39b-b461251a8b57)

5. Find the percentage change in the average price of Airbnb in a city each year – In this analysis, the city is first grabbed from the user. A query is run to retrieve the required data for avarage rental pricing in the city across all the years. The percent change in the pricing each year is displayed on a scatter plot. Using prediction analysis, the linear regression line is drawn on the scatter plot data. This data is very useful as percentage change in the average rental price of Airbnb in a particular city for each year and the linear regression line will help us to predict whether the rental price will increase or decrease. This prediction analysis is useful for everyone involved: Airbnb, hosts and customers. Analyzing the scatter plot and the down-sloping linear regression line, the rental prices seem to indicate a percentage decrease in price.

     ![image](https://github.com/kkhade1/MongoDB/assets/107223444/1585a7ce-bb4b-4aa5-9734-00706dc2ed09)


