import badger2040
import jpegdec
import pngdec
import qrcode
import utime

# --- Setup ---
display = badger2040.Badger2040()
display.led(128)
jpeg = jpegdec.JPEG(display.display)
png = pngdec.PNG(display.display)

# --- Content ---
name = "Michael Gamble"
title = "Partner Marketing"
co = "arm.com"
github = "@arm-michael"
li = ".../in/michaelgamble"
mail = "michael.gamble@arm.com"
qr_url = "https://github.com/arm-michael"

fun_facts = [
    "Works with creators",
    "Loves hardware + AI",
    "Total cat fan"
]

FONT_SIZE = 2
LINE_SPACING = 20

# --- QR Code Drawing ---
def draw_qr(url, x_offset, y_offset, scale):
    qr = qrcode.QRCode()
    qr.set_text(url)

    try:
        modules = qr.get_module_matrix()
    except AttributeError:
        display.set_pen(0)
        display.text("QR Error!", 10, 10, scale=1)
        return

    size = len(modules)

    for row in range(size):
        for col in range(size):
            if modules[row][col]:
                display.set_pen(0)  # Black
            else:
                display.set_pen(15)  # White
            display.rectangle(x_offset + col * scale, y_offset + row * scale, scale, scale)

# --- Screens ---
def show_main():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.text("Name: " + name, 10, 20, scale=FONT_SIZE)
    display.text("Title: " + title, 10, 40, scale=FONT_SIZE)
    display.text("Co: " + co, 10, 60, scale=FONT_SIZE)
    draw_qr(qr_url, 160, 10, 3)
    display.update()

def show_contact():
    display.set_pen(0)
    display.clear()
    display.set_pen(15)
    display.text("e: " + mail, 10, 20, scale=FONT_SIZE)
    display.text("gh: " + github, 10, 40, scale=FONT_SIZE)
    display.text("LinkedIn: " + li, 10, 60, scale=FONT_SIZE)
    display.update()

def show_facts():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.text("Fun Facts:", 10, 10, scale=FONT_SIZE)
    for i, fact in enumerate(fun_facts):
        display.text(f"- " + fact, 10, 30 + i * LINE_SPACING, scale=FONT_SIZE)
    display.update()

def show_cat(blink=False):
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    face = "( o.o )" if not blink else "( -.- )"

    display.text(" /\\_/\\ ", 10, 20, scale=FONT_SIZE)
    display.text(face,     10, 40, scale=FONT_SIZE)
    display.text(" > ^ < ", 10, 60, scale=FONT_SIZE)

    display.update()

def show_png():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    try:
        png.open_file("badge2.png")
        png.decode(0, 0)
    except OSError:
        display.text("Missing: badge2.png", 10, 10, scale=1)

    display.update()

# --- Section Management ---
screens = [show_main, show_contact, show_facts, show_cat, show_png]
screen_index = 0

# --- Show initial screen ---
screens[screen_index]()

# --- Main Loop ---
while True:
    if display.pressed(badger2040.BUTTON_UP):
        screen_index = (screen_index - 1) % len(screens)
        screens[screen_index]()
        utime.sleep(0.5)

    elif display.pressed(badger2040.BUTTON_DOWN):
        screen_index = (screen_index + 1) % len(screens)
        screens[screen_index]()
        utime.sleep(0.5)