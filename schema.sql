CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  account_owner TEXT NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  status TEXT NOT NULL CHECK (status IN ('new','processing','shipped','completed','cancelled')),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  created_on DATE NOT NULL,
  due_on DATE NOT NULL
);

CREATE INDEX orders_customer_id_idx ON orders(customer_id);
CREATE INDEX orders_status_idx ON orders(status);
