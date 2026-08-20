# demoagent20aug

## Shooting Reflexes

A small Python game that tests your shooting reflexes.

### How to play

```bash
python shooting_reflexes.py
```

1. Enter your player name and press **Start** (or Enter).
2. A shooter is drawn at the bottom middle of the screen.
3. After a short random delay a target appears somewhere on screen.
4. Press the **space bar** to shoot as fast as you can.
5. If your reaction time is under **0.3 seconds** you win, otherwise the computer wins.
6. The result is shown as "YOU WIN" or "YOU LOOSE"; press **space** to play another
   round or **Esc** to quit.

Shooting before the target appears counts as a loss.

### Requirements

- Python 3 with `tkinter` (standard library). On Debian/Ubuntu install it with
  `sudo apt-get install python3-tk` if it is missing.
