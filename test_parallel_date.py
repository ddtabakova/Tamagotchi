import unittest

from parallel_date import ParallelDate


class ParallelDateTest(unittest.TestCase):

    def test_seconds(self):
        date = ParallelDate(144.0)
        self.assertEqual(date.get_seconds(), '0')

    def test_update_date(self):
        date = ParallelDate(144.0)
        date.update_date(1)
        self.assertEqual(date.get_minutes(), '2')

if __name__ == '__main__':
    unittest.main()
