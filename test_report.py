import unittest
from datetime import date
from report import summarize

def order(id, status='new', due='2026-10-18', cents='1200'):
    return {'id':id,'customer_id':'1','status':status,'due_on':due,'total_cents':cents}
class ReportTests(unittest.TestCase):
    def test_overdue_open_orders_only(self):
        rows=[order('1'),order('2','processing',cents='300'),order('3','shipped'),order('4',due='2026-10-19'),order('5','completed')]
        self.assertEqual(summarize(rows,date(2026,10,19)),[{'customer_id':'1','order_count':2,'total_cents':1500,'oldest_due_on':'2026-10-18'}])
    def test_invalid_input_is_not_silently_published(self):
        with self.assertRaises(ValueError): summarize([order('1'),order('1')],date(2026,10,19))
        with self.assertRaises(ValueError): summarize([order('1',cents='-1')],date(2026,10,19))
    def test_no_overdue_orders(self):
        self.assertEqual(summarize([order('1',due='2026-10-20')],date(2026,10,19)),[])
if __name__=='__main__': unittest.main()
