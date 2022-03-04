import base64
from shared_flow import print_auth_url
from shared_flow import send_token_request
from shared_flow import handle_sso_token_response
from app_info import client_id, app_secret


def main():

    print_auth_url(client_id)

    auth_code = input("Copy the \"code\" query parameter and enter it here: ")
    
    user_pass = "{}:{}".format(client_id, app_secret)
    basic_auth = base64.urlsafe_b64encode(user_pass.encode('utf-8')).decode()
    auth_header = "Basic {}".format(basic_auth)

    form_values = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }

    headers = {"Authorization": auth_header}

    res = send_token_request(form_values, add_headers=headers)

    handle_sso_token_response(res)


if __name__ == "__main__":
    main()
