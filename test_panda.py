import unittest

from panda import Panda


class PandaTest(unittest.TestCase):

    def test_above_limit_update(self):
        panda = Panda()
        panda.update_hungry(panda.POSITIVE_UPDATE)
        self.assertEqual(panda.get_feed(), 1.0)

    def test_below_limit_update(self):
        panda = Panda()
        for i in range(1, 10):
            panda.update_hungry(panda.NEGATIVE_UPDATE)
        self.assertEqual(panda.get_feed(), 0.0)

    def test_calculate_happiness(self):
        panda = Panda()
        panda.update_dirty(panda.NEGATIVE_UPDATE)
        self.assertEqual(panda.get_happiness(), 0.9)

    def test_update_ill(self):
        panda = Panda()
        panda.update_ill(panda.NEGATIVE_UPDATE)
        self.assertEqual(panda.get_cure(), 0.5)

    def test_update_sleepy(self):
        panda = Panda()
        panda.update_sleepy(panda.NEGATIVE_UPDATE)
        panda.update_sleepy(panda.NEGATIVE_UPDATE)
        self.assertEqual(panda.get_sleep(), 0.5)

    def test_update_dirty(self):
        panda = Panda()
        panda.update_dirty(panda.NEGATIVE_UPDATE)
        panda.update_dirty(panda.NEGATIVE_UPDATE)
        self.assertEqual(panda.get_clean(), 0.0)

    def test_kill(self):
        panda = Panda()
        panda.kill()
        self.assertFalse(panda.get_alive())

    def test_dead_state(self):
        panda = Panda()
        panda.kill()
        self.assertEqual(panda._state, panda.STATE_DEAD)

    def test_healing_state(self):
        panda = Panda()
        panda.update_ill(panda.NEGATIVE_UPDATE)
        panda.heal()
        self.assertEqual(panda._state, panda.STATE_HEALING)

    def test_playing_state(self):
        panda = Panda()
        panda.update_playful(panda.NEGATIVE_UPDATE)
        panda.play()
        self.assertEqual(panda._state, panda.STATE_PLAYING)

    def test_state_no_change(self):
        panda = Panda()
        panda.eat()
        self.assertNotEqual(panda._state, panda.STATE_EATING)

if __name__ == '__main__':
    unittest.main()
