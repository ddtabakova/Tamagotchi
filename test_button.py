import unittest

from button import Button


class ButtonTest(unittest.TestCase):

    def test_is_pressed_yes(self):
        button = Button(0, 0, 40, 40, "images/button-0.png", None)
        self.assertTrue(button.pressed((20, 20)))

    def test_is_pressed_no(self):
        button = Button(0, 0, 40, 40, "images/button-0.png", None)
        self.assertFalse(button.pressed((200, 200)))

if __name__ == '__main__':
    unittest.main()
