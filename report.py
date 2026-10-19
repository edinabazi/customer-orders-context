#!/usr/bin/env python3
"""Produce an overdue-order summary from a local CSV snapshot."""
import argparse
import csv
from datetime import date
from pathlib import Path
import os
import tempfile

def summarize(rows, as_of):
    groups = {}
    seen = set()
    for row in rows:
        if row['id'] in seen:
            raise ValueError('Duplicate order ID: ' + row['id'])
        seen.add(row['id'])
        due = date.fromisoformat(row['due_on'])
        amount = int(row['total_cents'])
        if amount < 0:
            raise ValueError('Negative order amount')
        if row['status'] not in ('new', 'processing') or due >= as_of:
            continue
        cid = row['customer_id']
        g = groups.setdefault(cid, {'customer_id': cid, 'order_count': 0, 'total_cents': 0, 'oldest_due_on': due.isoformat()})
        g['order_count'] += 1
        g['total_cents'] += amount
        g['oldest_due_on'] = min(g['oldest_due_on'], due.isoformat())
    return sorted(groups.values(), key=lambda r: int(r['customer_id']))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('data/orders.csv'))
    parser.add_argument('--output', type=Path, default=Path('output/overdue-summary.csv'))
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    with args.input.open(newline='') as f:
        summary = summarize(csv.DictReader(f), args.as_of)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', newline='', dir=args.output.parent, delete=False) as f:
            temporary = f.name
            writer = csv.DictWriter(f, fieldnames=['customer_id', 'order_count', 'total_cents', 'oldest_due_on'])
            writer.writeheader()
            writer.writerows(summary)
        os.replace(temporary, args.output)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    print(f'Wrote {len(summary)} customer summaries to {args.output} for {args.as_of}')

if __name__ == '__main__':
    main()
