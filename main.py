from microbit import *

smile = [
    [0, 0, 0, 0, 0],
    [0, 9, 0, 9, 0],
    [0, 0, 0, 0, 0],
    [9, 0, 0, 0, 9],
    [0, 9, 9, 9, 0],
]

sad = [
    [0, 0, 0, 0, 0],
    [0, 9, 0, 9, 0],
    [0, 0, 0, 0, 0],
    [0, 9, 9, 9, 0],
    [9, 0, 0, 0, 9],
]

while True:
    if button_a.is_pressed():
        display.show(smile)

    else:
        display.show(sad)

    sleep(1)
