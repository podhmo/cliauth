import webbrowser
import sys


def scopes_info() -> None:
    url = "https://developers.google.com/identity/protocols/googlescopes"
    print(f"opening {url}", file=sys.stderr)
    webbrowser.open(url, new=1, autoraise=True)


def credentials_info() -> None:
    url = "https://console.cloud.google.com/apis/credentials"
    print(f"opening {url}", file=sys.stderr)
    webbrowser.open(url, new=1, autoraise=True)
