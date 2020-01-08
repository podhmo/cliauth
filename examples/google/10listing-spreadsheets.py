from handofcats import as_command
from cliauth.google.authflow import Flow, Config
from cliauth.google.discovery import Cache, build


@as_command
def run():
    import logging

    logging.basicConfig(level=logging.DEBUG)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    c = Config(skip_verify=True)
    credentials = Flow(c).get_credentials_in_loop(scopes)

    resource = build("drive", "v3", credentials=credentials, cache=Cache(c))

    page_token = ""
    for i in range(10):
        q = "mimeType='application/vnd.google-apps.spreadsheet'"
        response = (
            resource.drives()
            .list(
                q=q,
                pageSize=100,
                fields="nextPageToken,files(id,name)",
                # supportsTeamDrives=True,
                # includeTeamDriveItems=True,
            )
            .execute()
        )
        print(response)

        for file in response.get("files", []):
            print(f'Found file: {file.get("name")} (file.get("id"))')

        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
