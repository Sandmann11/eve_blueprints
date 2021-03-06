import time
import base64
from datetime import datetime as dt
import requests
import pandas as pd
from inv_types import df2, locations_df
from app_info import client_id, app_secret, refresh_token, character_id


start = time.time()
print("\nStart!\n")


# Authorize with SSO refresh token and retrieve new access token from SSO response
def authorize():
    user_pass = "{}:{}".format(client_id, app_secret)
    basic_auth = base64.urlsafe_b64encode(user_pass.encode('utf-8')).decode()
    auth_header = "Basic {}".format(basic_auth)
    form_values = {"grant_type": "refresh_token",
                "refresh_token": refresh_token}
    headers = {"Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com",
            "Authorization": auth_header}
    res = requests.post("https://login.eveonline.com/v2/oauth/token",
                        data=form_values,
                        headers=headers)
    res.raise_for_status()
    data = res.json()
    access_token = data["access_token"]
    return access_token

access_token = authorize()


# Authorize with new access token and retrieve the blueprint list
def get_blueprints():
    blueprint_path = ("https://esi.evetech.net/latest/characters/{}/"
                    "blueprints/".format(character_id))
    bp_headers = {"Authorization": "Bearer {}".format(access_token)}
    bp_res = requests.get(blueprint_path, headers=bp_headers)
    bp_res.raise_for_status()
    blueprints = bp_res.json()
    return blueprints

blueprints = get_blueprints()


# Convert to pandas DataFrame, clean up
def blueprints_df():
    df = pd.DataFrame(blueprints)
    df = df.drop("item_id", axis='columns')
    df.rename(columns={"location_flag": "loc_flag",
                    "location_id": "loc_id",
                    "material_efficiency": "mat_eff",
                    "time_efficiency": "time_eff",
                    "typeID": "type_id"},
            inplace=True)
    return df

df = blueprints_df()
print(df)



bp_df = pd.merge(df, df2)

bp_df.rename(columns={"groupID": "group_id",
                      "categoryID": "category_id",
                      "groupName": "group_name",
                      "typeName": "type_name",
                      "marketGroupID": "market_group_id"},
             inplace=True)

bp_df = bp_df.drop(["group_id", "category_id", "type_id", "market_group_id"],
                   axis='columns')

bp_df = bp_df[["loc_flag", "loc_id", "type_name", "quantity", "mat_eff",
               "time_eff", "runs", "group_name"]]

bp_df["quantity"].replace({-1: "Original",
                           -2: "Copy"},
                          inplace=True)

bp_df["runs"].replace({-1: "inf"},
                      inplace=True)

bp_df["group_name"] = bp_df["group_name"].map(lambda x: x.rstrip("Blueprint"))
bp_df["group_name"] = bp_df["group_name"].map(lambda x: x.rstrip("Blueprints"))
bp_df["group_name"] = bp_df["group_name"].map(lambda x: x.rstrip("Formulas"))
bp_df["type_name"] = bp_df["type_name"].map(lambda x: x.rstrip("Blueprint"))
bp_df["type_name"] = bp_df["type_name"].map(lambda x: x.rstrip("Formula"))

# bp_df = bp_df.convert_dtypes()
print(f"\nPrinting bp_df:\n{bp_df}\n")
print(bp_df.info())


# loc_df = pd.read_csv('game_data/locations.csv')
# print(f"\nPrinting loc_df:\n{loc_df}\n")
# loc_df = loc_df.reset_index(drop=True)
# print(loc_df.info())

# blueprints_df = pd.merge(loc_df, bp_df, how='right')
# blueprints_df = blueprints_df.reset_index(drop=True)
# blueprints_df = blueprints_df.convert_dtypes()

# print(f"\nPrinting blueprints_df:\n{blueprints_df}\n")
# print(blueprints_df.info())

# Write the blueprint list into a new Excel sheet with current date & time as the sheet name
# now = dt.now()
# sheet_name = now.strftime("%Y.%m.%d - %H.%M.%S")

# with pd.ExcelWriter('blueprints.xlsx', mode='a') as writer:
#     blueprints_df.to_excel(writer, sheet_name=sheet_name)


end = time.time()
print("\nStop!\n")

counter = end - start
counter = round(counter, 2)

print(f"Operation complete\nTime elapsed: {counter} s\n")
