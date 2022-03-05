import pandas as pd


def inv_types():
    df = pd.read_excel('game_data/invTypes.xlsx')
    df = df.drop(["description", "volume", "mass", "capacity",
                  "portionSize", "raceID", "basePrice",
                  "iconID", "soundID", "graphicID"],
                 axis='columns')

    filt = df["published"] == 0
    df = df.drop(index=df[filt].index)
    df = df.drop(["published"], axis='columns')
    df = df.fillna(-1)
    df.rename(columns={"typeID": "type_id"}, inplace=True)
    df = df.reset_index(drop=True)
    df = df.convert_dtypes()
    return df


inv_types_df = inv_types()
# print(f"\nPrinting inv_types_df:\n{inv_types_df}")


def group_ids():
    df = pd.read_csv('game_data/invGroups.csv')
    df = df.drop(["iconID", "useBasePrice", "anchored",
                  "anchorable", "fittableNonSingleton"],
                 axis='columns')

    filt = df["published"] == 0
    df = df.drop(index=df[filt].index)
    df = df.drop(["published"], axis='columns')
    df = df.reset_index(drop=True)
    df = df.convert_dtypes()
    return df


group_ids_df = group_ids()
# print(f"\nPrinting group_ids_df:\n{group_ids_df}")

df2 = pd.merge(group_ids_df, inv_types_df)
# print(f"\nPrinting df2:\n{df2}")


def station_ids():
    df = pd.read_csv('game_data/stations.csv')
    df = df.reset_index(drop=True)
    # df = df.convert_dtypes()
    return df

stations_df = station_ids()
# print(f"\nPrinting stations_df:\n{stations_df}")


def structure_ids():
    df = pd.read_csv('game_data/structures.csv')
    df = df.reset_index(drop=True)
    # df = df.convert_dtypes()
    return df


structures_df = structure_ids()
# print(f"\nPrinting structures_df:\n{structures_df}")

# USE CONCAT!!!
locations_df = stations_df.append(structures_df)
locations_df = locations_df.astype({'loc_id': 'int64', 
                                    'loc_name': 'string'})
# locations_df = locations_df.reset_index(drop=True)

locations_df.to_csv('game_data/locations.csv', index=False)

print(f"\nPrinting locations_df:\n{locations_df}\n")
print(locations_df.info())


# def inv_names():
#     df = pd.read_csv('game_data/invNames.csv')
#     df.rename(columns={"itemID": "loc_id",
#                        "itemName": "loc_name"},
#               inplace=True)

#     df = df.convert_dtypes()
#     return df


# inv_names_df = inv_names()

# print(f"\nPrinting inv_names_df:\n{inv_names_df}")


# def market_group_ids():
#     df = pd.read_csv('invMarketGroups.csv')
#     df = df.drop(["parentGroupID", "description", "iconID", "hasTypes"],
#                  axis='columns')
#     df.rename(columns={"marketGroupID": "market_group_id",
#                        "marketGroupName": "market_group"},
#               inplace=True)
#     df = df.reset_index(drop=True)
#     df = df.convert_dtypes()
#     return df

# market_groups_df = market_group_ids()
# print(f"\nPrinting market_groups_df:\n{market_groups_df}")
