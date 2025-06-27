# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "muutils>=0.8.10",
# ]
# ///
"bundling script for the JS embedding visualizations"

from pathlib import Path

from muutils.web.bundle_html import InlineConfig, inline_html_file

if __name__ == "__main__":
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

    args: argparse.Namespace = arg_parser.parse_args()

    args.out_path.parent.mkdir(parents=True, exist_ok=True)

    inline_html_file(
        html_path=args.in_path,
        output_path=args.out_path,
        config=InlineConfig(
            local=True,
            remote=args.remote,
        ),
    )
