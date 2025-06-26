# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "scikit-learn",
# ]
# ///

from pathlib import Path
import json

import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA

def write_data_jsonl(
	data_raw: dict,
	output_path: Path,
	include_raw: bool = True,
) -> None:

	data_pca: PCA = PCA(n_components=3)
	_ = data_pca.fit(data_raw["data"])
	pca_values: np.ndarray = data_pca.transform(data_raw["data"])

	data_transformed: list[dict[str, float | int | str]] = [
		{
			# principal components
			**{
				f"pc.{i + 1}": float(pc_val)
				for i, pc_val in enumerate(pca_row)
			},
			# target
			"target_int": int(data_raw["target"][idx]),
			"target_name": str(
				data_raw["target_names"][data_raw["target"][idx]]
			),
			**(
				{} if not include_raw else
				{
					f"data.{feat_name}": float(row[i])
					for i, feat_name in enumerate(data_raw["feature_names"])
				}
			),
		}
		for idx, (row, pca_row) in enumerate(zip(data_raw["data"], pca_values))
	]

	# quick checks
	assert len(data_transformed) == len(data_raw["data"])
	assert {"pc.1", "pc.2", "pc.3"} <= data_transformed[0].keys()

	# save to JSON
	with output_path.open("w") as f:
		for item in data_transformed:
			f.write(json.dumps(item) + "\n")

if __name__ == "__main__":
	import sys
	match sys.argv[1]:
		case "iris":
			write_data_jsonl(
				data_raw=datasets.load_iris(),
				output_path=Path("docs/iris/iris.jsonl"),
			)
		case "digits":
			write_data_jsonl(
				data_raw=datasets.load_digits(),
				output_path=Path("docs/digits/digits.jsonl"),
				include_raw=False,
			)
		