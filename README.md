# js-embedding-vis

3D interactive embedding/point cloud visualization.

See [`miv.name/js-embedding-vis/digits/`](https://miv.name/js-embedding-vis/digits/) for a demo. Best viewed in fullscreen mode, kind of works on mobile but not ideal.

[![](docs/screenshot.png)](https://miv.name/js-embedding-vis/digits/)

Raw source code in `src/`, a bundled version (not including `three.js`) in `bundled/`.

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