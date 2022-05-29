import threading as _threading
import time as _time

_time_start = _time.time()
_config = {}
_letters = {
    ""
}


def emulator_config(*, temp=21.0, light_level=255):
    global _config

    _config["temp"] = temp
    _config["light_level"] = light_level


class display:
    _board = [
        [
            0 for _ in range(5)
        ] for _ in range(5)
    ]

    @staticmethod
    def get_pixel(x, y):
        """
        Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright).
        """
        return display._board[x][y]

    @staticmethod
    def set_pixel(x, y, value):
        """
        Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9.
        """
        if not (0 <= x < 5 and 0 <= y < 5 and 0 <= value < 10):
            raise Exception()

        display._board[x][y] = value

    @staticmethod
    def clear():
        """
        Set the brightness of all LEDs to 0 (off).
        """
        display._board = [
            [
                0 for _ in range(5)
            ] for _ in range(5)
        ]

    @staticmethod
    def show(image, delay=400, *, clear=False):
        """
        If image is a string, float or integer, display letters/digits in sequence. Otherwise, if image is an iterable
        sequence of images, display these images in sequence. Each letter, digit or image is shown with delay
        milliseconds between them.
        """

        if type(image) == list and len(image) == 5 and len(image[0]) == 5:
            for _x in range(5):
                for _y in range(5):
                    display.set_pixel(_x, _y, image[_y][_x])
            return

        if type(image) == str:
            for letter in image:
                ...

        sleep(delay)

        if clear:
            display.clear()

    @staticmethod
    def scroll(text):
        raise NotImplemented

    # on and off are for use with GPIO relocation, as GPIO is not implemented functions are redundant
    @staticmethod
    def on():
        ...

    @staticmethod
    def off():
        ...

    @staticmethod
    def is_on():
        return True

    @staticmethod
    def read_light_level():
        """
        Use the display’s LEDs in reverse-bias mode to sense the amount of light falling on the display.
        Returns an integer between 0 and 255 representing the light level, with larger meaning more light.
        """
        return _config["light_level"]


def sleep(n):
    """
    Wait for n milliseconds. One second is 1000 milliseconds, so:

        microbit.sleep(1000)

    will pause the execution for one second. n can be an integer or a floating point number.
    """
    _time.sleep(n / 1000)


def running_time():
    """
    Return the number of milliseconds since the board was switched on or restarted.
    """
    return _time.time() - _time_start


def temperature():
    """
    Return the temperature of the micro:bit in degrees Celcius.
    """
    return _config["temp"]


class _button:
    def __init__(self):
        self._is_pressed = False
        self._was_pressed = False
        self._presses = 0

    def _press(self):
        self._is_pressed = True
        self._was_pressed = True
        self._presses += 1

    def _un_press(self):
        self._is_pressed = False

    def is_pressed(self):
        return self._is_pressed

    def was_pressed(self):
        if self._was_pressed:
            self._was_pressed = False
            return True

        return False

    def get_presses(self):
        a = self._presses
        self._presses = 0
        return a


button_a = _button()
button_b = _button()


def _run_screen():
    print("[E] started screen process")

    import random as _random
    import pygame as _pygame

    _pygame.init()
    _pygame.font.init()

    _display = _pygame.display.set_mode((150 + 16 + 16, 106 + 16 + 16 + 16 + 16))
    _clock = _pygame.time.Clock()
    _font = _pygame.font.SysFont(_pygame.font.get_default_font(), 12)
    _running = True

    _tri_c = [(0, 124, 113), (130, 106, 0), (0, 80, 163), (149, 15, 66)][_random.randint(0, 3)]

    while _running:
        for _e in _pygame.event.get():
            if _e.type == _pygame.QUIT:
                _running = False

            elif _e.type == _pygame.MOUSEBUTTONDOWN:
                if ((32 - _e.pos[0]) ** 2 + (79 - _e.pos[1]) ** 2) ** 0.5 < 8:
                    button_a._press()

                elif ((150 - _e.pos[0]) ** 2 + (79 - _e.pos[1]) ** 2) ** 0.5 < 8:
                    button_b._press()

            elif _e.type == _pygame.MOUSEBUTTONUP:
                button_a._un_press()
                button_b._un_press()

        _display.fill((0, 0, 0))

        # to many numbers
        _pygame.draw.rect(_display, (24, 24, 24), (16, 16, 150, 106 + 16 + 16), border_radius=4)
        _pygame.draw.polygon(_display, _tri_c, ((16 + 8, 16), (16 + 8, 16 + 8), (16, 16 + 8), (16, 16 + 24), (16 + 24, 16),
                                                (16 + 24, 16 + 18), (16 + 24 + 18, 16), (16 + 24 + 18, 16 + 12),
                                                (16 + 24 + 18 + 12, 16)))
        # maintain curve on polygon
        _pygame.draw.rect(_display, _tri_c, (16, 16, 12, 12), border_radius=4)
        _pygame.draw.rect(_display, (139, 140, 134), (24, 55 + 16, 16, 16), border_radius=2)
        _pygame.draw.circle(_display, (69, 70, 69), (32, 63 + 16), 6)
        _pygame.draw.polygon(_display, _tri_c, ((32, 75 + 16), (32, 87 + 16), (20, 87 + 16)))
        _display.blit(_font.render("A", True, (24, 24, 24)), (26, 80 + 16))
        _pygame.draw.rect(_display, (139, 140, 134), (141, 55 + 16, 16, 16), border_radius=2)
        # okay there's got to be a better way of doing this
        _pygame.draw.circle(_display, (69, 70, 69), (149, 63 + 16), 6)
        _pygame.draw.polygon(_display, _tri_c, ((149, 51 + 16), (149, 39 + 16), (161, 39 + 16)))
        _display.blit(_font.render("B", True, (24, 24, 24)), (150, 39 + 16))
        _pygame.draw.rect(_display, (246, 212, 111), (9 + 16 - 4, 138 + 8, 2, 8))
        _pygame.draw.rect(_display, (246, 212, 111), (9 + 16 - 4 + 138, 138 + 8, 2, 8))
        for _a in range(5):
            _pygame.draw.rect(_display, (246, 212, 111), (9 + _a * 30 + 16, 138, 12, 16))
            _pygame.draw.circle(_display, (24, 24, 24), (9 + 4 + _a * 30 + 18, 138), 6)
            _pygame.draw.circle(_display, (246, 212, 111), (9 + 4 + _a * 30 + 18, 138), 6, 2)
            for _b in range(5):
                if _a != 4:  # witchcraft follows
                    _pygame.draw.rect(_display, (246, 212, 111), (9 + _a * 30 + 16 + _b * 3 + 14, 138 + 8, 2, 8))
                _pygame.draw.rect(_display, (187, 186, 181), (32 + 25 + _a * 16, 8 + 25 + _b * 16 + 16, 3, 2))
                _pygame.draw.rect(_display, [(151, 151, 151), (28 * display.get_pixel(_a, _b), 0, 0)][1], (32 + 24 + _a * 16, 8 + 27 + _b * 16 + 16, 5, 5))
                _pygame.draw.rect(_display, (80, 80, 79), (32 + 25 + _a * 16, 8 + 32 + _b * 16 + 16, 3, 2))

        _pygame.display.update()
        _clock.tick(65)


if __name__ == '__main__':
    print("must be imported as module.")
else:
    print("microbit emulator v0")
    _threading.Thread(target=_run_screen).start()
    _time.sleep(2)
