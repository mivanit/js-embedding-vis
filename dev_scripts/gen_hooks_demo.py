"""Generate the iris-hooks demo: bundled HTML with inline config + hooks JS."""

import json
from pathlib import Path

from js_embedding_vis.inline_cfg import fetch_jev_pkg, inline_config, inline_hooks

ROOT = Path(__file__).resolve().parent.parent

HOOKS_JS = r"""
HOOKS.onReady = async (pointCloud, uiManager) => {
    let useCustomColor = false;

    document.getElementById('customColorToggle')
        .addEventListener('change', (e) => {
            useCustomColor = e.target.checked;
            pointCloud._updateColors();
        });

    HOOKS.colorOverrideFn = (rowIndex, row) => {
        if (!useCustomColor) return null;
        // petal length ranges ~1.0 to 6.9 in the iris dataset
        const val = parseFloat(row['data.petal length (cm)']);
        const t = Math.max(0, Math.min(1, (val - 1) / 5.9));
        return { r: t, g: 0.2, b: 1 - t };
    };

    HOOKS.hoverExtendFn = (rowIndex, row) => {
        const pl = parseFloat(row['data.petal length (cm)']);
        const pw = parseFloat(row['data.petal width (cm)']);
        return '<b>Petal area</b>: ' + (pl * pw).toFixed(2) + ' cm\u00B2';
    };

    // Populate the Dataset Info panel
    const rows = pointCloud.model.df.data;
    const counts = {};
    for (const row of rows) {
        const species = row['target_name'] || 'unknown';
        counts[species] = (counts[species] || 0) + 1;
    }
    const lines = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])
        .map(([name, n]) => `<b>${name}</b>: ${n}`)
        .join('<br>');
    const el = document.getElementById('datasetInfoBody');
    if (el) el.innerHTML = `<b>Total points:</b> ${rows.length}<br><br>${lines}`;
};
""".strip()


def main() -> None:
    cfg_path = ROOT / "docs" / "_configs" / "iris-hooks.json"
    out_path = ROOT / "docs" / "iris-hooks" / "index.html"

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    html = fetch_jev_pkg()
    html = inline_config(cfg, html)
    html = inline_hooks(HOOKS_JS, html)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
