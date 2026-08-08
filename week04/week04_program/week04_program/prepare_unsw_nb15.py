"""Create a small, balanced teaching subset from UNSW-NB15.

Place UNSW_NB15_training-set.csv next to this script, then run:
    python prepare_unsw_nb15.py
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path(__file__).with_name("UNSW_NB15_training-set.csv")
OUTPUT_FILE = Path(__file__).with_name("unsw_nb15_small.csv")
RANDOM_STATE = 42
SAMPLES_PER_CLASS = 5_000

FEATURES = [
    "dur",
    "spkts",
    "dpkts",
    "sbytes",
    "dbytes",
    "rate",
    "sttl",
    "dttl",
    "sload",
    "dload",
    "sloss",
    "dloss",
    "sinpkt",
    "dinpkt",
    "sjit",
    "djit",
    "smean",
    "dmean",
    "ct_srv_src",
    "ct_dst_ltm",
    "ct_src_ltm",
    "ct_srv_dst",
]


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"未找到 {INPUT_FILE.name}。请先从UNSW-NB15官方页面下载训练集，"
            "并将文件放在本脚本所在目录。"
        )

    data = pd.read_csv(INPUT_FILE)
    required = set(FEATURES + ["label"])
    missing = sorted(required.difference(data.columns))
    if missing:
        raise ValueError(f"原始文件缺少必要字段：{missing}")

    data = data[FEATURES + ["label"]].copy()
    data = data.replace([float("inf"), float("-inf")], pd.NA).dropna()
    data = data.drop_duplicates()
    data["label"] = data["label"].astype(int)

    parts = []
    for label, group in data.groupby("label"):
        count = min(SAMPLES_PER_CLASS, len(group))
        parts.append(group.sample(n=count, random_state=RANDOM_STATE))

    result = pd.concat(parts, ignore_index=True)
    result = result.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"已生成：{OUTPUT_FILE}")
    print(f"样本数：{len(result)}")
    print(result["label"].value_counts().sort_index())


if __name__ == "__main__":
    main()

