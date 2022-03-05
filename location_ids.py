import time
import pandas as pd


# Operation time measurement start
start = time.time()
print(f"\nStart!\n")


# Scraping the lists of stations (NPC owned) and structures (player owned) 
# and their IDs and names
url = "https://www.adam4eve.eu/info_stations.php"
dfs = pd.read_html(url)


# There are several tables on the page, so this has to be run just once to find out 
# the index of the table we want.
# for idx, table in enumerate(dfs):
#     print("**************************************************")
#     print(idx)
#     print(table)


# Stations
stations_df = dfs[4]
stations_df = stations_df.convert_dtypes()

stations_df.to_csv('game_data/stations.csv',
              header=["loc_id", "loc_name"], index=False)


#Structures
str_df = dfs[5]
str_df = str_df.convert_dtypes()

str_df.to_csv('game_data/structures.csv',
              header=["loc_id", "loc_name"], index=False)


# Operation time measurement stop
end = time.time()
print(f"\nStop!\n")

counter = end - start
counter = round(counter, 2)

print(f"Operation complete.\nTime elapsed: {counter} s\n\n")