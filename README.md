# Daily order report

A working local Python script that summarizes overdue open orders from a CSV snapshot. All records are invented.

## Run locally

Python 3.10+ is sufficient; no third-party dependencies are required.

```sh
python3 report.py --as-of 2026-10-19
python3 -m unittest -v
```

The output is `output/overdue-summary.csv`: one row per customer, open overdue order count, total value in integer cents, and earliest due date. Only `new` and `processing` orders with a due date strictly before the reference date count. Re-running the command replaces the same output file; it does not append duplicates.

## Current process

The script works with a local export. Someone runs it manually, checks the generated CSV, then copies the summary into a Google Sheet used by operations. There is no scheduler, hosted runtime, failure notification or live connector in this repository.

## Desired process

The production order records live in Snowflake. The team wants the same summary to refresh a dedicated tab of a Google Sheet at 07:00 Europe/London each weekday, even when nobody's computer is on. Failed runs should notify the report owner and retain the last successful sheet contents. Re-running for the same business date should not duplicate rows. There are about 5,000 source records per day, ten report readers and one operations owner who can edit SQL and small scripts. The team has no infrastructure team.

No hosting, orchestration or integration product has been selected. Keeping the calculation logic is useful, but retaining Python is not a requirement if another approach is simpler to operate.

## Files and limits

- `data/orders.csv` and `data/customers.csv`: synthetic source examples, not a live warehouse export.
- `report.py`: local calculation and CSV output only.
- `sql/source.sql`: intended source projection; the actual database/schema and authorization are not configured.
- `schema.sql` and `seed.sql`: the original relational sample schema and records; not the production deployment or a requirement to use a particular database.
- `examples/overdue-summary.csv`: reproducible output for 2026-10-19.

No Snowflake account, Google Sheet, credentials or connections are supplied. Recommendations can be made from this context; live integration and scheduled operation need separately authorized service access.
