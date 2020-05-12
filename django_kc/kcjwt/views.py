import os
import requests
import json
import jwt

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import RequestTokenForm

KEYCLOAK_HOST = os.environ.get('KEYCLOAK_HOST')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM')
KEYCLOAK_CLIENT = os.environ.get('KEYCLOAK_CLIENT')
KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_AUDIENCE = os.environ.get('KEYCLOAK_AUDIENCE')

# Create your views here.
@login_required
def index(request):

    form = RequestTokenForm()
    context = {
        'form': form
    }
    return render(request, 'index.html', context)

@login_required
def token_request(request):
    
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('user_pass')

        kc_host = KEYCLOAK_HOST
        realm = KEYCLOAK_REALM

        client_id = KEYCLOAK_CLIENT
        client_secret = KEYCLOAK_CLIENT_SECRET
        username = username
        password = password

        pub_key_url = kc_host + '/auth/realms/' + KEYCLOAK_REALM

        raw_pub_key =  json.loads(requests.get(pub_key_url).text)['public_key']

        if KEYCLOAK_AUDIENCE:
            audience = KEYCLOAK_AUDIENCE
        else: 
            audience = 'account'
    
        formatted_key = """-----BEGIN PUBLIC KEY-----
""" + raw_pub_key + """
-----END PUBLIC KEY-----"""

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username, 
            'password': password,
            'grant_type': 'password'
        }

        token_url = kc_host + '/auth/realms/' + realm + '/protocol/openid-connect/token'

        token_req = requests.post(token_url, data)

        json_token = json.loads(token_req.text)

        decoded_token = jwt.decode(json_token['access_token'], formatted_key, algorithms=['RS256'], audience=audience)

        response_data = {}

        response_data['result'] = 200
        
        for key in decoded_token:
            response_data[key] = decoded_token[key]            

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"Double check the details."}),
            content_type="application/json"
        )
