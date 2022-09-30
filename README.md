# Pango lineage designation dates

This repository attempts to collect the dates on which each Pango lineage was designated.

Unfortunately, there is no file in the pango-designation repo that mentions the date a lineage was added so we have to go dig into the git history (please tell me if there's a better way).

## Possible approaches

- Find first mention in `lineages.csv` file, need to step through history commit by commit and see when a lineage was first mentioned
- First mention in `lineage_notes.txt`
- First mention in commit message

Try all of the above and use the earliest date.

## Output

- `lineage_designation_dates.csv` - CSV file with lineage, date, commit hash and designation release it was first part of

## Uses

- Put as coloring on Nextclade reference trees
