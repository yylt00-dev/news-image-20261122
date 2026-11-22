#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026 and save entry.png.

Fresh drawing made for this competition only: Pillow, no network, no
external assets. Layout: navy masthead, one lead story (Peru quake) with a
hand-drawn Andes panel, four story cards in a 2x2 grid, and an "also today"
ticker strip along the bottom.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 24, 22)
NAVY = (18, 38, 66)
NAVY2 = (28, 56, 92)
RED = (176, 32, 32)
GOLD = (184, 124, 26)
TEAL = (18, 110, 105)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (96, 94, 88)
LINE = (200, 192, 172)
SKY = (146, 178, 205)
MT_FAR = (96, 118, 148)
MT_NEAR = (58, 74, 96)
SNOW = (238, 240, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif(size):
    return load("DejaVuSerif-Bold.ttf", size)


def serif_reg(size):
    return load("DejaVuSerif.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def split_lines(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(draw, x, y, text, font, max_w, fill, leading=None):
    step = leading or int(font.size * 1.3)
    for line in split_lines(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def centre(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.25)


def draw_andes(draw, x0, y0, x1, y1):
    """Andes ridge under a pale sky, with red seismic rings above the peak."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun
    draw.ellipse([x1 - 92, y0 + 26, x1 - 36, y0 + 82], fill=(246, 214, 130))
    # far ridge
    far = [(x0, y1), (x0 + 40, y0 + 118), (x0 + 130, y0 + 168),
           (x0 + 210, y0 + 96), (x0 + 300, y0 + 160), (x0 + 380, y0 + 120),
           (x0 + 460, y0 + 176), (x1, y0 + 138), (x1, y1)]
    draw.polygon(far, fill=MT_FAR)
    # snow caps on the far ridge
    for px, py, s in [(x0 + 210, y0 + 96, 26), (x0 + 380, y0 + 120, 20)]:
        draw.polygon([(px - s, py + 16), (px, py), (px + s, py + 16)],
                     fill=SNOW)
    # near ridge
    near = [(x0, y1), (x0 + 70, y0 + 190), (x0 + 190, y0 + 130),
            (x0 + 300, y0 + 200), (x0 + 420, y0 + 148), (x1, y0 + 196),
            (x1, y1)]
    draw.polygon(near, fill=MT_NEAR)
    draw.polygon([(x0 + 190 - 24, y0 + 146), (x0 + 190, y0 + 130),
                  (x0 + 190 + 24, y0 + 146)], fill=SNOW)
    # valley floor with a small village
    draw.rectangle([x0, y1 - 46, x1, y1], fill=(88, 96, 66))
    for hx in range(x0 + 26, x1 - 40, 58):
        draw.rectangle([hx, y1 - 78, hx + 34, y1 - 46], fill=(232, 222, 196))
        draw.polygon([(hx - 3, y1 - 78), (hx + 17, y1 - 94),
                      (hx + 37, y1 - 78)], fill=(150, 52, 40))
    # crack lines in the ground
    for (ax, ay, bx, by) in [(x0 + 90, y1 - 46, x0 + 130, y1 - 18),
                             (x0 + 300, y1 - 46, x0 + 280, y1 - 12),
                             (x0 + 420, y1 - 46, x0 + 452, y1 - 20)]:
        draw.line([(ax, ay), (bx, by)], fill=(40, 40, 36), width=3)
    # seismic rings over the tallest peak
    cx, cy = x0 + 210, y0 + 96
    for r, wdt in [(26, 5), (48, 4), (72, 3), (98, 2)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=(176, 32, 32), width=wdt)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(176, 32, 32))


def icon_globe(draw, cx, cy, r, colour):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=colour, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=colour, width=3)


def icon_drop(draw, cx, cy, r, colour):
    draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r], fill=colour)
    draw.polygon([(cx - r, cy - r // 2), (cx, cy - r - 8),
                  (cx + r, cy - r // 2)], fill=colour)
    draw.line([(cx - r // 2, cy + r // 4), (cx + r // 2, cy + r // 4)],
              fill=WHITE, width=4)


def icon_flag(draw, cx, cy, r, colour):
    draw.line([(cx - r // 2, cy - r), (cx - r // 2, cy + r)],
              fill=colour, width=4)
    draw.polygon([(cx - r // 2, cy - r), (cx + r, cy - r // 2),
                  (cx - r // 2, cy)], fill=colour)


def icon_pin(draw, cx, cy, r, colour):
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r // 4],
                 outline=colour, width=4)
    draw.ellipse([cx - 5, cy - r + 9, cx + 5, cy - r + 19], fill=colour)
    draw.polygon([(cx - 7, cy + r // 4), (cx + 7, cy + r // 4),
                  (cx, cy + r)], fill=colour)


CARDS = [
    ("GENEVA  ·  ARMS", "Robot-weapons talks end without rules",
     "UN talks on lethal autonomous weapons fall short of enforceable "
     "guidelines.", NAVY2, icon_globe),
    ("OSLO  ·  CLIMATE", "Top court voids disputed oil licences",
     "Norway's supreme court rules climate-challenged oil licences "
     "invalid.", TEAL, icon_drop),
    ("MOGADISHU  ·  CONFLICT", "Al-Shabaab claims deadly ambush",
     "Militants say hundreds of Somali troops were killed; the toll is "
     "unverified.", RED, icon_flag),
    ("BLUE NILE  ·  SUDAN", "Rebels seize the key Bau region",
     "Sudan's Tasis Alliance takes the Blue Nile's Bau region as "
     "fighting spreads.", GOLD, icon_pin),
]

TICKER = ("EU and Indonesia sign a landmark trade deal  •  France holds a "
          "fourth weekend of cost-of-living protests  •  Four nations urge "
          "aid access to flooded Gaza  •  Eisenkot tapped to form Israel's "
          "next government  •  Alcaraz faces Zverev for the ATP Finals "
          "title  •  Ghana unveils Heritage Series banknotes")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 128], fill=NAVY)
    centre(d, W // 2, 16, "THE WORLD IN ONE PAGE", serif(56), WHITE)
    centre(d, W // 2, 84, "SUNDAY, 22 NOVEMBER 2026  ·  THE DAY'S NEWS IN A SINGLE IMAGE",
           sans_b(19), (200, 208, 220))
    d.rectangle([0, 128, W, 136], fill=RED)

    # ---- lead story ----
    y = 156
    d.text((28, y), "EARTHQUAKE  ·  PERU", font=sans_b(21), fill=RED)
    y += 34
    d.text((28, y), "THE ANDES", font=serif(66), fill=INK)
    y += 72
    d.text((28, y), "SHAKE", font=serif(66), fill=INK)
    y += 82
    y = paragraph(d, 28, y,
                  "A strong earthquake struck Peru's Andean highlands on "
                  "Sunday. No damage or casualties were reported.",
                  serif_reg(25), 440, INK)
    draw_andes(d, 500, 156, 996, 470)
    d.rectangle([500, 156, 996, 470], outline=INK, width=2)
    d.text((512, 478), "The Andes, Peru — seismic waves over the high peaks.",
           font=sans(16), fill=GREY)

    # ---- story cards, 2 x 2 ----
    top, card_h, gap = 516, 168, 16
    card_w = (W - 56 - gap) // 2
    for i, (kicker, head, body, colour, icon) in enumerate(CARDS):
        x0 = 28 + (i % 2) * (card_w + gap)
        y0 = top + (i // 2) * (card_h + gap)
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=CARD,
                    outline=LINE, width=2)
        d.rectangle([x0, y0, x0 + card_w, y0 + 8], fill=colour)
        d.text((x0 + 16, y0 + 20), kicker, font=sans_b(16), fill=colour)
        head_lines = split_lines(d, head, serif(25), card_w - 108)
        hy = y0 + 48
        for line in head_lines[:2]:
            d.text((x0 + 16, hy), line, font=serif(25), fill=INK)
            hy += 32
        # body sits under the headline block, at most two lines
        by = hy + 6
        for line in split_lines(d, body, sans(17), card_w - 32)[:2]:
            d.text((x0 + 16, by), line, font=sans(17), fill=GREY)
            by += 21
        icon(d, x0 + card_w - 42, y0 + 62, 22, colour)

    # ---- ticker ----
    ty = 884
    d.rectangle([0, ty, W, ty + 104], fill=NAVY)
    d.text((28, ty + 8), "ALSO TODAY", font=sans_b(18), fill=(246, 214, 130))
    paragraph(d, 28, ty + 34, TICKER, sans(17), W - 56, WHITE, leading=22)

    # ---- footer ----
    centre(d, W // 2, 996, "22 NOVEMBER 2026 — one day, one image",
           sans(15), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    build()
