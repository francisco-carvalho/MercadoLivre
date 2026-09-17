import os
import base64
import hashlib
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from dotenv import load_dotenv, set_key


load_dotenv()


def save_refresh_token(refresh_token):
    set_key(".env", "MELI_REFRESH_TOKEN", refresh_token)

def refresh_access_token():
    refresh_token = os.getenv("MELI_REFRESH_TOKEN")

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("MELI_CLIENT_ID"),
        "client_secret": os.getenv("MELI_CLIENT_SECRET"),
        "refresh_token": refresh_token,
    }

    response = requests.post(
        "https://api.mercadolibre.com/oauth/token",
        data=payload,
        timeout=30,
    )

    response.raise_for_status()

    tokens = response.json()

    if tokens.get("refresh_token"):
        save_refresh_token(tokens["refresh_token"])

    return tokens

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(
        os.urandom(64)
    ).decode().rstrip("=")

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")

    return code_verifier, code_challenge


def get_access_token():
    refresh_token = os.getenv("MELI_REFRESH_TOKEN")

    if refresh_token:
        return refresh_access_token()

    verifier, challenge = generate_pkce()

    params = {
        "response_type": "code",
        "client_id": os.getenv("MELI_CLIENT_ID"),
        "redirect_uri": os.getenv("MELI_REDIRECT_URI"),
        "scope": "offline_access read",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    authorization_url = (
        "https://auth.mercadolivre.com.br/authorization?"
        + urlencode(params)
    )

    callback_url = input("\nPaste the callback URL here: ").strip()

    parsed_url = urlparse(callback_url)
    query_params = parse_qs(parsed_url.query)

    authorization_code = query_params.get("code", [None])[0]

    if not authorization_code:
        raise ValueError("Authorization code was not found in the callback URL.")

    token_url = "https://api.mercadolibre.com/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("MELI_CLIENT_ID"),
        "client_secret": os.getenv("MELI_CLIENT_SECRET"),
        "code": authorization_code,
        "redirect_uri": os.getenv("MELI_REDIRECT_URI"),
        "code_verifier": verifier,
    }

    response = requests.post(
        token_url,
        data=payload,
        timeout=30,
    )

    response.raise_for_status()

    tokens = response.json()

    if tokens.get("refresh_token"):
        save_refresh_token(tokens["refresh_token"])

    return tokens


if __name__ == "__main__":
    tokens = get_access_token()

    print("\nAuthorization successful!")
    print(f"Access token received: {bool(tokens.get('access_token'))}")
    print(f"Refresh token received: {bool(tokens.get('refresh_token'))}")