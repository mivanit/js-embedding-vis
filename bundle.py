# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "muutils>=0.8.10",
# ]
# ///

from pathlib import Path

from muutils.web.bundle_html import InlineConfig, inline_html_file

if __name__ == "__main__":
    out_path: Path = Path("bundled/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    inline_html_file(
        html_path=Path("src/index.html"),
        output_path=out_path,
        config=InlineConfig(
            local=True,
            remote=False,
        ),
    )
