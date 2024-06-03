from flask import Blueprint, request, jsonify, redirect
from helpers import upsert_contact, upsert_hubspot_contact, get_hubspot_token, save_tokens, load_tokens
import requests
import time
import os
import json

webhook_bp = Blueprint('webhook_bp', __name__)

CLIENT_ID = 'a103975e-0126-43ca-a5c7-c0ae3c3a62c2'
CLIENT_SECRET = 'e7d3f137-a889-43fd-b3f2-3b0fb31969a0'
REDIRECT_URI = 'http://localhost:5000/oauth-callback'
SCOPES = 'crm.objects.contacts.write oauth crm.objects.contacts.read'

AUTHORIZATION_URL = 'https://app.hubspot.com/oauth/authorize'

TOKENS_FILE = 'tokens.json'

TOKENS = {
    'access_token': None,
    'refresh_token': None,
    'expires_in': 0,
    'last_refreshed': 0
}

@webhook_bp.route('/authorize')
def authorize():
    scopes = SCOPES.replace(' ', '%20')
    auth_url = f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)

@webhook_bp.route('/oauth-callback')
def oauth_callback():
    global TOKENS
    code = request.args.get('code')
    token_url = 'https://api.hubapi.com/oauth/v1/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch tokens from HubSpot', 'details': response.json()}), response.status_code
    
    tokens = response.json()
    
    if 'access_token' not in tokens or 'refresh_token' not in tokens:
        return jsonify({'error': 'Invalid response from HubSpot', 'details': tokens}), 500

    TOKENS = {
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'expires_in': tokens['expires_in'],
        'last_refreshed': time.time()
    }
    
    save_tokens(TOKENS)

    return jsonify({'message': 'Tokens received', 'tokens': tokens, 'updated_tokens': TOKENS})


@webhook_bp.route('/refresh-token')
def refresh_token():
    global TOKENS
    token_url = 'https://api.hubapi.com/oauth/v1/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': TOKENS.get('refresh_token')
    }
    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to refresh token', 'details': response.json()}), response.status_code
    
    tokens = response.json()
    TOKENS.update({
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'expires_in': tokens['expires_in'],
        'last_refreshed': time.time()
    })
    save_tokens(TOKENS)
    print(tokens)
    return jsonify({'message': 'Access token refreshed', 'access_token': tokens['access_token'], 'updated_tokens': TOKENS})


@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    access_token = get_hubspot_token()
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 500
    
    hubspot_result = upsert_hubspot_contact(email, name, access_token)
    if 'status' in hubspot_result and hubspot_result['status'] == 'error':
        return jsonify({'error': 'Failed to update HubSpot contact', 'details': hubspot_result}), 500
    
    return jsonify({'hubspot_result': hubspot_result})
