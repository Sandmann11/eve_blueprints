import time
import pandas as pd


# Operation time measurement start
start = time.time()
print(f"\nStart!\n")


# Scraping the lists of structures and their IDs and names
url = "https://www.adam4eve.eu/info_stations.php"
dfs = pd.read_html(url)


# There are several tables on the page, so this has to be run just once 
# to find out the index of the table we want.

# for idx, table in enumerate(dfs):
#     print("**************************************************")
#     print(idx)
#     print(table)


str_df = dfs[5]
str_df = str_df.convert_dtypes()

# col_names = ["str_id", "str_name"]

str_df.to_csv('game_data/structures.csv', header=["str_id", "str_name"], index=False)

print(str_df.head())
print(str_df.info())

# Operation time measurement stop
end = time.time()
print(f"\nStop!\n")

counter = end - start
counter = round(counter, 2)

print(f"Operation complete.\nTime elapsed: {counter} s\n\n")