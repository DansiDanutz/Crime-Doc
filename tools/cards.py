#!/usr/bin/env python3
"""cards.py — the on-screen cards of an episode: date stamps, name tags, figures, questions.

Cards are data, in the episode's production/cards.json: each names its chapter, when it appears
(seconds into that chapter), how long it stays, its kind and its words. This module checks them
against the storyboard and draws each one as a transparent 1280x720 image in the umbra. look
(white on near-black, one red accent); tools/assemble-episode.py fades them over the picture.

Kinds:
  stamp     date / place stamp, bottom left            {"lines": ["16 NOVEMBER 1984", "HAMBURG"]}
  tag       DNA name tag with a pointer                {"text": "...", "sub": "...", "role": "subject"|"institution", "pos": "tl"}
  figure    one big number or term + a label           {"value": "DM 9.97", "label": "PER PAGE VIEW"}
  question  the question put to the viewer             {"text": "WHERE DID THE PASSWORD COME FROM?"}
  act       part title                                 {"part": "PART I", "title": "THE PROMISE"}
  flag      small "keep this in mind" note, top right  {"label": "KEEP IN MIND", "text": "..."}
  file      summary of a document's findings           {"header": "...", "rows": ["FINDING | RESULT"]}
  list      a short numbered list                      {"rows": ["A WATCHED DEMONSTRATION?", ...]}

Usage:
    tools/cards.py umbra ep03-ghost-characters                # check cards.json
    tools/cards.py umbra ep03-ghost-characters --sheet x.png  # contact sheet of every card
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 720
INK = (10, 10, 11)
PAPER = (244, 243, 239)
RED = (200, 16, 46)
GREY = (176, 176, 172)
KINDS = {
    "stamp": ("lines",), "tag": ("text",), "figure": ("value", "label"), "question": ("text",),
    "act": ("part", "title"), "flag": ("label", "text"), "file": ("header", "rows"), "list": ("rows",),
}
MIN_S, MAX_S = 1.5, 8.0
MAX_LINE = 48  # characters; a card is read in a glance, not studied
FADE_S = 0.25

FONTS = {  # first file that exists wins; macOS first, then common Linux fonts
    "bold": ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "mono": ["/System/Library/Fonts/Supplemental/Courier New Bold.ttf", "/Library/Fonts/Courier New Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"],
}


def load_tool(name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), Path(__file__).resolve().parent / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- validation (no Pillow needed)

def chapter_windows(shotlist: dict) -> dict[str, tuple[float, float]]:
    """chapter id -> (start, length) in seconds of the cut."""
    windows, t = {}, 0.0
    for chapter in shotlist["chapters"]:
        length = float(sum(int(sc["duration_s"]) for sc in chapter["scenes"]))
        windows[chapter["id"]] = (t, length)
        t += length
    return windows


def card_lines(card: dict) -> list[str]:
    lines = []
    for field in ("lines", "rows"):
        lines += card.get(field, [])
    for field in ("text", "sub", "value", "label", "part", "title", "header"):
        if card.get(field):
            lines.append(card[field])
    return lines


def plan(cards: list[dict], shotlist: dict) -> list[dict]:
    """Validate cards against the storyboard; return them with absolute start/end, in time order.
    Raises ValueError naming the card at fault."""
    windows = chapter_windows(shotlist)
    placed = []
    for i, card in enumerate(cards):
        name = f"card {i + 1} ({card.get('chapter')}, {card.get('kind')})"
        kind = card.get("kind")
        if kind not in KINDS:
            raise ValueError(f"{name}: unknown kind; use one of {', '.join(KINDS)}")
        missing = [f for f in KINDS[kind] if not card.get(f)]
        if missing:
            raise ValueError(f"{name}: missing {', '.join(missing)}")
        if card.get("chapter") not in windows:
            raise ValueError(f"{name}: no chapter {card.get('chapter')!r} in the shotlist")
        try:
            at, dur = float(card.get("at", -1)), float(card.get("dur", 0))
        except (TypeError, ValueError):
            raise ValueError(f"{name}: at and dur must be numbers")
        if not (math.isfinite(at) and math.isfinite(dur)):
            raise ValueError(f"{name}: at and dur must be finite numbers")
        start, length = windows[card["chapter"]]
        if at < 0 or not MIN_S <= dur <= MAX_S:
            raise ValueError(f"{name}: needs at >= 0 and dur between {MIN_S} and {MAX_S} s")
        if at + dur > length + 1e-6:
            raise ValueError(f"{name}: runs past the end of its {length:g} s chapter")
        long = [s for s in card_lines(card) if len(s) > MAX_LINE]
        if long:
            raise ValueError(f"{name}: line over {MAX_LINE} characters: {long[0]!r}")
        if kind == "tag" and card.get("role", "subject") not in ("subject", "institution"):
            raise ValueError(f"{name}: role must be subject or institution")
        placed.append({**card, "start": round(start + at, 3), "end": round(start + at + dur, 3)})
    placed.sort(key=lambda c: c["start"])
    for a, b in zip(placed, placed[1:]):
        if b["start"] < a["end"]:
            raise ValueError(f"cards overlap: {a['chapter']} {a['kind']} and {b['chapter']} {b['kind']} "
                             "(one card on screen at a time)")
    return placed


def load(ep: Path, shotlist: dict) -> list[dict]:
    path = ep / "production" / "cards.json"
    if not path.exists():
        return []
    return plan(json.loads(path.read_text())["cards"], shotlist)


# ---------------------------------------------------------------- drawing (Pillow)

def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        raise SystemExit("error: Pillow is missing; run `python -m pip install -r requirements.txt`")
    return Image, ImageDraw, ImageFilter, ImageFont


def font(style: str, size: int):
    _, _, _, ImageFont = _pil()
    for path in FONTS[style]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)  # Pillow's bundled font: plainer, but the card still renders


def text_w(draw, s: str, f, tracking: int = 0) -> int:
    return int(draw.textlength(s, font=f)) + tracking * max(len(s) - 1, 0)


def tracked(draw, xy, s: str, f, fill, tracking: int = 0) -> None:
    """Draw with letter-spacing (Pillow has none built in)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking


def wrap(draw, s: str, f, width: int) -> list[str]:
    lines, line = [], ""
    for word in s.split():
        test = f"{line} {word}".strip()
        if line and draw.textlength(test, font=f) > width:
            lines.append(line)
            line = word
        else:
            line = test
    return lines + ([line] if line else [])


def panel(img, box, fill, radius=0, soft=0):
    Image, ImageDraw, ImageFilter, _ = _pil()
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill)
    if soft:
        layer = layer.filter(ImageFilter.GaussianBlur(soft))
    img.alpha_composite(layer)


def render(card: dict):
    Image, ImageDraw, _, _ = _pil()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    kind = card["kind"]

    if kind == "stamp":
        big, small = font("mono", 30), font("mono", 20)
        first, rest = card["lines"][0], card["lines"][1:]
        width = max([text_w(draw, first, big, 3)] + [text_w(draw, s, small, 2) for s in rest]) + 56
        height = 34 + 40 + 28 * len(rest)
        x0, y0 = 56, H - 56 - height
        panel(img, (x0, y0, x0 + width, y0 + height), INK + (215,))
        draw.rectangle((x0, y0, x0 + 6, y0 + height), fill=RED)
        tracked(draw, (x0 + 28, y0 + 16), first, big, PAPER, 3)
        for j, s in enumerate(rest):
            tracked(draw, (x0 + 28, y0 + 58 + 28 * j), s, small, GREY, 2)

    elif kind == "tag":
        main, sub = font("bold", 30), font("mono", 18)
        subject = card.get("role", "subject") == "subject"
        width = max(text_w(draw, card["text"], main), text_w(draw, card.get("sub", ""), sub, 2)) + 44
        height = 58 + (26 if card.get("sub") else 0)
        pos = card.get("pos", "tl")
        x0 = 64 if pos[1] == "l" else (W - 64 - width if pos[1] == "r" else (W - width) // 2)
        top = pos[0] == "t"
        y0 = 72 if top else H - 72 - height
        fill = RED if subject else INK
        draw.rectangle((x0, y0, x0 + width, y0 + height), fill=fill + (255,),
                       outline=None if subject else PAPER, width=0 if subject else 2)
        tip_x = x0 + 40
        if top:  # pointer hangs below the box, the DNA's "triangular pointer at the relevant head"
            draw.polygon([(tip_x - 14, y0 + height), (tip_x + 14, y0 + height), (tip_x, y0 + height + 18)], fill=fill)
        else:
            draw.polygon([(tip_x - 14, y0), (tip_x + 14, y0), (tip_x, y0 - 18)], fill=fill)
        draw.text((x0 + 22, y0 + 12), card["text"], font=main, fill=PAPER)
        if card.get("sub"):
            tracked(draw, (x0 + 22, y0 + 52), card["sub"], sub, PAPER if subject else GREY, 2)

    elif kind == "figure":
        size = 104
        while size > 56 and text_w(draw, card["value"], font("bold", size)) > W - 2 * 88:
            size -= 4  # long terms ("GHOST CHARACTERS") shrink to fit the frame
        value, label = font("bold", size), font("mono", 22)
        vw = text_w(draw, card["value"], value)
        lw = text_w(draw, card["label"], label, 3)
        x0, cy = 88, H // 2
        panel(img, (0, cy - 150, max(vw, lw) + 200, cy + 150), INK + (170,), soft=40)
        draw.text((x0, cy - 92), card["value"], font=value, fill=PAPER)
        draw.rectangle((x0, cy + 34, x0 + 120, cy + 40), fill=RED)
        tracked(draw, (x0, cy + 56), card["label"], label, PAPER, 3)

    elif kind == "question":
        q, label = font("bold", 50), font("mono", 20)
        lines = wrap(draw, card["text"], q, 1040)
        height = 70 + 62 * len(lines) + 34
        y0 = int(H * 0.60) - height // 2
        panel(img, (0, y0, W, y0 + height), INK + (205,))
        draw.rectangle((0, y0, W, y0 + 4), fill=RED)
        tag = card.get("label", "THE QUESTION")
        tracked(draw, ((W - text_w(draw, tag, label, 4)) // 2, y0 + 26), tag, label, RED, 4)
        for j, s in enumerate(lines):
            draw.text(((W - text_w(draw, s, q)) // 2, y0 + 64 + 62 * j), s, font=q, fill=PAPER)

    elif kind == "act":
        part, title = font("mono", 26), font("bold", 92)
        panel(img, (0, 0, W, H), INK + (150,))
        pw, tw = text_w(draw, card["part"], part, 6), text_w(draw, card["title"], title, 4)
        tracked(draw, ((W - pw) // 2, H // 2 - 96), card["part"], part, RED, 6)
        tracked(draw, ((W - tw) // 2, H // 2 - 50), card["title"], title, PAPER, 4)
        draw.rectangle((W // 2 - 44, H // 2 + 72, W // 2 + 44, H // 2 + 77), fill=RED)

    elif kind == "flag":
        label, body = font("mono", 18), font("bold", 26)
        lines = wrap(draw, card["text"], body, 420)
        width, height = 470, 56 + 34 * len(lines) + 18
        x0, y0 = W - 56 - width, 56
        panel(img, (x0, y0, x0 + width, y0 + height), INK + (220,))
        draw.rectangle((x0, y0, x0 + 6, y0 + height), fill=RED)
        tracked(draw, (x0 + 26, y0 + 18), card["label"], label, RED, 3)
        for j, s in enumerate(lines):
            draw.text((x0 + 26, y0 + 48 + 34 * j), s, font=body, fill=PAPER)

    elif kind == "file":
        head, row, val, lab = font("mono", 22), font("mono", 24), font("bold", 24), font("mono", 17)
        rows = [r.split(" | ", 1) for r in card["rows"]]
        width = 720
        sheet = Image.new("RGBA", (width, 136 + 52 * len(rows)), PAPER + (250,))
        sd = ImageDraw.Draw(sheet)
        tracked(sd, (34, 28), card.get("label", "SUMMARY OF FINDINGS"), lab, RED, 3)
        sd.text((34, 56), card["header"], font=head, fill=INK)
        sd.line((34, 96, width - 34, 96), fill=INK, width=2)
        for j, (left, *right) in enumerate(rows):
            y = 116 + 52 * j
            sd.text((34, y), left, font=row, fill=INK)
            if right:
                sd.text((width - 34 - text_w(sd, right[0], val), y), right[0], font=val,
                        fill=RED if "NOT" in right[0] else INK)
        sheet = sheet.rotate(1.4, expand=True, resample=3)
        x0, y0 = W - sheet.width - 60, (H - sheet.height) // 2 - 20
        panel(img, (x0 + 10, y0 + 14, x0 + sheet.width + 10, y0 + sheet.height + 14), (0, 0, 0, 120), soft=14)
        img.alpha_composite(sheet, (x0, y0))

    elif kind == "list":
        idx, row = font("mono", 28), font("bold", 46)
        rows = card["rows"]
        height = 76 * len(rows) + 60
        y0 = (H - height) // 2
        panel(img, (0, y0 - 20, W, y0 + height + 20), INK + (190,), soft=30)
        width = max(text_w(draw, s, row) for s in rows) + 90
        x0 = (W - width) // 2
        for j, s in enumerate(rows):
            y = y0 + 30 + 76 * j
            tracked(draw, (x0, y + 10), f"{j + 1:02d}", idx, RED, 2)
            draw.text((x0 + 90, y), s, font=row, fill=PAPER)
    return img


def render_all(cards: list[dict], out_dir: Path) -> list[Path]:
    paths = []
    for i, card in enumerate(cards):
        path = out_dir / f"card-{i + 1:02d}-{card['kind']}.png"
        render(card).save(path)
        paths.append(path)
    return paths


def contact_sheet(cards: list[dict], dest: Path, cols: int = 3) -> None:
    Image, ImageDraw, _, _ = _pil()
    tw, th = W // 2, H // 2
    rows = (len(cards) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (40, 40, 42))
    label = font("mono", 16)
    for i, card in enumerate(cards):
        bg = Image.new("RGBA", (W, H), (96, 98, 102, 255))  # a mid-grey stand-in for footage
        bg.alpha_composite(render(card))
        tile = bg.convert("RGB").resize((tw, th))
        ImageDraw.Draw(tile).text((10, 8), f"{card['chapter']} +{card['at']}s  {card['kind']}",
                                  font=label, fill=(255, 255, 0))
        sheet.paste(tile, ((i % cols) * tw, (i // cols) * th))
    sheet.save(dest)


def overlay_filter(cards: list[dict], first_input: int = 1) -> tuple[str, str]:
    """ffmpeg filter graph fading each card in and out over [0:v]; returns (graph, output label)."""
    parts, base = [], "0:v"
    for i, card in enumerate(cards):
        n, dur = first_input + i, card["end"] - card["start"]
        parts.append(f"[{n}:v]format=rgba,fade=in:st=0:d={FADE_S}:alpha=1,"
                     f"fade=out:st={dur - FADE_S:.3f}:d={FADE_S}:alpha=1,"
                     f"setpts=PTS-STARTPTS+{card['start']:.3f}/TB[c{i}]")
        out = f"v{i}"
        parts.append(f"[{base}][c{i}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{card['start']:.3f},{card['end']:.3f})'[{out}]")
        base = out
    return ";".join(parts), base


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("episode")
    ap.add_argument("--sheet", type=Path, help="write a contact sheet PNG of every card")
    args = ap.parse_args(argv)
    assemble = load_tool("assemble-episode")
    ep = assemble.episode_dir(args.channel, args.episode)
    shotlist = json.loads((ep / "production" / "shotlist.json").read_text())
    try:
        cards = load(ep, shotlist)
    except ValueError as err:
        print(f"error: cards.json: {err}", file=sys.stderr)
        return 2
    print(f"{len(cards)} card(s), {sum(c['end'] - c['start'] for c in cards):.1f} s on screen")
    for c in cards:
        print(f"  {c['start']:6.1f}-{c['end']:6.1f}  {c['chapter']}  {c['kind']:8}  {' / '.join(card_lines(c))[:70]}")
    if args.sheet:
        contact_sheet(cards, args.sheet)
        print(f"sheet: {args.sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
