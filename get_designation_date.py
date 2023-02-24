import datetime as dt
import io
import os
from collections import defaultdict
from typing import DefaultDict

import pandas as pd
from dateutil import parser
from pydriller import Repository
from tqdm import tqdm
import typer


def main(
    pango_path: str = "~/code/pango-designation",
):
    # PANGO_PATH = "~/code/pango-designation"  # Local path
    # PANGO_PATH = "https://github.com/cov-lineages/pango-designation"  # CI
    # PANGO_PATH = "pango-designation"  # CI
    # Find out if there are new commits
    # if file exists
    TIMESTAMP_FILE = "data/previous_commit_timestamp.txt"
    if not os.path.exists(TIMESTAMP_FILE):
        print("No previous commit timestamp found. Exiting.")
        exit()

    with open(TIMESTAMP_FILE, "r") as f:
        previous_commit_datetime = parser.parse(f.read())

    repo = Repository(
        pango_path, filepath="lineages.csv" #, since=previous_commit_datetime
    )

    commits = list(repo.traverse_commits())
    total_commits = len(commits)

    new_commits = [
        commit
        for commit in commits
        # if commit.author_date > previous_commit_datetime
    ]
    if len(new_commits) > 0:
        print("New commits found ... ", len(new_commits))
    else:
        print("No new commits found")
    #     return 1

    first_mention: DefaultDict[str, dt.datetime] = defaultdict(None)
    df = pd.read_csv("data/lineage_designation_date.csv", index_col=0)
    for index, row in df.iterrows():
        try:
            first_mention[index] = parser.parse(row["designation_date"])
        except:
            first_mention[index] = None
    # SINCE = parser.parse(df.designation_date.max()) - dt.timedelta(days=5)
    # TO = SINCE + dt.timedelta(days=50)
    for commit in tqdm(commits, total=total_commits):
        for file in commit.modified_files:
            if file.filename == "lineages.csv":
                code = file.source_code
                df = pd.read_csv(io.StringIO(code))
                for lineage in df.lineage.unique():
                    if lineage not in first_mention:
                        first_mention[lineage] = commit.committer_date.isoformat()

    df = pd.DataFrame.from_dict(
        first_mention, orient="index", columns=["designation_date"]
    )
    df.to_csv("data/lineage_designation_date.csv", index_label="lineage")

    print("Updating timestamp")
    most_recent_commit = commits[-1]
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(most_recent_commit.author_date.isoformat())

    # Print dates and hashes of recent commits
    for commit in commits:
        print(commit.author_date, commit.hash)


if __name__ == "__main__":
    typer.run(main)
