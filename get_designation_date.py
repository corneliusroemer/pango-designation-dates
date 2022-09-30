import datetime as dt
import io
from collections import defaultdict
from typing import DefaultDict

import pandas as pd
from dateutil import parser
from pydriller import Repository
from tqdm import tqdm

while True:
    first_mention: DefaultDict[str, dt.datetime] = defaultdict(None)
    df = pd.read_csv("data/lineage_designation_date.csv", index_col=0)
    for index, row in df.iterrows():
        first_mention[index] = parser.parse(row["designation_date"])
    SINCE = parser.parse(df.designation_date.max()) - dt.timedelta(days=5)
    TO = SINCE + dt.timedelta(days=50)
    # PATH = "~/code/pango-designation" # Local path
    PATH = "https://github.com/cov-lineages/pango-designation"  # CI
    repo = Repository(
        "~/code/pango-designation", filepath="lineages.csv", since=SINCE, to=TO
    )
    total_commits = len(list(repo.traverse_commits()))
    for commit in tqdm(repo.traverse_commits(), total=total_commits):
        for file in commit.modified_files:
            if file.filename == "lineages.csv":
                code = file.source_code
                df = pd.read_csv(io.StringIO(code))
                for lineage in df.lineage.unique():
                    if lineage not in first_mention:
                        first_mention[lineage] = commit.committer_date.date()

    df = pd.DataFrame.from_dict(
        first_mention, orient="index", columns=["designation_date"]
    )
    df.to_csv("data/lineage_designation_date.csv", index_label="lineage")
    print(f"Done with {SINCE} to {TO}")
    if TO > dt.datetime.now() + dt.timedelta(days=30):
        break


# %%
