from handofcats import as_command
from cliauth.google.authflow import Flow, Config
from google.auth.transport.requests import AuthorizedSession


@as_command
def run():
    import logging

    logging.basicConfig(level=logging.DEBUG)

    c = Config()
    credentials = Flow(c).get_credentials(scopes=None)
    session = AuthorizedSession(credentials)

    page_token = ""
    url = "https://www.googleapis.com/drive/v3/files"

    params = {
        "q": "mimeType='application/vnd.google-apps.spreadsheet'",
        "pageSize": 1000,
        "supportsTeamDrives": True,
        "includeTeamDriveItems": True,
        "fields": "nextPageToken,files(name,id)",
    }

    while page_token is not None:
        if page_token:
            params["pageToken"] = page_token

        res = session.request("get", url, params=params)
        assert res.status_code == 200, res.status_code
        data = res.json()
        for file in data.get("files", []):
            print(f'Found file: {file.get("name")} ({file.get("id")})')

        page_token = data.get("nextPageToken", None)
        if page_token is None:
            break
