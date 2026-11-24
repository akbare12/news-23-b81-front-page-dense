#!/usr/bin/env python3
"""news-23 b81 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024, PIL. Run: python3 draw.py  -> entry.png next to this file."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)
GOLD_L = (232, 196, 90)
RED = (178, 34, 34)
RED_L = (214, 48, 49)
BLUE = (31, 58, 147)
BLUE_L = (46, 92, 178)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
PURPLE = (106, 27, 154)
GRAY = (90, 90, 90)
CREAM = (250, 246, 232)
NAVY = (13, 27, 62)
INK = (20, 20, 20)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def wrap(s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def chip(x, y, label, kind):
    """Small REPORTED (blue) / CLAIM (red) chip; returns width."""
    font = f(SANS_B, 9)
    w_ = int(d.textlength(label, font=font)) + 10
    col = BLUE if kind == "REPORTED" else RED
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=3, fill=col)
    d.text((x + 5, y + 2), label, font=font, fill=WHITE)
    return w_


# ---------------- masthead ----------------
d.rectangle([0, 0, W, 46], fill=BLACK)
text(8, 3, "THE WORLD TODAY", f(SERIF_B, 38), WHITE)
text(1016, 15, "MONDAY 23 NOVEMBER 2026", f(SANS_B, 15), GOLD_L, anchor="ra")

# ---------------- kicker ----------------
d.rectangle([0, 46, W, 70], fill=RED)
text(512, 51, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
     "US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     f(SANS_B, 14), WHITE, anchor="ma")

# ---------------- number strip: 2 rows x 5 cols ----------------
NUMS = [
    ("-3.3%", "KOSPI", RED_L),
    ("5.3", "US-CHINA POWER GAP", BLUE_L),
    ("11,762", "EBOLA CASES, DRC", GREEN),
    ("10T won", "SEOUL STABILISATION FUND", GOLD),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", BLUE_L),
    ("165", "RUSSIAN MISSILES/WEEK", RED_L),
    ("12,000", "CLEARED IN MANCHESTER", GREEN),
    ("264 kg", "EXPLOSIVES SEIZED", GOLD),
    ("$107.3B", "ANTHROPIC IPO", PURPLE),
]
STRIP_Y, STRIP_H = 70, 64
COL_W = 1008 // 5
for i, (val, lab, col) in enumerate(NUMS):
    row, c = divmod(i, 5)
    x0 = 8 + c * COL_W
    y0 = STRIP_Y + row * 32
    text(x0 + 2, y0 + 1, val, f(SANS_B, 17), col)
    text(x0 + 2, y0 + 20, lab, f(SANS, 8), GRAY)

# ---------------- region bar ----------------
REG_Y, REG_H = 134, 18
REGIONS = [("ASIA-PACIFIC 7", 7, BLUE), ("AMERICAS 8", 8, RED),
           ("MIDDLE EAST 6", 6, GOLD), ("EUROPE 5", 5, TEAL),
           ("AFRICA 3", 3, PURPLE), ("WORLD 2", 2, GRAY)]
rx = 8
for label, n, col in REGIONS:
    w_ = round(1008 * n / 31)
    d.rectangle([rx, REG_Y, rx + w_ - 1, REG_Y + REG_H], fill=col)
    text(rx + w_ // 2, REG_Y + 3, label, f(SANS_B, 11), WHITE, anchor="ma")
    rx += w_

# ---------------- THE DAY IN UTC strip ----------------
UTC_Y = 152
text(8, UTC_Y + 2, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   "
     "~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     f(SANS, 11), INK)
text(1016, UTC_Y + 2, "~ APPROX", f(SANS, 10), GRAY, anchor="ra")

# ---------------- heroes ----------------
HERO_X = [8, 347, 686]
HERO_W = 330
SCENE_Y, SCENE_H = 168, 112
LABEL_Y, LABEL_H = 280, 15
HEAD_Y = 300
BODY_Y = 348
SRC_Y = 380


def hero_scene_kospi(x0):
    d.rectangle([x0, SCENE_Y, x0 + HERO_W, SCENE_Y + SCENE_H], fill=NAVY)
    # lit buildings
    import random
    rnd = random.Random(81)
    bx = x0 + 8
    while bx < x0 + HERO_W - 20:
        bw, bh = rnd.randint(18, 30), rnd.randint(34, 78)
        d.rectangle([bx, SCENE_Y + SCENE_H - bh, bx + bw, SCENE_Y + SCENE_H],
                    fill=(24, 42, 84))
        for wy in range(SCENE_Y + SCENE_H - bh + 6, SCENE_Y + SCENE_H - 4, 10):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # orange chart line
    pts = [(x0 + 12, SCENE_Y + 78), (x0 + 52, SCENE_Y + 66),
           (x0 + 96, SCENE_Y + 72), (x0 + 140, SCENE_Y + 52),
           (x0 + 186, SCENE_Y + 60), (x0 + 232, SCENE_Y + 40),
           (x0 + 278, SCENE_Y + 46), (x0 + 318, SCENE_Y + 30)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=WHITE)
    text(x0 + 10, SCENE_Y + 6, "-3.3%", f(SANS_B, 26), (255, 90, 80))


def hero_scene_guterres(x0):
    d.rectangle([x0, SCENE_Y, x0 + HERO_W, SCENE_Y + SCENE_H], fill=(13, 92, 74))
    text(x0 + 12, SCENE_Y + 10, "150 DELEGATES", f(SANS_B, 26), GOLD_L)
    text(x0 + 12, SCENE_Y + 40, "BACK A RISK", f(SANS_B, 26), GOLD_L)
    text(x0 + 12, SCENE_Y + 70, "FRAMEWORK", f(SANS_B, 26), GOLD_L)
    # globe
    cx, cy, r = x0 + 268, SCENE_Y + 56, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 216, 200),
              outline=WHITE, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 150, 135))
    d.line([cx - r, cy, cx + r, cy], fill=(90, 150, 135))
    d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill=(90, 150, 135))
    d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill=(90, 150, 135))


def hero_scene_power(x0):
    d.rectangle([x0, SCENE_Y, x0 + HERO_W, SCENE_Y + SCENE_H], fill=CREAM)
    text(x0 + 10, SCENE_Y + 4, "NARROWEST SINCE 2018", f(SANS_B, 10), INK)
    text(x0 + HERO_W - 10, SCENE_Y + 4, "GAP 5.3", f(SANS_B, 11), RED, anchor="ra")
    bars = [("US", 78.9, BLUE, WHITE), ("CHINA", 73.6, RED, WHITE),
            ("INDIA", 40.5, GOLD, INK)]
    base = SCENE_Y + SCENE_H - 6
    bw, gap = 72, 22
    bx = x0 + 26
    for name, val, col, lab_col in bars:
        bh = {78.9: 44, 73.6: 41, 40.5: 24}[val]
        top = base - bh
        text(bx + bw // 2, top - 19, f"{val}", f(SANS_B, 16), INK, anchor="ma")
        d.rectangle([bx, top, bx + bw, base], fill=col)
        text(bx + bw // 2, base - 15, name, f(SANS_B, 11), lab_col, anchor="ma")
        bx += bw + gap


hero_scene_kospi(HERO_X[0])
hero_scene_guterres(HERO_X[1])
hero_scene_power(HERO_X[2])

HEROES = [
    ("KOSPI 4,708.54  \u00b7  -161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
     "Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE"),
    ("UN  \u00b7  BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; "
     "150 back a risk framework.", "UNITED NATIONS"),
    ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest "
     "since 2018. India third at 40.5.", "LOWY INSTITUTE"),
]
for i, (lab, head, body, src) in enumerate(HEROES):
    x0 = HERO_X[i]
    d.rectangle([x0, LABEL_Y, x0 + HERO_W, LABEL_Y + LABEL_H], fill=BLACK)
    text(x0 + 6, LABEL_Y + 2, lab, f(SANS_B, 10), WHITE)
    for j, ln in enumerate(wrap(head, f(SANS_B, 20), HERO_W)):
        text(x0, HEAD_Y + j * 22, ln, f(SANS_B, 20), INK)
    for j, ln in enumerate(wrap(body, f(SANS, 12), HERO_W)[:2]):
        text(x0, BODY_Y + j * 15, ln, f(SANS, 12), (60, 60, 60))
    text(x0, SRC_Y, src, f(SANS, 10), GRAY)
    chip(x0 + HERO_W - 62, SRC_Y - 2, "REPORTED", "REPORTED")

# ---------------- MORE OF THE DAY strip ----------------
MORE_Y = 398
d.rectangle([0, MORE_Y, W, MORE_Y + 18], fill=BLACK)
text(8, MORE_Y + 2, "MORE OF THE DAY  \u2014  10 STORIES", f(SANS_B, 12), WHITE)

# ---------------- cards: 2 rows x 5 ----------------
CARDS = [
    ("AMERICAS", BLUE, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
     "Reuters", "REPORTED"),
    ("FBI", BLUE, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", GOLD, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.",
     "Reuters", "REPORTED"),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.",
     "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M DEAL", "Nine-year deal, largest ever.",
     "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.",
     "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", BLUE, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
     "WSJ", "REPORTED"),
    ("EUROPE", GOLD, "POLAND: 3 MISSILES CROSSED AIRSPACE",
     "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", PURPLE, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
     "Reuters", "CLAIM"),
]
CARD_W, CARD_GAP = 196, 7
CARD_H = 66
for i, (cat, col, head, body, src, kind) in enumerate(CARDS):
    row, c = divmod(i, 5)
    x0 = 8 + c * (CARD_W + CARD_GAP)
    y0 = 422 + row * 70
    d.rectangle([x0, y0, x0 + CARD_W, y0 + 14], fill=col)
    text(x0 + 4, y0 + 2, cat, f(SANS_B, 10), WHITE)
    text(x0 + CARD_W - 4, y0 + 2, str(i + 1), f(SANS_B, 10), WHITE, anchor="ra")
    lines = wrap(head, f(SANS_B, 12), CARD_W - 2)
    for j, ln in enumerate(lines[:2]):
        text(x0 + 1, y0 + 16 + j * 14, ln, f(SANS_B, 12), INK)
    by = y0 + 16 + min(len(lines), 2) * 14 + 1
    text(x0 + 1, by, body, f(SANS, 10), (60, 60, 60))
    sy = y0 + CARD_H - 13
    text(x0 + 1, sy, src, f(SANS, 9), GRAY)
    chip(x0 + CARD_W - 62, sy - 1, kind, kind)

# ---------------- WHERE IT HAPPENED strip ----------------
WHERE_Y = 566
d.rectangle([0, WHERE_Y, W, WHERE_Y + 18], fill=BLACK)
text(8, WHERE_Y + 2, "WHERE IT HAPPENED", f(SANS_B, 12), WHITE)
text(344, WHERE_Y + 2, "ALSO ON MONDAY", f(SANS_B, 12), WHITE)

# ---------------- map ----------------
MAP_X, MAP_Y, MAP_W, MAP_H = 8, 588, 322, 264
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], outline=INK, width=1)
# stylised continents (light green blobs)
d.polygon([(18, 640), (60, 610), (110, 612), (128, 650), (108, 700),
           (86, 760), (60, 800), (34, 770), (22, 700)], fill=(205, 232, 190))
d.polygon([(150, 620), (300, 606), (322, 640), (310, 700), (270, 730),
           (210, 724), (160, 690), (148, 650)], fill=(205, 232, 190))
d.polygon([(210, 740), (262, 736), (272, 770), (240, 800), (214, 776)],
          fill=(205, 232, 190))
d.ellipse([286, 796, 318, 826], fill=(205, 232, 190))
PINS = {1: (44, 700), 2: (66, 788), 3: (288, 640), 4: (88, 668), 5: (104, 640),
        6: (238, 648), 7: (78, 700), 8: (30, 716), 9: (52, 748), 10: (66, 772),
        11: (214, 640), 12: (196, 628), 13: (262, 622)}
for n, (px, py) in PINS.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    text(px, py - 5, str(n), f(SANS_B, 9), WHITE, anchor="ma")
text(MAP_X + 6, MAP_Y + MAP_H - 42,
     "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", f(SANS, 9), INK)
text(MAP_X + 6, MAP_Y + MAP_H - 30,
     "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF",
     f(SANS, 9), INK)
text(MAP_X + 6, MAP_Y + MAP_H - 18,
     "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow",
     f(SANS, 9), INK)

# ---------------- ALSO list ----------------
ALSO = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe  [CLAIM]",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones  [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
ay = 590
for item in ALSO:
    if "[CLAIM]" in item:
        base, _ = item.split("  [CLAIM]")
        text(344, ay, base, f(SANS, 12), INK)
        w_ = d.textlength(base, font=f(SANS, 12))
        text(344 + w_ + 4, ay, "[CLAIM]", f(SANS_B, 11), RED)
    else:
        text(344, ay, item, f(SANS, 12), INK)
    ay += 15

# ---------------- DATE CHECK ----------------
DC_Y, DC_H = 862, 62
d.rectangle([8, DC_Y, 1016, DC_Y + DC_H], outline=RED, width=2)
text(14, DC_Y + 4, "DATE CHECK", f(SANS_B, 12), RED)
text(1010, DC_Y + 4, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
     f(SANS_B, 9), RED, anchor="ra")
text(14, DC_Y + 22,
     "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 "
     "El Chapo (22 Nov) \u00b7 EU-Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 "
     "ICJ Myanmar (19 Nov)", f(SANS, 11), INK)
text(14, DC_Y + 40,
     "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 "
     "COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff", f(SANS, 11), INK)

# ---------------- footer ----------------
FY = 934
text(8, FY, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 "
     "WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     f(SANS, 10), GRAY)
text(8, FY + 14, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, "
     "not independently confirmed. ONGOING = still developing.",
     f(SANS, 10), GRAY)
text(8, FY + 28, "All times UTC. Figures as reported 23 Nov 2026. "
     "Scenes are drawn illustrations, not photographs.", f(SANS, 10), GRAY)
d.line([8, FY + 46, 1016, FY + 46], fill=GOLD, width=2)
text(512, FY + 54, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  "
     "31 stories  \u00b7  6 regions", f(SANS_B, 13), GOLD, anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
