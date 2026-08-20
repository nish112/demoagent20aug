"""Shooting reflexes game.

A small tkinter game that measures how fast the player reacts to a target
appearing on screen.

Rules:
    1. The player enters a name.
    2. A shooter is drawn at the bottom middle of the screen.
    3. A target appears at a random position after a random delay.
    4. The player presses the space bar to shoot.
    5. The reaction time between target appearance and the space bar press
       is measured.
    6. A reaction time under 0.3 seconds means the player wins, otherwise the
       computer wins.
"""

import random
import sys
import time
import tkinter as tk

WIDTH = 800
HEIGHT = 600
WIN_THRESHOLD = 0.3
MIN_DELAY_MS = 1000
MAX_DELAY_MS = 4000
TARGET_RADIUS = 25


class ShootingReflexesGame:
    """Tkinter application implementing the reflex shooting game."""

    def __init__(self, root):
        self.root = root
        self.root.title("Shooting Reflexes")
        self.player_name = ""
        self.target_id = None
        self.target_shown_at = None
        self.pending_target = None
        self.round_active = False
        self.wins = 0
        self.losses = 0

        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT, bg="#101820", highlightthickness=0
        )
        self.canvas.pack()

        self.root.bind("<space>", self.on_shoot)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.ask_player_name()

    # -- setup -------------------------------------------------------------
    def ask_player_name(self):
        """Show the name entry screen."""
        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 80,
            text="SHOOTING REFLEXES",
            fill="#f2f2f2",
            font=("Helvetica", 32, "bold"),
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 20,
            text="Enter your name and press Start",
            fill="#9fb4c7",
            font=("Helvetica", 16),
        )

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 16), justify="center")
        self.canvas.create_window(WIDTH // 2, HEIGHT // 2 + 30, window=self.name_entry)
        self.name_entry.focus_set()
        self.name_entry.bind("<Return>", lambda event: self.start_game())

        self.start_button = tk.Button(
            self.root, text="Start", font=("Helvetica", 14), command=self.start_game
        )
        self.canvas.create_window(WIDTH // 2, HEIGHT // 2 + 80, window=self.start_button)

    def start_game(self):
        """Validate the name and start the first round."""
        name = self.name_entry.get().strip()
        if not name:
            name = "Player"
        self.player_name = name
        self.name_entry.destroy()
        self.start_button.destroy()
        self.next_round()

    # -- round handling ----------------------------------------------------
    def next_round(self):
        """Draw the arena and schedule the next target."""
        self.cancel_pending_target()
        self.round_active = True
        self.target_id = None
        self.target_shown_at = None

        self.draw_scene("Get ready... press SPACE when the target appears")
        delay = random.randint(MIN_DELAY_MS, MAX_DELAY_MS)
        self.pending_target = self.root.after(delay, self.show_target)

    def draw_scene(self, message, message_color="#9fb4c7"):
        """Redraw the background, shooter and status text."""
        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH // 2,
            40,
            text=f"{self.player_name}   |   You {self.wins} - {self.losses} Computer",
            fill="#f2f2f2",
            font=("Helvetica", 16, "bold"),
        )
        self.canvas.create_text(
            WIDTH // 2, 80, text=message, fill=message_color, font=("Helvetica", 14)
        )
        self.draw_shooter()

    def draw_shooter(self):
        """Draw the shooter at the bottom middle of the screen."""
        base_x = WIDTH // 2
        base_y = HEIGHT - 40
        self.canvas.create_rectangle(
            base_x - 30, base_y, base_x + 30, base_y + 20, fill="#3d5a80", outline=""
        )
        self.canvas.create_oval(
            base_x - 18, base_y - 45, base_x + 18, base_y - 9, fill="#98c1d9", outline=""
        )
        self.canvas.create_rectangle(
            base_x - 4, base_y - 110, base_x + 4, base_y - 40, fill="#ee6c4d", outline=""
        )

    def show_target(self):
        """Place a target at a random position and start the timer."""
        self.pending_target = None
        x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
        y = random.randint(TARGET_RADIUS + 100, HEIGHT - 180)
        self.target_id = self.canvas.create_oval(
            x - TARGET_RADIUS,
            y - TARGET_RADIUS,
            x + TARGET_RADIUS,
            y + TARGET_RADIUS,
            fill="#e63946",
            outline="#f1faee",
            width=3,
        )
        self.target_shown_at = time.perf_counter()

    def cancel_pending_target(self):
        """Cancel a scheduled target, if any."""
        if self.pending_target is not None:
            self.root.after_cancel(self.pending_target)
            self.pending_target = None

    # -- input -------------------------------------------------------------
    def on_shoot(self, event=None):
        """Handle the space bar press."""
        if not self.round_active:
            self.next_round()
            return

        if self.target_shown_at is None:
            # Fired before the target appeared.
            self.cancel_pending_target()
            self.round_active = False
            self.end_round(
                won=False, message="Too early! You shot before the target appeared."
            )
            return

        reaction = time.perf_counter() - self.target_shown_at
        self.round_active = False
        won = reaction < WIN_THRESHOLD
        self.end_round(won=won, message=f"Reaction time: {reaction:.3f} s")

    def end_round(self, won, message):
        """Show the round result and wait for the player to continue."""
        if won:
            self.wins += 1
            result = "YOU WIN"
            color = "#8ac926"
        else:
            self.losses += 1
            result = "YOU LOOSE"
            color = "#e63946"

        self.draw_scene(message, message_color="#f2f2f2")
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text=result,
            fill=color,
            font=("Helvetica", 48, "bold"),
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 60,
            text="Press SPACE to play again (ESC to quit)",
            fill="#9fb4c7",
            font=("Helvetica", 14),
        )


def main():
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print(f"Unable to start the game: no display available ({exc}).", file=sys.stderr)
        return 1
    ShootingReflexesGame(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
