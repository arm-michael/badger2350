import badger2040
import utime
import urandom
import os

# --- Setup ---
display = badger2040.Badger2040()
display.set_font("bitmap8")
display.led(128)

# Buttons
BUTTONS = {
    "A": badger2040.BUTTON_A,
    "B": badger2040.BUTTON_B,
    "C": badger2040.BUTTON_C
}
BUTTON_KEYS = list(BUTTONS.keys())

# Flash file for storing high score
HIGH_SCORE_FILE = "simon_highscore.txt"

# --- Flash storage ---
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# --- Draw text ---
def draw_message(lines):
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    for i, line in enumerate(lines):
        display.text(line, 10, 20 + i * 20, scale=2)
    display.update()

# --- Flash a letter ---
def flash_letter(letter, speed):
    draw_message(["Simon says:", f"{letter}"])
    utime.sleep(speed)
    # No need to clear/update again; just pause briefly before the next step
    utime.sleep(0.2)

# --- Show full sequence ---
def play_sequence(sequence, speed):
    for letter in sequence:
        flash_letter(letter, speed)

# --- Wait for player input ---
def get_player_input():
    while True:
        for letter, pin in BUTTONS.items():
            if display.pressed(pin):
                while display.pressed(pin):
                    pass  # debounce
                return letter
        utime.sleep(0.05)

# --- Game logic ---
def start_game():
    sequence = []
    round_number = 0
    game_over = False
    high_score = load_high_score()

    while not game_over:
        next_letter = urandom.choice(BUTTON_KEYS)
        sequence.append(next_letter)
        round_number += 1

        # Increase difficulty
        speed = max(0.3, 0.7 - (round_number // 3) * 0.1)

        draw_message([f"Round {round_number}"])
        utime.sleep(1)

        play_sequence(sequence, speed)

        for expected in sequence:
            player = get_player_input()
            flash_letter(player, 0.2)
            if player != expected:
                game_over = True
                break

    # Save high score
    if round_number - 1 > high_score:
        save_high_score(round_number - 1)
        new_best = True
    else:
        new_best = False

    draw_message([
        "❌ Wrong!",
        f"Score: {round_number - 1}",
        f"Best: {max(high_score, round_number - 1)}",
        "🎉 New High!" if new_best else "",
        "Press A to restart"
    ])

# --- Start ---
draw_message(["Badge Simon", "Press A to start"])

while True:
    if display.pressed(badger2040.BUTTON_A):
        start_game()
        draw_message(["Badge Simon", "Press A to start"])
    utime.sleep(0.1)
