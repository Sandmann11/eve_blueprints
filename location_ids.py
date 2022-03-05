import time
import pandas as pd

# Operation time measurement start
start = time.time()
print("\nStart!\n")


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
# print(structures_df)

structures_df = str_df.drop(str_df.index[0])

structures_df.to_csv('game_data/structures.csv')

# Operation time measurement stop
end = time.time()
print("Stop!\n")

counter = end - start
counter = round(counter, 2)
print(f"Operation complete\n\nTime elapsed: {counter} s\n\n")