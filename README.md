# KeyCloak JWT Application Testing

The goal of this application is to provide an authentication frontend that queries Keycloak and prints out the JWT token to the screen. 

The purpose is for testing authentications options from RedHat SSO or Keycloak.

#### Quickstart

To run the web server:

```bash
# Start the server
docker run -d --name keycloak-client \
            -p 8000:8000 \ 
            -e KEYCLOAK_HOST='https://keycloak-server/' \
            -e KEYCLOAK_REALM='keycloak-realm' \
            -e KEYCLOAK_CLIENT='keycloak-client' \
            -e KEYCLOAK_CLIENT_SECRET='keycloak-client-secret' \
            ironrainindustries/kc-django:bc-01

# Run database migrations
docker exec keycloak-client python manage.py makemigrations

```

#### Environment Variables
`KEYCLOAK_HOST` - URL to the Keycloak host.
`KEYCLOAK_REALM` - The Realm within Keycloak being used.
`KEYCLOAK_CLIENT` - The Client within the Realm, users can be in multiple clients but only one Realm.
`KEYCLOAK_CLIENT_SECRET` - The Client secret, the Client `Access Type` must be set to `confidential` to access the secret under the `Credentials` tab.
`KEYCLOAK_AUDIENCE` - Required for the POST, will need changing if the default audience, `account` is changed on the Keycloak side.

#### Notes
The database is non-persistent as the application is 
