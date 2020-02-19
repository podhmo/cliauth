import webbrowser
import sys


def scopes_info() -> None:
    url = "https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/#available-scopes"
    print(f"opening {url}", file=sys.stderr)
    webbrowser.open(url, new=1, autoraise=True)


def credentials_info() -> None:
    url = "https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#web-application-flow"
    print(f"opening {url}", file=sys.stderr)
    webbrowser.open(url, new=1, autoraise=True)
