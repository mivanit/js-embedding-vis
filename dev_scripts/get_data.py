# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "scikit-learn",
# ]
# ///
"data loading/generation script for demo"

from pathlib import Path
import json
from typing import TypedDict

import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA


class DataRaw(TypedDict):
    data: np.ndarray  # shape (n_samples, n_features)
    target: np.ndarray  # shape (n_samples,) all values in range [0, n_classes)
    target_names: list[str]  # length n_classes
    feature_names: list[str]  # length n_features


def write_data_jsonl(
    data_raw: DataRaw,
    output_path: Path,
    include_raw: bool = True,
) -> None:
    data_pca: PCA = PCA(n_components=3)
    _ = data_pca.fit(data_raw["data"])
    pca_values: np.ndarray = data_pca.transform(data_raw["data"])

    data_transformed: list[dict[str, float | int | str]] = [
        {
            # principal components
            **{f"pc.{i + 1}": float(pc_val) for i, pc_val in enumerate(pca_row)},
            # target
            "target_int": int(data_raw["target"][idx]),
            "target_name": str(data_raw["target_names"][data_raw["target"][idx]]),
            **(
                {}
                if not include_raw
                else {
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
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        for item in data_transformed:
            f.write(json.dumps(item) + "\n")


def generate_rand_data(
    n_samples: int = 100_000,
    n_features: int = 5,
    n_classes: int = 10,
) -> DataRaw:
    data: np.ndarray = np.random.randn(n_samples, n_features)
    target: np.ndarray = np.random.randint(0, n_classes, size=n_samples)
    target_names: list[str] = [f"class_{i}" for i in range(n_classes)]
    feature_names: list[str] = [f"feature_{i}" for i in range(n_features)]

    return DataRaw(
        data=data,
        target=target,
        target_names=target_names,
        feature_names=feature_names,
    )


if __name__ == "__main__":
    import sys

    match sys.argv[1]:
        case "iris":
            write_data_jsonl(
                data_raw=datasets.load_iris(),
                output_path=Path("docs/iris/iris.jsonl"),
            )
        case "digits":
            digits = datasets.load_digits()
            # Generate main data file (without pixels)
            write_data_jsonl(
                data_raw=digits,
                output_path=Path("docs/digits/digits.jsonl"),
                include_raw=False,
            )
            # Generate separate pixel data file
            pixel_path = Path("docs/digits/digits-pixels.jsonl")
            with pixel_path.open("w") as f:
                for image in digits.images:
                    f.write(json.dumps(image.flatten().tolist()) + "\n")
        case "stress":
            point_count: int = 100_000
            write_data_jsonl(
                data_raw=generate_rand_data(),
                output_path=Path("docs/stress/stress.jsonl"),
                include_raw=False,
            )
