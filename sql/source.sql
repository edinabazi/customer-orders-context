-- Replace the database/schema/table with the authorized production source.
SELECT id, customer_id, status, total_cents, created_on, due_on
FROM orders;
