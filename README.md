# Customer and order records

A synthetic planning example for an operations team working with an existing database.

## Business context

A small company stores customer and order records in Postgres. Operations staff need to search customers, review orders and update order status. Viewers should only read records; managers should also make changes. The company has limited engineering capacity and wants minimal ongoing maintenance.

No application, frontend framework, hosting provider or integration approach has been chosen. The database should remain the source of truth.

## Data

- `schema.sql`: customers and orders tables, constraints and indexes.
- `seed.sql`: deterministic synthetic records for that schema.
- `data/customers.csv` and `data/orders.csv`: readable versions of the same records.
- `data/summary.json`: reference date, row counts and status distribution.

The reference date is 2026-10-17. Orders have statuses new, processing, shipped, completed or cancelled. Allowed forward transitions are new to processing or cancelled, processing to shipped or cancelled, and shipped to completed. Completed and cancelled are terminal states. The schema limits allowed status values; a future implementation must enforce transition rules separately.

## Starting state and limits

These are synthetic example records, not a production export. No database server, API, application or credentials are included. The SQL can initialize a separately supplied test Postgres database. Schema and snapshots are sufficient for a planning task; a connected or deployed application requires a database/API reachable from its runtime and authorized test credentials.

When building a demonstration from the snapshots, identify it as synthetic and state its storage mechanism. A local demonstration or imported snapshot does not establish a connection to an existing live database.
