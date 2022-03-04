import urllib
import requests
from validate_jwt import validate_eve_jwt


def print_auth_url(client_id, code_challenge=None):
    base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/"
    params = {
        "response_type": "code",
        "redirect_uri": "https://localhost/callback/",
        "client_id": client_id,
        "scope": "esi-characters.read_blueprints.v1",
        "state": "unique-state"
    }

    if code_challenge:
        params.update({
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        })

    string_params = urllib.parse.urlencode(params)
    full_auth_url = "{}?{}".format(base_auth_url, string_params)
    
    print(full_auth_url)


#Sends a request for an authorization token to EVE SSO
def send_token_request(form_values, add_headers={}):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com",
    }

    if add_headers:
        headers.update(add_headers)

    res = requests.post(
        "https://login.eveonline.com/v2/oauth/token",
        data=form_values,
        headers=headers,
    )

    print("Request sent to URL {} with headers {} and form values: "
          "{}\n".format(res.url, headers, form_values))
    res.raise_for_status()

    return res

#Handles the authorization code response from the EVE SSO
def handle_sso_token_response(sso_response):
    
    if sso_response.status_code == 200:
        data = sso_response.json()
        access_token = data["access_token"]

        print("\nVerifying access token JWT...")

        jwt = validate_eve_jwt(access_token)
        character_id = jwt["sub"].split(":")[2]
        blueprint_path = ("https://esi.evetech.net/latest/characters/{}/"
                          "blueprints/".format(character_id))

        print("\nSuccess! Here is the payload received from EVE SSO: {}"
              "\nYou can use the access_token to make an authenticated "
              "request to {}".format(data, blueprint_path))

        input("\nPress any key to have this program make the request for you:")

        headers = {
            "Authorization": "Bearer {}".format(access_token)
        }

        res = requests.get(blueprint_path, headers=headers)
        
        print("\nMade request to {} with headers: "
              "{}".format(blueprint_path, res.request.headers))
        
        res.raise_for_status()

        data = res.json()
        print(type(data))

    else:
        print("\nSomething went wrong! Make sure you completed all the prerequisites and "
              "try again.")
        print("\nSent request with url: {} \nbody: {} \nheaders: {}".format(
            sso_response.request.url,
            sso_response.request.body,
            sso_response.request.headers
        ))
        print("\nSSO response code is: {}".format(sso_response.status_code))
        print("\nSSO response JSON is: {}".format(sso_response.json()))
