# Micro:bit emulator
A simple emulator for microbit.py for assistance with development of micropython for the bbc micro:bit
### Usage:


simple micro:bit program that displays a happy/sad face when a button is pressed
```py
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
```

### notes:
`display.show()` does not accept strings as there is no table of stings yet :)
