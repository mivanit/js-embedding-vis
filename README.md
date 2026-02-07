# js-embedding-vis

3D interactive embedding/point cloud visualization. Useful for exploring t-SNE, UMAP, PCA, and other dimensionality reduction results.

See [`miv.name/js-embedding-vis/digits/`](https://miv.name/js-embedding-vis/digits/) for a demo. Best viewed in fullscreen mode, kind of works on mobile but not ideal.

[![](docs/screenshot.png)](https://miv.name/js-embedding-vis/digits/)

Raw source code in `src/`, a bundled version (not including `three.js`) in `bundled/`.

## Usage

To create your own visualization:

1. Copy a demo folder (e.g., `docs/iris/`) as a template
2. Replace the `.jsonl` data file with your data
3. Edit `config.json` to match your column names
4. Serve via any HTTP server (e.g., `python -m http.server`)

**Note:** Must be served via HTTP - won't work from `file://` due to browser security restrictions.

## Highlight Groups

You can highlight specific groups of points via URL parameters or config.json. Each group specifies a column to match against and values to highlight.

### URL Format

```
?highlight.<groupname>.col=<column>&highlight.<groupname>.values=<val1>,<val2>&highlight.<groupname>.color=<hex>
```

- `col` - Column name to match against
- `values` - Comma-separated values to highlight
- `color` - (Optional) Hex color like `%23ff0000` (URL-encoded `#ff0000`)

### Examples

Highlight setosa flowers in red:
[`iris/?highlight.setosa.col=target_name&highlight.setosa.values=setosa&highlight.setosa.color=%23ff0000`](https://miv.name/js-embedding-vis/iris/?highlight.setosa.col=target_name&highlight.setosa.values=setosa&highlight.setosa.color=%23ff0000)

Multiple groups (setosa red, versicolor blue):
[`iris/?highlight.setosa.col=target_name&highlight.setosa.values=setosa&highlight.setosa.color=%23ff0000&highlight.versicolor.col=target_name&highlight.versicolor.values=versicolor&highlight.versicolor.color=%230066ff`](https://miv.name/js-embedding-vis/iris/?highlight.setosa.col=target_name&highlight.setosa.values=setosa&highlight.setosa.color=%23ff0000&highlight.versicolor.col=target_name&highlight.versicolor.values=versicolor&highlight.versicolor.color=%230066ff)

### Config.json Format

```json
{
  "highlightGroups": {
    "setosa": {
      "col": "target_name",
      "values": ["setosa"],
      "color": "#ff0000"
    },
    "versicolor": {
      "col": "target_name",
      "values": ["versicolor"]
    }
  }
}
```

Groups without an explicit `color` get auto-assigned colors that can be randomized with the randomize colors button.

## Controls

### Movement

| Key   | Action                                    |
| ----- | ----------------------------------------- |
| WASD  | Move around the 3D space                  |
| Mouse | Look around (double-click to lock cursor) |
| Q / E | Roll camera left/right                    |
| Shift | Sprint (faster movement)                  |
| ESC   | Exit mouse-look mode                      |

### Panels

Press key to toggle:

| Key | Panel                                    |
| --- | ---------------------------------------- |
| H   | Help menu                                |
| M   | Main controls menu                       |
| I   | Info panel (selected points)             |
| L   | Legend panel (color scheme)              |
| N   | Navigation panel (3D compass)            |
| J   | Performance stats (FPS, camera position) |

### Toggles

| Key | Toggle                  |
| --- | ----------------------- |
| K   | Hover tooltips          |
| B   | Click-to-select         |
| O   | Right-click actions     |
| P   | Middle-click info boxes |

### Data Interaction

| Key | Action                          |
| --- | ------------------------------- |
| C   | Cycle through color-by columns  |
| V   | Cycle through selection columns |

### Touch Controls (Mobile)

| Gesture    | Action           |
| ---------- | ---------------- |
| Tap        | Select point     |
| Hold       | Show point info  |
| Drag       | Pan/rotate view  |
| Pinch      | Zoom in/out      |
| Double tap | Lock/unlock view |

## Interaction

- **Click** - Select/deselect a point (when click-to-select is enabled)
- **Right-click** - Show point data or open URL (when enabled)
- **Middle-click** - Create a draggable info box for the point (when enabled)
- **Hover** - Show tooltip with point details (when enabled)

## Configuration

- All settings are automatically saved to the URL
- Use the **Export Current Config** button in the controls menu (M) to get a JSON file
- URL parameters override `config.json` settings
- Use **Reset Config** to return to loaded defaults

### Key config.json Options

```json
{
  "dataFile": "data.jsonl",
  "defaultColorColumn": "category",
  "defaultSelectionColumn": "category",
  "hoverColumns": ["name", "value1", "value2"],
  "numericalPrefix": "pc."
}
```

## Data Format

Data is loaded from JSONL (JSON Lines) format - one JSON object per line:

```jsonl
{"name": "point1", "pc.1": 0.5, "pc.2": -0.3, "pc.3": 0.1, "category": "A"}
{"name": "point2", "pc.1": -0.2, "pc.2": 0.8, "pc.3": -0.4, "category": "B"}
```

- Columns prefixed with `pc.` (configurable via `numericalPrefix`) are treated as numeric dimensions for the 3D axes
- Other columns can be used for coloring, selection, and display
- Numeric columns use a viridis gradient colormap; categorical columns use distinct colors

### CSV Format (Simple)

CSV files are also supported with a simple parser:

```csv
name,pc.1,pc.2,pc.3,category
point1,0.5,-0.3,0.1,A
point2,-0.2,0.8,-0.4,B
```

**Limitations:** The CSV parser splits on commas and newlines directly. Fields cannot contain commas or newlines. For data with special characters, use JSONL format instead.