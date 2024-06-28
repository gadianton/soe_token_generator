# Standard python libraries
import base64
import hashlib
import os
import random
import re
import string
from urllib.parse import unquote
import webbrowser

# Open source libraries
import requests


def main():

    url = get_url()
    client_id = get_client_id()
    write_access = get_write_access_scope()
    no_expiry = get_no_expiry_scope()
    access_team = get_access_team_scope()
    code_verifier = create_code_verifier()

    oauth_url = url + '/oauth'
    redirect_uri = oauth_url + '/login_success'

    scopes = []
    if write_access:
        scopes.append("write_access")
    if no_expiry:
        scopes.append("no_expiry")
    if access_team:
        scopes.append("access_team")
    scope = ",".join(scopes) if scopes else ""

    authorization_code = get_authorization_code(oauth_url, code_verifier, redirect_uri,
                                                client_id, scope)
    token = get_token(oauth_url, client_id, redirect_uri, authorization_code, code_verifier)
    print("Here is your API token (below). Please keep it safe and don't share it.")
    print(f"API token >>> {token}")
    return token


def get_url():

    url = input('Enter the URL for your Stack Overflow instance: ')
    if not url.startswith("https://"):
        url = "https://" + url
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Received response code {response.status_code} when trying to access URL")
        print("Please check the URL and try again")
        raise SystemExit
    else:
        return url


def get_client_id():

    try:
        client_id = int(input('Enter the client ID for your API key: '))
    except ValueError:
        print("The client ID needs to be an number (integer)")
        raise SystemExit

    return client_id


def get_write_access_scope():

    phrase = 'Do you want the API token to have write access? (y/n) '
    return get_bool_response(phrase)


def get_no_expiry_scope():

    phrase = 'Do you want an API token without an expiration date? (y/n) '
    return get_bool_response(phrase)


def get_access_team_scope():

    phrase = "Do you want the API token to have access to a private team? (y/n) "
    return get_bool_response(phrase)


def get_bool_response(phrase):

    for _ in range(3):  # Allow up to 3 attempts
        response = input(phrase)
        if response.lower() in ["n", "y"]:
            if response == 'y':
                return True
            if response == 'n':
                return False
        print("Please enter a 'y' or 'n'")
    raise ValueError("Invalid input received multiple times.")


def get_authorization_code(oauth_url, code_verifier, redirect_uri, client_id, scope):

    code_challenge_method = 'S256'
    code_challenge = create_code_challenge(code_verifier)
    state = create_random_string(10)

    print("A browser tag is going to open and ask you to authenticate Stack Oveflow Enterprise")
    print("After successfully authenticating, you'll arrive a webpage that says "
          "'Authorizing Application'. Copy the URL of that page to your clipboard and return to "
          "this window.")
    input("Press Enter when ready...")
    webbrowser_url = f"{oauth_url}?client_id={client_id}&scope={scope}&state={state}&" \
        f"code_challenge={code_challenge}&code_challenge_method={code_challenge_method}&" \
        f"redirect_uri={redirect_uri}"
    webbrowser.open_new_tab(webbrowser_url)

    response_url = input("Please paste the URL from the previous step: ")
    match = re.search(r'code=(.+?)&', response_url)
    if match:
        authorization_code = match.group(1)
    else:
        raise ValueError("Authorization code not found in URL.")

    if "%" in authorization_code:
        authorization_code = unquote(authorization_code)

    return authorization_code


def create_code_verifier():
    # Source of code: https://www.stefaanlippens.net/oauth-code-flow-pkce.html

    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

    return code_verifier


def create_code_challenge(code_verifier):
    # Source of code: https://www.stefaanlippens.net/oauth-code-flow-pkce.html

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')

    return code_challenge


def create_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))


def get_token(oauth_url, client_id, redirect_uri, authorization_code, code_verifier):

    # Exchange the authorization code for an access token
    token_url = oauth_url + '/access_token/json'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': authorization_code,
        'code_verifier': code_verifier
    }

    response = requests.post(token_url, data=params)
    response_json = response.json()
    try:
        token = response_json['access_token']
    except KeyError:
        print("Error: Unable to retrieve access token.")
        print(response_json)
        # Potential error messages:
        # {"error_message":"Authorization code has expired"}
        # {"error_message":"No authorization code found"}
        raise SystemExit

    return token


if __name__ == '__main__':

    main()
