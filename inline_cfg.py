from types import TracebackType
from typing import Final, Optional, Type
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HTML_URL: Final[str] = (
    "https://raw.githubusercontent.com/"
    "mivanit/js-embedding-vis/refs/heads/main/bundled/index.html"
)

def fetch_jev_html(url: str = HTML_URL) -> str:
    """Fetch the bundled HTML for `js-embedding-vis` directly from GitHub

    # Returns:
     - `str`
        Raw HTML contents of the file
    """
    with urlopen(
            Request(url, headers={"User-Agent": "python-urllib"}),
        ) as resp:
        return resp.read().decode(resp.headers.get_content_charset("utf-8"))
