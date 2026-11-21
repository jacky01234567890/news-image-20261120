#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 as a 1024x1024 PNG.

A newspaper front page: eyebrow line, WORLD NEWS masthead, the date in red,
the lead story on Russia's November strike on Ukraine, two rows of two
stories (Wall Street, the White House, Cyclone Akvan, the Peru earthquake),
an ALSO TODAY briefs list, and a footer. Everything is laid out top to
bottom with a running cursor, so no block can overlap the next one.

Deterministic: no randomness, no clock, no network. Two runs write the
same bytes. Run from anywhere; the image is written next to this script's
parent directory as entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS_PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")

W, H = 1024, 1024
INK = (0, 0, 0)
RED = (198, 32, 32)
GREY = (115, 115, 115)
PAPER = (255, 255, 255)

LEFT = 44
RIGHT = 980
MID = 512
GUTTER = 24
COL = (RIGHT - LEFT - GUTTER) // 2  # width of one story column


def face(path, size):
    """A TrueType font at the given size."""
    return ImageFont.truetype(path, size)


def shrink_to_fit(text, path, width, size):
    """The largest size at or below `size` for which `text` fits `width`."""
    f = face(path, size)
    while f.getlength(text) > width and size > 8:
        size -= 2
        f = face(path, size)
    return f


def wrap_lines(draw, text, font, width):
    """Split `text` into lines that fit `width`, breaking on spaces."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def block(draw, x, y, text, font, width, leading, fill=INK):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for line in wrap_lines(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def bar(draw, y, weight, fill=INK, x0=LEFT, x1=RIGHT):
    """A horizontal rule; return the y just below it."""
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)
    return y + weight


def kicker(draw, x, y, text):
    """A small red section label; return the y below it."""
    return block(draw, x, y, text, face(SANS, 19), COL, 24, fill=RED)


def story(draw, x, y, label, headline, body):
    """One grid story: kicker, headline, body. Return the y below it."""
    y = kicker(draw, x, y, label)
    y = block(draw, x, y + 2, headline, face(SANS, 24), COL, 30)
    y = block(draw, x, y + 4, body, face(SANS_PLAIN, 19), COL, 24)
    return y


def brief(draw, x, y, lead, rest):
    """One ALSO TODAY line: bold lead, then the plain remainder."""
    bold = face(SANS, 20)
    plain = face(SANS_PLAIN, 20)
    draw.text((x, y), lead, font=bold, fill=INK)
    draw.text((x + draw.textlength(lead, font=bold), y), rest, font=plain, fill=INK)
    return y + 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer border.
    draw.rectangle([28, 28, 996, 996], outline=INK, width=3)

    y = 40
    # Eyebrow: the paper's line on the left, the weekday on the right.
    draw.text((LEFT, y), "THE WORLD IN ONE IMAGE", font=face(SANS, 20), fill=INK)
    day = "FRIDAY"
    draw.text((RIGHT - draw.textlength(day, font=face(SANS, 20)), y),
              day, font=face(SANS, 20), fill=RED)
    y += 26

    # Masthead, as large as fits the page width; advance by its ink height.
    mast = shrink_to_fit("WORLD NEWS", SERIF, RIGHT - LEFT, 102)
    draw.text((LEFT, y), "WORLD NEWS", font=mast, fill=INK)
    y = draw.textbbox((LEFT, y), "WORLD NEWS", font=mast)[3] + 12

    y = bar(draw, y, 5, fill=RED) + 8

    # The date, prominent in red.
    draw.text((LEFT, y), "Friday, 20 November 2026",
              font=face(SERIF, 33), fill=RED)
    y += 40

    y = bar(draw, y, 3) + 8

    # Lead story: Russia's biggest strike of November.
    y = block(draw, LEFT, y, "UKRAINE WAR  \u00b7  KYIV AND POLAND",
              face(SANS, 20), RIGHT - LEFT, 25, fill=RED)
    y = block(draw, LEFT, y + 4,
              "Russia launches its biggest strike of November; "
              "missiles fall in Poland",
              face(SANS, 40), RIGHT - LEFT, 46)
    y = block(draw, LEFT, y + 6,
              "More than 400 drones and 110 missiles hit Ukraine overnight, "
              "striking three Kyiv bridges and killing at least eight. "
              "Two missiles and a drone fall in Poland.",
              face(SANS_PLAIN, 21), RIGHT - LEFT, 28)
    y = bar(draw, y + 10, 3) + 10

    # Two rows of two stories, with a vertical divider between columns.
    top = y
    left_y = story(draw, LEFT, y, "WALL STREET",
                   "AI sell-off drags S&P 500 and Dow into correction",
                   "The S&P 500 falls 3.7% and the Nasdaq 5.3% in the worst "
                   "week since 2020; Nvidia drops 14% as its chief is ousted.")
    right_y = story(draw, MID + GUTTER // 2, y, "WHITE HOUSE",
                    "Trump: Putin wants the Ukraine war to end by diplomacy",
                    "In a 90-minute news conference, Trump defends his summit "
                    "ties and vows Iran will never get a nuclear weapon.")
    row_end = max(left_y, right_y)
    draw.line([MID, top, MID, row_end], fill=GREY, width=1)

    top = row_end + 8
    left_y = story(draw, LEFT, top, "CYCLONE AKVAN",
                   "Cyclone Akvan hits Odisha after 370,000 evacuated",
                   "The storm makes landfall near Gopalpur with winds to "
                   "90 kmph; no major damage or loss of life is reported.")
    right_y = story(draw, MID + GUTTER // 2, top, "PERU",
                    "Magnitude 6.7 earthquake shakes central Peru",
                    "The tremor, centred near Jun\u00edn, is felt in Lima; no "
                    "casualties or serious damage are reported.")
    row_end = max(left_y, right_y)
    draw.line([MID, top, MID, row_end], fill=GREY, width=1)

    y = bar(draw, row_end + 10, 3) + 8

    # Also today: five briefs.
    draw.text((LEFT, y), "ALSO TODAY", font=face(SANS, 20), fill=INK)
    y += 24
    for lead, rest in [
        ("COP31 climate talks stall", " as the draft drops fossil fuels."),
        ("Hungary lifts its veto", " on Ukraine\u2019s EU accession talks."),
        ("Ukraine says it retook 14 settlements", " in Kharkiv region."),
        ("EU sends Ukraine nearly \u20ac8 billion,", " its largest payout yet."),
        ("US and China agree humans must oversee",
         " military AI decisions."),
    ]:
        y = brief(draw, LEFT, y, lead, rest)

    y = bar(draw, y + 6, 2, fill=GREY) + 8
    draw.text((LEFT, y),
              "All events happened or were first reported on "
              "Friday 20 November 2026.",
              font=face(SANS_PLAIN, 16), fill=GREY)

    img.save(TARGET, "PNG")


if __name__ == "__main__":
    main()
