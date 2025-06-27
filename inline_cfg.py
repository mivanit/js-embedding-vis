from pathlib import Path
from typing import Final, Optional
from urllib.request import Request, urlopen
import json

HTML_URL: Final[str] = (
    "https://raw.githubusercontent.com/"
    "mivanit/js-embedding-vis/refs/heads/main/bundled/index.html"
)

REPLACE_CONFIG_STRING: Final[str] = "/*$$$INLINE_CONFIG$$$*/"

REPLACE_CONFIG_FMT: Final[str] = "var INLINE_CONFIG = {cfg_json};"


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


def inline_config(
    cfg: dict | str,
    html: Optional[str] = None,
) -> str:
    """Inline the config into the HTML file"""

    if html is None:
        html = fetch_jev_html()

    cfg_json: str = cfg if isinstance(cfg, str) else json.dumps(cfg, indent=2)

    # check the replace string is present exactly once
    n_occurrences: int = html.count(REPLACE_CONFIG_STRING)
    if n_occurrences != 1:
        raise ValueError(
            f"Expected exactly one occurrence of '{REPLACE_CONFIG_STRING}' in the HTML, "
            f"found {n_occurrences} occurrences."
        )

    return html.replace(
        REPLACE_CONFIG_STRING,
        REPLACE_CONFIG_FMT.format(cfg_json=cfg_json),
    )


def write_inlined_config(
    cfg: dict | str | None = None,
    cfg_path: Optional[Path] = None,
    html: Optional[str] = None,
    out_path: Path = "bundled/index.html",
) -> None:
    if cfg is None and cfg_path is None:
        raise ValueError("Either `cfg` or `cfg_path` must be provided.")

    if cfg is not None and cfg_path is not None:
        raise ValueError("Only one of `cfg` or `cfg_path` can be provided.")

    if cfg_path is not None:
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config file {cfg_path} does not exist.")
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    inlined_html: str = inline_config(cfg, html)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(inlined_html)


if __name__ == "__main__":
    import argparse

    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Inline the config into the HTML file for the JS embedding visualizations."
    )
    arg_parser.add_argument(
        "--cfg",
        type=str,
        help="JSON string to inline as the config.",
    )
    arg_parser.add_argument(
        "--cfg-path",
        type=Path,
        help="Path to a JSON file to inline as the config.",
    )
    arg_parser.add_argument(
        "--out-path",
        type=Path,
        default=Path("bundled/index.html"),
        help="Path to the output HTML file with the inlined config.",
    )

    args: argparse.Namespace = arg_parser.parse_args()

    write_inlined_config(
        cfg=args.cfg,
        cfg_path=args.cfg_path,
        out_path=args.out_path,
    )
