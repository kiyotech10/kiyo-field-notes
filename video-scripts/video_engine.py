#!/usr/bin/env python3
"""
汎用スライドビデオエンジン
使い方: from video_engine import render_video, SLIDES型定義を参照
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Config ─────────────────────────────────────────────────────
W, H  = 1920, 1080
FPS   = 30
FONT  = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
FADE  = 15  # frames (0.5 sec)

# Colors
BG     = (9,   9,   9)
WHITE  = (240, 240, 240)
AMBER  = (245, 158, 11)
GRAY   = (156, 163, 175)
DARK_G = (75,  85,  99)
PANEL  = (17,  24,  39)
BORDER = (55,  65,  81)
DIM    = (31,  41,  55)
GREEN  = (34,  197, 94)
RED    = (239, 68,  68)
BLUE   = (96,  165, 250)

def f(size):
    return ImageFont.truetype(FONT, size)

def new_img():
    return Image.new("RGB", (W, H), BG)

def sz(d, text, font):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]

def cx_text(d, text, y, font, color=WHITE):
    w, h = sz(d, text, font)
    d.text(((W - w) // 2, y), text, font=font, fill=color)
    return y + h

def add_glow(im, color=(245, 158, 11), intensity=0.06):
    arr = np.array(im, dtype=np.float32)
    cx, cy = W / 2, H / 2
    Y, X = np.ogrid[:H, :W]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    mask = np.clip(1.0 - dist / (W * 0.42), 0, 1) ** 2 * intensity * 255
    for i, c in enumerate(color):
        arr[:, :, i] = np.clip(arr[:, :, i] + mask * (c / 255), 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

def wrap_text(d, text, font, max_width):
    """テキストを max_width 内に折り返す"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        w, _ = sz(d, test, font)
        if w > max_width and current:
            lines.append(current)
            current = char
        else:
            current = test
    if current:
        lines.append(current)
    return lines

# ─────────────────────────────────────────────────────────────
# Slide type renderers
# ─────────────────────────────────────────────────────────────

def render_HOOK(slide):
    """
    フック（冒頭）スライド
    keys: label, line1, accent, line2(opt), sub
    """
    im = add_glow(new_img())
    d = ImageDraw.Draw(im)
    lbf = f(26); mf = f(90); sf = f(38)
    label = slide.get("label", "")
    line1 = slide.get("line1", "")
    accent = slide.get("accent", "")
    line2 = slide.get("line2", "")
    sub = slide.get("sub", "")

    elems = []
    if label:  elems.append(("label", label))
    if line1:  elems.append(("main",  line1))
    if accent: elems.append(("acc",   accent))
    if line2:  elems.append(("main",  line2))
    if sub:    elems.append(("sub",   sub))

    heights = []
    for typ, txt in elems:
        fo = lbf if typ == "label" else (sf if typ == "sub" else mf)
        _, h = sz(d, txt, fo)
        heights.append(h)

    gaps = [28 if i == 0 else 16 for i in range(len(elems) - 1)]
    total = sum(heights) + sum(gaps)
    y = (H - total) // 2

    for i, (typ, txt) in enumerate(elems):
        fo = lbf if typ == "label" else (sf if typ == "sub" else mf)
        col = AMBER if typ in ("label", "acc") else (GRAY if typ == "sub" else WHITE)
        w, h = sz(d, txt, fo)
        d.text(((W - w) // 2, y), txt, font=fo, fill=col)
        y += h + (gaps[i] if i < len(gaps) else 0)
    return im


def render_SECTION(slide):
    """
    セクション区切り
    keys: number(opt), title, sub(opt)
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    mf = f(80); sf = f(38); nf = f(26)
    number = slide.get("number", "")
    title = slide.get("title", "")
    sub = slide.get("sub", "")

    parts = []
    if number: parts.append(("num", number))
    parts.append(("title", title))
    if sub: parts.append(("sub", sub))

    heights = [sz(d, t, (nf if k == "num" else (sf if k == "sub" else mf)))[1] for k, t in parts]
    total = sum(heights) + 20 * (len(parts) - 1)
    y = (H - total) // 2

    # 左アクセントライン
    lx = 120; lw = 6
    d.rectangle([lx, (H - total) // 2 - 10, lx + lw, (H + total) // 2 + 10], fill=AMBER)

    for i, (k, txt) in enumerate(parts):
        fo = nf if k == "num" else (sf if k == "sub" else mf)
        col = AMBER if k == "num" else (GRAY if k == "sub" else WHITE)
        w, h = sz(d, txt, fo)
        d.text((lx + lw + 36, y), txt, font=fo, fill=col)
        y += h + 20
    return im


def render_STATEMENT(slide):
    """
    ステートメント（主張）スライド
    keys: label(opt), lines: list[str|dict(text,accent)]
    sub(opt): str
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); mf = f(72); sf = f(36)
    label = slide.get("label", "")
    lines = slide.get("lines", [])
    sub = slide.get("sub", "")

    # lines can be str or {"text":"...", "accent":"..."} dicts
    heights = []
    if label:
        _, h = sz(d, label, lbf)
        heights.append(("label", label, lbf, h))
    for line in lines:
        if isinstance(line, str):
            _, h = sz(d, line, mf)
            heights.append(("plain", line, mf, h))
        else:
            _, h = sz(d, line["text"], mf)
            heights.append(("mixed", line, mf, h))
    if sub:
        _, h = sz(d, sub, sf)
        heights.append(("sub", sub, sf, h))

    total = sum(h for *_, h in heights) + 20 * (len(heights) - 1)
    y = (H - total) // 2 - 20

    for i, item in enumerate(heights):
        kind = item[0]
        if kind == "label":
            _, txt, fo, h = item
            w, _ = sz(d, txt, fo)
            d.text(((W - w) // 2, y), txt, font=fo, fill=AMBER)
        elif kind == "plain":
            _, txt, fo, h = item
            w, _ = sz(d, txt, fo)
            d.text(((W - w) // 2, y), txt, font=fo, fill=WHITE)
        elif kind == "mixed":
            _, line_d, fo, h = item
            # line_d has 'text' and 'accent'
            pre  = line_d.get("pre", "")
            acc  = line_d.get("accent", "")
            post = line_d.get("post", "")
            text = line_d.get("text", "")
            if acc and (pre or post):
                pw, _ = sz(d, pre, fo)
                aw, _ = sz(d, acc, fo)
                pstw, _ = sz(d, post, fo)
                total_w = pw + aw + pstw
                x = (W - total_w) // 2
                d.text((x, y), pre, font=fo, fill=WHITE)
                d.text((x + pw, y), acc, font=fo, fill=AMBER)
                d.text((x + pw + aw, y), post, font=fo, fill=WHITE)
            else:
                w, _ = sz(d, text, fo)
                d.text(((W - w) // 2, y), text, font=fo, fill=AMBER)
        elif kind == "sub":
            _, txt, fo, h = item
            w, _ = sz(d, txt, fo)
            d.text(((W - w) // 2, y), txt, font=fo, fill=GRAY)
        y += item[-1] + 20
    return im


def render_LIST(slide):
    """
    番号付きリスト
    keys: label(opt), items: list[str|dict(num,text,sub)]
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); nf = f(52); bf = f(44); sf = f(30)
    label = slide.get("label", "")
    items = slide.get("items", [])

    row_h = 110
    list_w = 1100
    lbw, lbh = sz(d, label, lbf) if label else (0, 0)
    total_h = (lbh + 38 if label else 0) + row_h * len(items)
    y = (H - total_h) // 2
    lx = (W - list_w) // 2

    if label:
        d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER)
        y += lbh + 38

    for i, item in enumerate(items):
        ry = y + i * row_h
        if i > 0:
            d.rectangle([lx, ry - 1, lx + list_w, ry], fill=DIM)
        if isinstance(item, str):
            num = str(i + 1)
            nw, nh = sz(d, num, nf)
            tw, th = sz(d, item, bf)
            d.text((lx, ry + (row_h - nh) // 2 - 4), num, font=nf, fill=AMBER)
            d.text((lx + 80, ry + (row_h - th) // 2 - 4), item, font=bf, fill=WHITE)
        else:
            num = item.get("num", str(i + 1))
            text = item.get("text", "")
            sub  = item.get("sub", "")
            nw, nh = sz(d, num, nf)
            tw, th = sz(d, text, bf)
            d.text((lx, ry + (row_h - nh) // 2 - 4 - (15 if sub else 0)), num, font=nf, fill=AMBER)
            d.text((lx + 80, ry + (row_h - th) // 2 - 4 - (12 if sub else 0)), text, font=bf, fill=WHITE)
            if sub:
                sw, sh = sz(d, sub, sf)
                d.text((lx + 80, ry + (row_h - th) // 2 + th + 2), sub, font=sf, fill=GRAY)
    return im


def render_TABLE(slide):
    """
    シンプルテーブル
    keys: label(opt), headers: list[str], rows: list[list[str]]
    accent_col(opt): int (0-indexed, amber color)
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); hf = f(32); cf = f(30)
    label = slide.get("label", "")
    headers = slide.get("headers", [])
    rows = slide.get("rows", [])
    accent_col = slide.get("accent_col", -1)

    col_w = 1400 // max(len(headers), 1)
    row_h = 68
    table_w = col_w * len(headers)
    tx = (W - table_w) // 2

    lbw, lbh = sz(d, label, lbf) if label else (0, 0)
    total_h = (lbh + 32 if label else 0) + row_h * (1 + len(rows))
    y = (H - total_h) // 2

    if label:
        d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER)
        y += lbh + 32

    # header row
    d.rectangle([tx, y, tx + table_w, y + row_h], fill=PANEL)
    for ci, h in enumerate(headers):
        col_color = AMBER if ci == accent_col else WHITE
        hw, hh = sz(d, h, hf)
        cx = tx + ci * col_w + (col_w - hw) // 2
        d.text((cx, y + (row_h - hh) // 2), h, font=hf, fill=col_color)
    y += row_h

    for ri, row in enumerate(rows):
        bg = (14, 20, 30) if ri % 2 == 0 else (10, 14, 22)
        d.rectangle([tx, y, tx + table_w, y + row_h], fill=bg)
        for ci, cell in enumerate(row):
            col_color = AMBER if ci == accent_col else (GRAY if ri % 2 == 0 else WHITE)
            cw2, ch = sz(d, cell, cf)
            cx = tx + ci * col_w + (col_w - cw2) // 2
            d.text((cx, y + (row_h - ch) // 2), cell, font=cf, fill=col_color)
        y += row_h
    return im


def render_QUOTE(slide):
    """
    引用ボックス
    keys: label(opt), quote_lines: list[str], accent_word(opt)
    sub(opt)
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); qf = f(50); sf = f(34)
    label = slide.get("label", "")
    quote_lines = slide.get("quote_lines", [])
    sub = slide.get("sub", "")
    accent_word = slide.get("accent_word", "")

    qsz = [sz(d, l, qf) for l in quote_lines]
    qpad = 56
    box_w = max((w for w, _ in qsz), default=400) + qpad * 2
    box_w = min(box_w, W - 200)
    box_h = sum(h for _, h in qsz) + 18 * (len(quote_lines) - 1) + qpad * 2

    lbw, lbh = sz(d, label, lbf) if label else (0, 0)
    sw2, sh = sz(d, sub, sf) if sub else (0, 0)
    total_h = (lbh + 36 if label else 0) + box_h + (20 + sh if sub else 0)
    y = (H - total_h) // 2

    if label:
        d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER)
        y += lbh + 36

    bx = (W - box_w) // 2
    d.rounded_rectangle([bx, y, bx + box_w, y + box_h], radius=16, fill=(10, 8, 2), outline=AMBER, width=2)
    # side bar
    d.rectangle([bx, y + 14, bx + 5, y + box_h - 14], fill=AMBER)
    ty = y + qpad
    for line, (lw, lh) in zip(quote_lines, qsz):
        if accent_word and accent_word in line:
            idx = line.index(accent_word)
            pre, mid, post = line[:idx], accent_word, line[idx + len(accent_word):]
            pw, _ = sz(d, pre, qf); aw, _ = sz(d, mid, qf); pstw, _ = sz(d, post, qf)
            total_w = pw + aw + pstw
            x0 = bx + (box_w - total_w) // 2
            d.text((x0, ty), pre, font=qf, fill=WHITE)
            d.text((x0 + pw, ty), mid, font=qf, fill=AMBER)
            d.text((x0 + pw + aw, ty), post, font=qf, fill=WHITE)
        else:
            d.text((bx + (box_w - lw) // 2, ty), line, font=qf, fill=WHITE)
        ty += lh + 18
    y += box_h + 20

    if sub:
        d.text(((W - sw2) // 2, y), sub, font=sf, fill=GRAY)
    return im


def render_COMPARE(slide):
    """
    2列比較
    keys: label(opt), left_label, left_items: list[str]
                      right_label, right_items: list[str]
    highlight: "left" | "right" | "both"
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); hf = f(44); bf = f(36)
    label = slide.get("label", "")
    left_label  = slide.get("left_label", "")
    right_label = slide.get("right_label", "")
    left_items  = slide.get("left_items", [])
    right_items = slide.get("right_items", [])
    highlight   = slide.get("highlight", "right")

    bxw = 720; gap = 80; bxh = 80 + 64 * max(len(left_items), len(right_items))
    bx1 = (W - bxw * 2 - gap) // 2
    bx2 = bx1 + bxw + gap
    bby = (H - bxh) // 2 + (30 if label else 0)

    if label:
        lbw, lbh = sz(d, label, lbf)
        d.text(((W - lbw) // 2, bby - lbh - 52), label, font=lbf, fill=AMBER)

    def draw_box(bx, header, items, highlighted):
        fill_outline = AMBER if highlighted else BORDER
        fill_bg = (20, 16, 3) if highlighted else PANEL
        d.rounded_rectangle([bx, bby, bx + bxw, bby + bxh], radius=14, fill=fill_bg, outline=fill_outline, width=2)
        hw, hh = sz(d, header, hf)
        col = AMBER if highlighted else GRAY
        d.text((bx + (bxw - hw) // 2, bby + 24), header, font=hf, fill=col)
        for i, item in enumerate(items):
            iw, ih = sz(d, item, bf)
            ic = AMBER if highlighted else WHITE
            d.text((bx + (bxw - iw) // 2, bby + 80 + i * 64), item, font=bf, fill=ic)

    draw_box(bx1, left_label,  left_items,  highlight in ("left", "both"))
    draw_box(bx2, right_label, right_items, highlight in ("right", "both"))

    vsf = f(36); vs = "VS"; vsw, vsh = sz(d, vs, vsf)
    d.text((bx1 + bxw + (gap - vsw) // 2, bby + (bxh - vsh) // 2), vs, font=vsf, fill=DARK_G)
    return im


def render_BIG_TEXT(slide):
    """
    大きいテキスト強調
    keys: pre(opt), accent, post(opt), sub(opt)
    font_size(opt): default 160
    """
    im = add_glow(new_img(), intensity=0.08)
    d = ImageDraw.Draw(im)
    fsize = slide.get("font_size", 160)
    bf = f(fsize); sf = f(40)
    pre    = slide.get("pre", "")
    accent = slide.get("accent", "")
    post   = slide.get("post", "")
    sub    = slide.get("sub", "")

    pw, ph = sz(d, pre, bf) if pre else (0, 0)
    aw, ah = sz(d, accent, bf)
    pstw, _ = sz(d, post, bf) if post else (0, 0)
    sw2, sh = sz(d, sub, sf) if sub else (0, 0)

    total_h = ah + (30 + sh if sub else 0)
    y = (H - total_h) // 2
    total_w = pw + aw + pstw
    x = (W - total_w) // 2
    if pre:   d.text((x, y), pre, font=bf, fill=WHITE)
    d.text((x + pw, y), accent, font=bf, fill=AMBER)
    if post:  d.text((x + pw + aw, y), post, font=bf, fill=WHITE)
    if sub:
        d.text(((W - sw2) // 2, y + ah + 36), sub, font=sf, fill=GRAY)
    return im


def render_CONCLUSION(slide):
    """
    結論スライド
    keys: label(opt), lines: list[dict(pre,accent,post) or str]
    """
    im = add_glow(new_img(), intensity=0.07)
    d = ImageDraw.Draw(im)
    lbf = f(26); mf = f(90)
    label = slide.get("label", "")
    lines = slide.get("lines", [])

    lbw, lbh = sz(d, label, lbf) if label else (0, 0)
    heights = [sz(d, (l if isinstance(l, str) else l.get("pre", "") + l.get("accent", "") + l.get("post", "")), mf)[1] for l in lines]
    total = (lbh + 28 if label else 0) + sum(heights) + 22 * (len(lines) - 1)
    y = (H - total) // 2

    if label:
        d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER)
        y += lbh + 28

    for i, line in enumerate(lines):
        if isinstance(line, str):
            w, h = sz(d, line, mf)
            d.text(((W - w) // 2, y), line, font=mf, fill=WHITE)
            y += h + 22
        else:
            pre  = line.get("pre", "")
            acc  = line.get("accent", "")
            post = line.get("post", "")
            pw, ph = sz(d, pre, mf) if pre else (0, 0)
            aw, ah = sz(d, acc, mf)
            pstw, _ = sz(d, post, mf) if post else (0, 0)
            total_w = pw + aw + pstw
            x = (W - total_w) // 2
            if pre:  d.text((x, y), pre, font=mf, fill=WHITE)
            d.text((x + pw, y), acc, font=mf, fill=AMBER)
            if post: d.text((x + pw + aw, y), post, font=mf, fill=WHITE)
            y += ah + 22
    return im


def render_OUTRO(slide):
    """
    エンディングスライド
    keys: message_lines: list[str], url(opt)
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); mf = f(60); cf = f(34)
    label = slide.get("label", "おわりに")
    message_lines = slide.get("message_lines", [])
    url = slide.get("url", "kiyo-field-notes.vercel.app")

    lbw, lbh = sz(d, label, lbf)
    mtsz = [sz(d, l, mf) for l in message_lines]
    mt_h = sum(h for _, h in mtsz) + 16 * (len(message_lines) - 1)
    card_lines = [
        ("チャンネル登録・高評価", WHITE),
        ("よろしくお願いします", WHITE),
        ("", None),
        (url, DARK_G),
    ]
    csz = [(sz(d, t, cf) if t else (0, 20)) for t, _ in card_lines]
    ci_h = sum(h for _, h in csz) + 10 * (len(card_lines) - 1)
    cpad = 38; cw = 700; card_h = ci_h + cpad * 2
    gap = 44
    bh = lbh + 28 + mt_h + gap + card_h
    y = (H - bh) // 2
    d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER); y += lbh + 28
    for line, (tw, th) in zip(message_lines, mtsz):
        col = AMBER if any(k in line for k in ("変わる", "大切", "重要")) else WHITE
        d.text(((W - tw) // 2, y), line, font=mf, fill=col); y += th + 16
    y += gap
    bx = (W - cw) // 2
    d.rounded_rectangle([bx, y, bx + cw, y + card_h], radius=14, fill=PANEL, outline=BORDER, width=1)
    ty = y + cpad
    for (text, col), (tw, th) in zip(card_lines, csz):
        if text and col:
            d.text((bx + (cw - tw) // 2, ty), text, font=cf, fill=col)
        ty += th + 10
    return im


def render_BULLET(slide):
    """
    箇条書きスライド
    keys: label(opt), items: list[str], sub(opt)
    """
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf = f(26); bf = f(44); sf = f(32)
    label = slide.get("label", "")
    items = slide.get("items", [])
    sub   = slide.get("sub", "")

    lbw, lbh = sz(d, label, lbf) if label else (0, 0)
    item_h = 80
    sw2, sh = sz(d, sub, sf) if sub else (0, 0)
    total_h = (lbh + 36 if label else 0) + item_h * len(items) + (20 + sh if sub else 0)
    y = (H - total_h) // 2
    lx = (W - 1100) // 2

    if label:
        d.text(((W - lbw) // 2, y), label, font=lbf, fill=AMBER)
        y += lbh + 36

    for item in items:
        # bullet
        d.ellipse([lx, y + 20, lx + 12, y + 32], fill=AMBER)
        tw, th = sz(d, item, bf)
        d.text((lx + 32, y + (item_h - th) // 2 - 4), item, font=bf, fill=WHITE)
        y += item_h

    if sub:
        d.text(((W - sw2) // 2, y + 16), sub, font=sf, fill=GRAY)
    return im


# ── Render registry ───────────────────────────────────────────
RENDERERS = {
    "HOOK":       render_HOOK,
    "SECTION":    render_SECTION,
    "STATEMENT":  render_STATEMENT,
    "LIST":       render_LIST,
    "TABLE":      render_TABLE,
    "QUOTE":      render_QUOTE,
    "COMPARE":    render_COMPARE,
    "BIG_TEXT":   render_BIG_TEXT,
    "CONCLUSION": render_CONCLUSION,
    "OUTRO":      render_OUTRO,
    "BULLET":     render_BULLET,
}


def render_video(slides, output_path):
    """
    slides: list of dicts with "type" and "hold" keys plus type-specific keys
    output_path: Path or str
    """
    output_path = Path(output_path)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "pipe:0",
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", "-preset", "fast",
        str(output_path)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    print(f"Rendering {len(slides)} slides...")
    images = []
    for i, slide in enumerate(slides):
        typ = slide.get("type", "STATEMENT")
        renderer = RENDERERS.get(typ)
        if renderer is None:
            print(f"  Warning: unknown slide type '{typ}', using STATEMENT")
            renderer = render_STATEMENT
        sys.stdout.write(f"  [{i+1}/{len(slides)}] {typ}\n")
        sys.stdout.flush()
        images.append(np.array(renderer(slide)))

    print("Writing video...")
    for i, (arr, slide) in enumerate(zip(images, slides)):
        hold = slide.get("hold", 7)
        raw = arr.tobytes()
        for _ in range(hold * FPS):
            proc.stdin.write(raw)
        if i < len(images) - 1:
            nxt = images[i + 1]
            for fi in range(FADE):
                a = fi / FADE
                bl = ((1 - a) * arr + a * nxt).astype(np.uint8)
                proc.stdin.write(bl.tobytes())

    proc.stdin.close()
    proc.wait()
    mb = output_path.stat().st_size / 1024 / 1024
    total_sec = sum(s.get("hold", 7) for s in slides) + FADE / FPS * (len(slides) - 1)
    print(f"\nDone: {output_path}")
    print(f"Size: {mb:.1f} MB | Duration: ~{total_sec:.0f}s ({total_sec/60:.1f}min)")
