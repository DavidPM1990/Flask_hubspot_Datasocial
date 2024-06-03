import requests
from models import Contact
from database import db
import time
import json
import os
TOKENS_FILE = 'tokens.json'

TOKENS = {
    'access_token': None,
    'refresh_token': None,
    'expires_in': 0,
    'last_refreshed': 0
}

CLIENT_ID = 'a103975e-0126-43ca-a5c7-c0ae3c3a62c2'
CLIENT_SECRET = 'e7d3f137-a889-43fd-b3f2-3b0fb31969a0'
TOKEN_URL = 'https://api.hubapi.com/oauth/v1/token'

def load_tokens():
    if os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, 'r') as file:
                tokens = json.load(file)
                TOKENS.update(tokens)
        except json.JSONDecodeError:
            print("Error decoding JSON from tokens file. Initializing with empty tokens.")
            save_tokens(TOKENS)

def save_tokens(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file)

def upsert_hubspot_contact(email, name, access_token):
    url = f"https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{email}/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "properties": [
            {"property": "email", "value": email},
            {"property": "firstname", "value": name},
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def refresh_hubspot_token():
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': TOKENS.get('refresh_token')
    }
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code != 200:
        print("Error refreshing token:", response.json())
        return None
    
    tokens = response.json()
    TOKENS['access_token'] = tokens['access_token']
    TOKENS['refresh_token'] = tokens['refresh_token']
    TOKENS['expires_in'] = tokens['expires_in']
    TOKENS['last_refreshed'] = time.time()
    save_tokens(tokens)
    print("Tokens refreshed:", tokens)
    return tokens['access_token']


def get_hubspot_token():
    current_time = time.time()
    if (current_time - TOKENS['last_refreshed']) >= TOKENS['expires_in']:
        return refresh_hubspot_token()
    return TOKENS['access_token']

load_tokens()


TOKENS_FILE = 'tokens.json'

TOKENS = {
    'access_token': None,
    'refresh_token': None,
    'expires_in': 0,
    'last_refreshed': 0
}

CLIENT_ID = 'a103975e-0126-43ca-a5c7-c0ae3c3a62c2'
CLIENT_SECRET = 'e7d3f137-a889-43fd-b3f2-3b0fb31969a0'
TOKEN_URL = 'https://api.hubapi.com/oauth/v1/token'

def load_tokens():
    if os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, 'r') as file:
                tokens = json.load(file)
                TOKENS.update(tokens)
        except json.JSONDecodeError:
            print("Error decoding JSON from tokens file. Initializing with empty tokens.")
            save_tokens()

def save_tokens(tokens):
    with open(TOKENS_FILE, 'w') as file:
        json.dump(tokens, file)

def upsert_contact(email, name):
    contact = Contact.query.filter_by(email=email).first()
    if contact:
        contact.name = name if name else contact.name
        db.session.commit()
        return contact.to_dict(), 'updated'
    else:
        new_contact = Contact(email=email, name=name)
        db.session.add(new_contact)
        db.session.commit()
        return new_contact.to_dict(), 'created'

def upsert_hubspot_contact(email, name, access_token):
    url = f"https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{email}/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "properties": [
            {"property": "email", "value": email},
            {"property": "firstname", "value": name},
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def refresh_hubspot_token():
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': TOKENS.get('refresh_token')
    }
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code != 200:
        print("Error refreshing token:", response.json())
        return None
    
    tokens = response.json()
    TOKENS['access_token'] = tokens['access_token']
    TOKENS['refresh_token'] = tokens['refresh_token']
    TOKENS['expires_in'] = tokens['expires_in']
    TOKENS['last_refreshed'] = time.time()
    save_tokens(tokens)
    print("Tokens refreshed:", tokens)
    return tokens['access_token']


def get_hubspot_token():
    current_time = time.time()
    if (current_time - TOKENS['last_refreshed']) >= TOKENS['expires_in']:
        return refresh_hubspot_token()
    return TOKENS['access_token']

load_tokens()