from google.auth import credentials

OAUTH2_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


class Credentials(credentials.ReadOnlyScoped, credentials.Credentials):
    TOKEN_ENDPOINT = OAUTH2_TOKEN_ENDPOINT
