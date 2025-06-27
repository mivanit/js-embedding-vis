# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "muutils>=0.8.10",
# ]
# ///
"bundling script for the JS embedding visualizations"

from pathlib import Path
import tomllib

from muutils.web.bundle_html import InlineConfig, inline_html_file, inline_html_assets

if __name__ == "__main__":
    # parse args
    import argparse

    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Bundle the HTML file for the JS embedding visualizations."
    )
    arg_parser.add_argument(
        "--in-path",
        type=Path,
        default=Path("src/index.html"),
        help="Path to the input HTML file to bundle.",
    )
    arg_parser.add_argument(
        "--out-path",
        type=Path,
        default=Path("bundled/index.html"),
        help="Path to the output bundled HTML file.",
    )
    arg_parser.add_argument(
        "--remote",
        action="store_true",
        help="Inline remote resources (CDN links) into the HTML file.",
    )
    arg_parser.add_argument(
        "--prettify",
        action="store_true",
        help="Prettify the output HTML file. (requires bs4)",
    )

    args: argparse.Namespace = arg_parser.parse_args()

    # bundle HTML file
    in_path: Path = Path(args.in_path)
    html_raw: str = in_path.read_text(encoding="utf-8")
    html_new: str = inline_html_assets(
        html_raw,
        base_path=in_path.parent,
        config=InlineConfig(
            local=True,
            remote=args.remote,
        ),
        prettify=args.prettify,
    )

    # add version info
    version: str = tomllib.loads(
        Path("pyproject.toml").read_text(encoding="utf-8")
    )["project"]["version"]
    html_new = html_new.replace(
        "/*$$$VERSION$$$*/",
        f"version: v{version}",
    )

    # write
    out_path: Path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_new)

