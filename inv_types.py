import pandas as pd


def inv_types():
    df = pd.read_excel('invTypes.xlsx')
    
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

print(f"\nPrinting inv_types:\n{inv_types()}")


def group_ids():
    df = pd.read_csv('invGroups.csv')
    
    df = df.drop(["iconID", "useBasePrice", "anchored", 
                  "anchorable", "fittableNonSingleton"],
                 axis='columns')
    
    filt = df["published"] == 0
    df = df.drop(index=df[filt].index)
    df = df.drop(["published"], axis='columns')
    df = df.reset_index(drop=True)
    df = df.convert_dtypes()

    return df

print(f"\nPrinting group_ids:\n{group_ids()}")


df2 = pd.merge(group_ids(), inv_types())
print(f"\nPrinting df2:\n{df2}")


def inv_names():
    df = pd.read_csv('invNames.csv')
    df.rename(columns={"itemID": "loc_id",
                       "itemName": "loc_name"},
              inplace=True)

    return df
    
    
loc_df = inv_names()
print(f"\nPrinting loc_df:\n{loc_df}")
