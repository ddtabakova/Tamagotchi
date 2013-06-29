import unittest

from progress_bars_controller import ProgressBarController


class ProgressBarControllerTest(unittest.TestCase):

    def test_attributes(self):
        pbs = {'test1': None, 'test2':  None, 'test3': None}
        pb_controller = ProgressBarController(pbs)

        self.assertIn('test1', dir(pb_controller))
        self.assertIn('test2', dir(pb_controller))
        self.assertIn('test3', dir(pb_controller))

if __name__ == '__main__':
    unittest.main()
