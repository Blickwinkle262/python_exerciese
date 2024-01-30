import unittest
from stock import Stock

class TestStock(unittest.TestCase):
    def test_create_stock(self):
        stock = Stock('GOOG',100,490.10)
        self.assertEqual(stock.name,'GOOG')
        self.assertEqual(stock.shares,100)
        self.assertEqual(stock.price,490.10)

if __name__ == '__main__':
    unittest.main()