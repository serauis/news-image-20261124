#!/usr/bin/env python3
"""Compose the news-image-20261124 front page (1024x1024) from the generated
illustrations and the verified 24-Nov-2026 story list.

Everything on the page is drawn here with PIL + DejaVu fonts; the generated
PNGs carry pictures only, no text. Three layout variants (A/B/C) differ in
which hero leads (column order + width); the winner is picked by hand after
viewing all three and shipped as entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024
MARGIN = 26
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (20, 50, 74)
RED = (158, 28, 28)
GREY = (110, 105, 95)
RULE = (198, 190, 175)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover(img, w, h):
    """Resize-and-centre-crop an image to exactly w x h."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


# --- The verified story list (see SOURCES.md for outlets + dates) --------
HEROES = [
    {
        "kicker": "CHESS  ·  GENEVA",
        "headline": "The youngest title match in history begins",
        "body": ("Gukesh, 20, defends the crown against Sindarov, 20. "
                 "Fourteen games, first to 7.5 points, a $2.5M fund."),
        "meta": "Game 1 today, 15:00 CET  ·  Sindarov has White",
    },
    {
        "kicker": "SKY  ·  WORLDWIDE",
        "headline": "Beaver Supermoon meets the Seven Sisters",
        "body": ("The full Moon peaks at 14:53 UTC, its brightest of the run. "
                 "Before dawn it occults stars of the Pleiades."),
        "meta": "Look up tonight  ·  Moon beside the Pleiades",
    },
    {
        "kicker": "COLOMBIA  ·  TEN YEARS ON",
        "headline": "Ten years after the FARC peace deal",
        "body": ("A decade on, the peace is unfinished. Aid need rose from "
                 "5.8M people in 2016 to 8.1M as violence rebounds."),
        "meta": "Anniversary today  ·  Signed 24 Nov 2016",
    },
]

TILES = [
    ("AUSTRALIA",
     "One Nation's biggest test",
     "Hanson's party polls 21-24% in Victoria ahead of Saturday's state vote; Labor faces a wipeout after 12 years."),
    ("PORTUGAL",
     "Budget vote day in Lisbon",
     "Parliament holds the final vote on the 2027 budget today; the CGTP union rallies outside."),
    ("INDIA - NEPAL",
     "First train reaches Janakpur",
     "The Saryu-Kamala Express arrives about 10:00, a day after Modi and Shah flagged it off in Ayodhya."),
    ("JAPAN",
     "Japan flash PMI out today",
     "S&P Global releases November flash PMIs at 00:30 GMT. October composite was 52.1."),
    ("GERMANY",
     "Germany's Ifo due 09:00 UTC",
     "The business climate index for November. October read 90.2, its best since May 2023."),
    ("UNITED STATES",
     "US consumer confidence due",
     "The Conference Board index lands at 15:00 UTC. Previous reading: 97.1."),
]

ALSO = [
    "US Treasury sells $70bn of 5-year notes today.",
    "Bank of Canada governor Tiff Macklem speaks today.",
    "Volkswagen opens wage talks with IG Metall.",
    "BASF holds its capital markets day.",
    "US ADP weekly employment change due today.",
    "Chicago Fed labour-market indicators due today.",
    "Japan back to work after Labour Thanksgiving Day.",
    "Austria says hackers breached its Foreign Ministry site.",
]

TIMELINE = [
    ("00:30", "Japan flash PMI released"),
    ("09:00", "Germany Ifo business climate"),
    ("~10:00", "Saryu-Kamala train reaches Janakpur"),
    ("14:53", "Supermoon at its fullest"),
    ("15:00", "Chess Game 1 begins; US confidence out"),
]


def build(order, widths, out_path):
    """order: permutation of hero indices left-to-right.
    widths: fractional column widths summing to 1.0."""
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    x0, x1 = MARGIN, W - MARGIN
    inner = x1 - x0

    # ---- Masthead ------------------------------------------------------
    d.text((x0, 18), "THE WORLD TODAY", font=SERIF_B(56), fill=INK)
    d.text((x0, 84), "Tuesday 24 November 2026", font=SANS_B(21), fill=RED)
    right = "17 STORIES  ·  5 REGIONS"
    d.text((x1 - d.textlength(right, font=SANS_B(15)), 90), right,
           font=SANS_B(15), fill=NAVY)
    d.line((x0, 116, x1, 116), fill=INK, width=3)
    d.line((x0, 121, x1, 121), fill=RULE, width=1)

    # ---- Hero triptych --------------------------------------------------
    trip = Image.open(os.path.join(HERE, "hero-triptych.png")).convert("RGB")
    pw = trip.width // 3
    panels = [trip.crop((i * pw, 0, (i + 1) * pw, trip.height))
              for i in range(3)]
    ty, th = 130, 168
    cx = x0
    col_x = []
    for idx, frac in zip(order, widths):
        cw = int(inner * frac)
        col_x.append((cx, cw))
        page.paste(cover(panels[idx], cw - 8, th), (cx + 4, ty))
        d.rectangle((cx + 4, ty, cx + cw - 4, ty + th), outline=INK, width=1)
        cx += cw

    # ---- Hero text ------------------------------------------------------
    hy = ty + th + 10
    for pos, idx in enumerate(order):
        hero = HEROES[idx]
        cx, cw = col_x[pos]
        tx = cx + 6
        tw = cw - 16
        lead = (pos == 0)
        d.text((tx, hy), hero["kicker"], font=SANS_B(11),
               fill=RED if lead else NAVY)
        y = hy + 17
        y = draw_wrapped(d, tx, y,
                         wrap(d, hero["headline"], SANS_B(19 if lead else 17), tw),
                         SANS_B(19 if lead else 17), INK, 22 if lead else 20)
        y += 3
        y = draw_wrapped(d, tx, y,
                         wrap(d, hero["body"], SANS(12), tw),
                         SANS(12), INK, 16)
        y += 3
        y = draw_wrapped(d, tx, y,
                         wrap(d, hero["meta"], SANS_B(11), tw),
                         SANS_B(11), NAVY, 14)

    # ---- Section header -------------------------------------------------
    sy = 452
    d.line((x0, sy, x1, sy), fill=INK, width=2)
    d.text((x0, sy + 8), "AROUND THE WORLD", font=SANS_B(15), fill=INK)
    d.text((x1 - d.textlength("Six more stories, pictured", font=SANS(13)), sy + 9),
           "Six more stories, pictured", font=SANS(13), fill=GREY)

    # ---- Pictured tiles (2 rows x 3) ------------------------------------
    sheet = Image.open(os.path.join(HERE, "tile-sprites.png")).convert("RGB")
    tw_, th_ = sheet.width // 3, sheet.height // 2
    sprites = [sheet.crop(((i % 3) * tw_, (i // 3) * th_,
                           (i % 3 + 1) * tw_, (i // 3 + 1) * th_))
               for i in range(6)]
    tile_w = inner // 3
    tile_h = 118
    ty0 = sy + 34
    for r in range(2):
        for c in range(3):
            i = r * 3 + c
            tx = x0 + c * tile_w
            ty_ = ty0 + r * (tile_h + 8)
            page.paste(cover(sprites[i], 112, 112), (tx + 2, ty_ + 2))
            d.rectangle((tx + 2, ty_ + 2, tx + 114, ty_ + 114),
                        outline=INK, width=1)
            kx, kw = tx + 124, tile_w - 132
            d.text((kx, ty_ + 2), TILES[i][0], font=SANS_B(10), fill=RED)
            y = ty_ + 17
            y = draw_wrapped(d, kx, y,
                             wrap(d, TILES[i][1], SANS_B(13), kw),
                             SANS_B(13), INK, 16)
            y += 2
            draw_wrapped(d, kx, y,
                         wrap(d, TILES[i][2], SANS(11), kw),
                         SANS(11), INK, 14)

    # ---- Also today + stats/timeline ------------------------------------
    ay = ty0 + 2 * (tile_h + 8) + 6
    d.line((x0, ay, x1, ay), fill=INK, width=2)
    d.text((x0, ay + 8), "ALSO TODAY", font=SANS_B(15), fill=INK)
    y = ay + 32
    for item in ALSO:
        d.text((x0, y), "\u2022", font=SANS_B(12), fill=RED)
        y = draw_wrapped(d, x0 + 14, y,
                         wrap(d, item, SANS(12), 590),
                         SANS(12), INK, 16)
        y += 4

    # Right-hand stats box
    bx = x0 + 630
    bw = x1 - bx
    d.rectangle((bx, ay + 8, x1, ay + 92), fill=NAVY)
    d.text((bx + 12, ay + 16), "17 STORIES  ·  5 REGIONS", font=SANS_B(14),
           fill=(255, 255, 255))
    d.text((bx + 12, ay + 38), "Europe  ·  Asia  ·  North America",
           font=SANS(12), fill=(220, 225, 230))
    d.text((bx + 12, ay + 56), "South America  ·  Oceania",
           font=SANS(12), fill=(220, 225, 230))
    d.text((bx + 12, ay + 74), "Drawn pictures: 9  ·  Timeline in UTC",
           font=SANS(11), fill=(200, 210, 220))

    ty2 = ay + 104
    d.text((bx, ty2), "THE DAY IN UTC", font=SANS_B(13), fill=RED)
    y = ty2 + 20
    for t, what in TIMELINE:
        d.text((bx, y), t, font=SANS_B(12), fill=NAVY)
        d.text((bx + 62, y), what, font=SANS(12), fill=INK)
        y += 17

    # ---- Footer: date check ----------------------------------------------
    fy = H - 44
    d.line((x0, fy, x1, fy), fill=INK, width=2)
    foot = ("Every event on this page happened, or was first reported, on "
            "Tuesday 24 November 2026. Events from 23 November or earlier "
            "were excluded.")
    lines = wrap(d, foot, SANS(12), inner)
    y = fy + 8
    for line in lines:
        lw = d.textlength(line, font=SANS(12))
        d.text(((W - lw) / 2, y), line, font=SANS(12), fill=INK)
        y += 15

    page.save(out_path, "PNG", optimize=True)
    print(out_path, page.size, os.path.getsize(out_path))


VARIANTS = {
    "A": ([0, 1, 2], [0.40, 0.30, 0.30]),   # chess-led
    "B": ([1, 0, 2], [0.40, 0.30, 0.30]),   # supermoon-led
    "C": ([2, 0, 1], [0.40, 0.30, 0.30]),   # Colombia-led
}

if __name__ == "__main__":
    for name, (order, widths) in VARIANTS.items():
        build(order, widths, os.path.join(HERE, "variant-%s.png" % name))
