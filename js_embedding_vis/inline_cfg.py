from pathlib import Path
from typing import Final, Literal, Optional
from urllib.request import Request, urlopen
import json

HtmlSource = Literal["remote", "pkg"]

HTML_URL: Final[str] = (
    "https://raw.githubusercontent.com/mivanit/js-embedding-vis/refs/heads/main/bundled/index.html"
)

REPLACE_CONFIG_STRING: Final[str] = "/*$$$INLINE_CONFIG$$$*/"
REPLACE_CONFIG_FMT: Final[str] = "var INLINE_CONFIG = {cfg_json};"

REPLACE_HOOKS_STRING: Final[str] = "/*$$$INLINE_HOOKS$$$*/"
REPLACE_HOOKS_FMT: Final[str] = "{hooks_js}"


def fetch_jev_remote(url: str = HTML_URL) -> str:
    """Fetch the bundled HTML for `js-embedding-vis` directly from GitHub

    # Returns:
     - `str`
        Raw HTML contents of the file
    """
    headers = {
        "User-Agent": "python-urllib",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    with urlopen(
        Request(url, headers=headers),
    ) as resp:
        return resp.read().decode(resp.headers.get_content_charset("utf-8"))


def fetch_jev_pkg() -> str:
    import importlib.resources
    import js_embedding_vis

    index_html_pkg_path: Path = (
        Path(importlib.resources.files(js_embedding_vis)) / "index.html"
    )
    return index_html_pkg_path.read_text(encoding="utf-8")


def fetch_jev(
    src: HtmlSource = "pkg",
) -> str:
    if src == "remote":
        return fetch_jev_remote()
    elif src == "pkg":
        return fetch_jev_pkg()
    else:
        raise ValueError(f"Invalid source '{src}'. Expected 'remote' or 'pkg'.")


def inline_config(
    cfg: dict | str,
    html: str,
    replace_config_string: str = REPLACE_CONFIG_STRING,
    replace_config_fmt: str = REPLACE_CONFIG_FMT,
) -> str:
    """Inline the config into the HTML file"""

    cfg_json: str = cfg if isinstance(cfg, str) else json.dumps(cfg, indent=2)

    # check the replace string is present exactly once
    n_occurrences: int = html.count(replace_config_string)
    if n_occurrences != 1:
        raise ValueError(
            f"Expected exactly one occurrence of '{replace_config_string}' in the HTML, "
            f"found {n_occurrences} occurrences."
        )

    return html.replace(
        replace_config_string,
        replace_config_fmt.format(cfg_json=cfg_json),
    )


def inline_hooks(
    hooks_js: str,
    html: str,
    replace_hooks_string: str = REPLACE_HOOKS_STRING,
    replace_hooks_fmt: str = REPLACE_HOOKS_FMT,
) -> str:
    """Inline raw JS that sets HOOKS properties into the HTML file"""

    n_occurrences: int = html.count(replace_hooks_string)
    if n_occurrences != 1:
        raise ValueError(
            f"Expected exactly one occurrence of '{replace_hooks_string}' in the HTML, "
            f"found {n_occurrences} occurrences."
        )

    return html.replace(
        replace_hooks_string,
        replace_hooks_fmt.format(hooks_js=hooks_js),
    )


def write_inlined_config(
    cfg: dict | str | None = None,
    cfg_path: Optional[Path] = None,
    html: Optional[str] = None,
    html_src: HtmlSource = "pkg",
    out_path: Path = "bundled/index.html",
    replace_config_string: str = REPLACE_CONFIG_STRING,
    replace_config_fmt: str = REPLACE_CONFIG_FMT,
) -> None:
    if cfg is None and cfg_path is None:
        raise ValueError("Either `cfg` or `cfg_path` must be provided.")

    if cfg is not None and cfg_path is not None:
        raise ValueError("Only one of `cfg` or `cfg_path` can be provided.")

    if cfg_path is not None:
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config file {cfg_path} does not exist.")
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    html_: str
    if html is None:
        html_ = fetch_jev(src=html_src)
    else:
        html_ = html

    inlined_html: str = inline_config(
        cfg=cfg,
        html=html_,
        replace_config_string=replace_config_string,
        replace_config_fmt=replace_config_fmt,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(inlined_html)


def main() -> None:
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
    arg_parser.add_argument(
        "--html-src",
        type=str,
        choices=["remote", "pkg"],
        default="pkg",
        help=(
            "Source of the HTML file to inline the config into. "
            "Use 'remote' to fetch from GitHub, or 'pkg' to use the local package version."
        ),
    )

    args: argparse.Namespace = arg_parser.parse_args()

    write_inlined_config(
        cfg=args.cfg,
        cfg_path=args.cfg_path,
        out_path=args.out_path,
        html_src=args.html_src,
    )


if __name__ == "__main__":
    main()
