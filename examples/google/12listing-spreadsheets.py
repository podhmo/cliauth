from handofcats import as_command
import requests
import subprocess
import json


@as_command
def run():
    import logging

    logging.basicConfig(level=logging.DEBUG)

    p = subprocess.run(
        "python -m cliauth.google access_token".split(" "),
        text=True,
        capture_output=True,
    )
    access_token = json.loads(p.stdout)["access_token"]

    session = requests.Session()
    session.headers.update({"Authorization": "Bearer %s" % access_token})

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
