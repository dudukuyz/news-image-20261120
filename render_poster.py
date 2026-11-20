#!/usr/bin/env python3
"""Render the 20 November 2026 news poster (1024x1024 PNG) with Pillow.

Draws a newspaper front page: masthead + dateline, a lead story on the
Trump-Xi-Putin trilateral in Shenzhen, then Cyclone Akvan, the Kyiv embassy
strikes, the Senegal boat sinking and the APEC summit, plus an "Also today"
strip. All text is drawn from the strings below; nothing is fetched.
Run: python3 render_poster.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (20, 20, 20)
GREY = (38, 38, 38)
RED = (185, 28, 28)
RULE = (185, 178, 160)
BLUE = (29, 78, 137)
LIGHT_BLUE = (207, 227, 242)
GOLD = (242, 183, 5)

FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu"]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise FileNotFoundError(name)


SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s) if os.path.exists(
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf") else font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("NotoSans-Bold.ttf", s) if os.path.exists(
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf") else font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s) if os.path.exists(
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf") else font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.35):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, text):
    f = SANS_B(15)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30  # margin

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(60)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    d.line([(mx, 118), (W - mx, 118)], fill=INK, width=2)
    d.line([(mx, 123), (W - mx, 123)], fill=INK, width=5)
    df = SANS_B(17)
    d.text((mx, 134), "FRIDAY, 20 NOVEMBER 2026", font=df, fill=RED)
    tag = "WORLD NEWS IN ONE IMAGE"
    d.text((W - mx - d.textlength(tag, font=df), 134), tag, font=df, fill=INK)

    # ---- Lead story: Trump-Xi-Putin ----
    y = 168
    y = kicker(d, mx, y, "Shenzhen, China")
    y = para(d, mx, y, "Trump, Xi and Putin meet \u2014 and sign a peace declaration",
             SERIF_B(42), 560, leading=1.12)
    y = para(d, mx, y + 8,
             "The first-ever three-way summit of the American, Chinese and "
             "Russian leaders ends with a joint declaration on nuclear risks, "
             "energy security and ending wars, after talks on the sidelines "
             "of the APEC summit.",
             SANS(18), 560)
    # globe illustration, right of the lead text
    cx, cy, r = 800, 300, 96
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIGHT_BLUE, outline=INK, width=3)
    d.ellipse([cx - r, cy - 38, cx + r, cy + 38], outline=(122, 167, 199), width=2)
    d.ellipse([cx - 38, cy - r, cx + 38, cy + r], outline=(122, 167, 199), width=2)
    d.ellipse([cx - 66, cy - r, cx + 66, cy + r], outline=(122, 167, 199), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(122, 167, 199), width=2)
    # three flags above the globe
    flags = [("USA", (178, 34, 52), (255, 255, 255)),
             ("CHN", (222, 41, 16), (255, 212, 0)),
             ("RUS", (255, 255, 255), (0, 57, 166))]
    fx = [668, 745, 822]
    for (label, bg, fg), x0 in zip(flags, fx):
        d.rectangle([x0, 176, x0 + 52, 210], fill=bg, outline=INK, width=2)
        ff = SANS_B(15)
        d.text((x0 + 26 - d.textlength(label, font=ff) / 2, 185), label, font=ff, fill=fg)
    d.line([(694, 210), (730, 236)], fill=INK, width=2)
    d.line([(771, 210), (771, 236)], fill=INK, width=2)
    d.line([(848, 210), (812, 236)], fill=INK, width=2)
    d.line([(mx, 452), (W - mx, 452)], fill=INK, width=3)

    # ---- Story rows ----
    def story(x, y, width, kick, head, deck, art):
        y2 = kicker(d, x, y, kick)
        y2 = para(d, x, y2, head, SERIF_B(27), width - 132, leading=1.14)
        y2 = para(d, x, y2 + 6, deck, SANS(16), width - 132)
        art(x + width - 118, y + 26)
        return y2

    def art_cyclone(x, y):
        d.ellipse([x, y, x + 118, y + 118], fill=(219, 233, 245), outline=INK, width=3)
        d.arc([x + 12, y + 12, x + 106, y + 106], 200, 60, fill=BLUE, width=8)
        d.arc([x + 26, y + 26, x + 92, y + 92], 20, 240, fill=(58, 123, 213), width=6)
        d.arc([x + 40, y + 40, x + 78, y + 78], 160, 20, fill=(122, 167, 199), width=5)
        d.ellipse([x + 54, y + 54, x + 64, y + 64], fill=RED)

    def art_embassy(x, y):
        d.rectangle([x + 8, y + 52, x + 110, y + 104], fill=(232, 221, 196), outline=INK, width=3)
        d.polygon([(x + 2, y + 52), (x + 59, y + 26), (x + 116, y + 52)], fill=RED, outline=INK)
        for cx0 in (x + 22, x + 53, x + 84):
            d.rectangle([cx0, y + 64, cx0 + 12, y + 104], fill=INK)
        d.rectangle([x + 46, y + 84, x + 72, y + 104], fill=(122, 106, 79), outline=INK, width=2)
        d.line([(x + 14, y + 34), (x + 28, y + 44)], fill=GOLD, width=4)
        d.line([(x + 104, y + 30), (x + 90, y + 44)], fill=GOLD, width=4)

    def art_boat(x, y):
        d.arc([x + 4, y + 76, x + 114, y + 96], 0, 180, fill=BLUE, width=5)
        d.arc([x + 8, y + 94, x + 110, y + 112], 0, 180, fill=(58, 123, 213), width=5)
        d.polygon([(x + 22, y + 74), (x + 96, y + 74), (x + 86, y + 52), (x + 32, y + 52)],
                  fill=(122, 74, 33), outline=INK)
        d.line([(x + 56, y + 52), (x + 56, y + 18)], fill=INK, width=4)
        d.polygon([(x + 60, y + 18), (x + 88, y + 40), (x + 60, y + 40)], fill=RED, outline=INK)

    def art_apec(x, y):
        d.ellipse([x, y, x + 118, y + 118], fill=(227, 239, 224), outline=INK, width=3)
        fl = [("US", (178, 34, 52), (255, 255, 255)),
              ("CN", (222, 41, 16), (255, 212, 0)),
              ("RU", (255, 255, 255), (0, 57, 166))]
        for i, (lb, bg, fg) in enumerate(fl):
            x0 = x + 16 + i * 28
            d.rectangle([x0, y + 28, x0 + 24, y + 46], fill=bg, outline=INK, width=2)
            ff = SANS_B(12)
            d.text((x0 + 12 - d.textlength(lb, font=ff) / 2, y + 31), lb, font=ff, fill=fg)
        d.ellipse([x + 24, y + 78, x + 94, y + 90], fill=(138, 109, 59), outline=INK, width=2)
        d.rectangle([x + 52, y + 68, x + 66, y + 80], fill=(138, 109, 59), outline=INK, width=2)

    row1 = 468
    story(mx, row1, 472, "India", "Cyclone Akvan bears down on India",
          "Severe storm nears the Odisha and Andhra Pradesh coasts; schools "
          "shut and thousands move to safety as landfall nears.", art_cyclone)
    d.line([(512, row1), (512, 676)], fill=RULE, width=1)
    story(542, row1, 452, "Ukraine", "Russian strikes hit embassies in Kyiv",
          "Austrian and Dutch missions damaged in overnight attacks as the "
          "war grinds on into another winter.", art_embassy)
    d.line([(mx, 688), (W - mx, 688)], fill=INK, width=2)

    row2 = 704
    story(mx, row2, 472, "West Africa", "Boat sinks off Senegal \u2014 dozens missing",
          "About 100 migrants were aboard when the vessel went down off the "
          "Senegalese coast; rescuers search for survivors.", art_boat)
    d.line([(512, row2), (512, 912)], fill=RULE, width=1)
    story(542, row2, 452, "Trade", "APEC leaders talk trade in Shenzhen",
          "Xi urges Asia-Pacific economies to keep trade open and work "
          "together on new technology at the leaders\u2019 summit.", art_apec)
    d.line([(mx, 924), (W - mx, 924)], fill=INK, width=2)

    # ---- Also today (two lines; the single-line version ran past the edge) ----
    y = kicker(d, mx, 932, "Also today")
    ticker_lines = [
        [("Van Gogh sells for a record $190.4m", True),
         ("  \u2022  Nicholls hits 113 not out as New Zealand reach 243 for 5 against India", False)],
        [("Anthropic said to be valued at $1.5 trillion", True),
         ("  \u2022  Modi meets the Prince and Princess of Wales in New Delhi", False)],
    ]
    for segments in ticker_lines:
        x = mx
        for text, bold in segments:
            f = SANS_B(16) if bold else SANS(16)
            d.text((x, y), text, font=f, fill=INK)
            x += d.textlength(text, font=f)
        y += 24
    d.line([(mx, 998), (W - mx, 998)], fill=INK, width=2)
    ff = SANS(13)
    d.text((mx, 1006), "20 NOVEMBER 2026", font=ff, fill=(85, 80, 63))
    foot = "MAKE.FUN NEWS-IMAGE \u2022 ALL STORIES AS REPORTED ON 20 NOVEMBER 2026"
    d.text((W - mx - d.textlength(foot, font=ff), 1006), foot, font=ff, fill=(85, 80, 63))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
