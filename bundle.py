# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "muutils>=0.8.10",
# ]
# ///

from pathlib import Path

from muutils.web.bundle_html import InlineConfig, inline_html_file

inline_html_file(
    html_path=Path("src/index.html"),
    output_path=Path("bundled/index.html"),
    config=InlineConfig(
		local=True,
		remote=False,
	),
)