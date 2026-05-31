#!/usr/bin/env python3
"""
MP4生成スクリプト: 境界知能は7人に1人 — 統計が先に決めた数字
Usage: python3 make_video.py
Output: borderline-intelligence.mp4
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────
W, H  = 1920, 1080
FPS   = 30
FONT  = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
OUT   = Path(__file__).parent / "borderline-intelligence.mp4"

# Colors
BG     = (9,   9,   9)
WHITE  = (240, 240, 240)
AMBER  = (245, 158, 11)
GRAY   = (156, 163, 175)
DARK_G = (75,  85,  99)
PANEL  = (17,  24,  39)
BORDER = (55,  65,  81)
DIM    = (31,  41,  55)

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

# ── Slide builders ────────────────────────────────────────────

def s01():
    """HOOK"""
    im = add_glow(new_img())
    d = ImageDraw.Draw(im)
    lbf, mf, sf = f(26), f(90), f(38)
    lbt = "BORDERLINE INTELLIGENCE"
    line1 = "境界知能は"
    acc   = "7人に1人"
    end   = "いる"
    sub   = "最近、SNSやニュースでよく見かける数字だ。"
    lbw, lbh = sz(d, lbt, lbf)
    l1w, l1h = sz(d, line1, mf)
    aw,  ah  = sz(d, acc, mf)
    ew,  _   = sz(d, end, mf)
    sw,  sh  = sz(d, sub, sf)
    bh = lbh + 28 + l1h + 16 + ah + 30 + sh
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER);  y += lbh + 28
    d.text(((W - l1w) // 2, y), line1, font=mf, fill=WHITE); y += l1h + 16
    tw = aw + ew; x = (W - tw) // 2
    d.text((x, y), acc, font=mf, fill=AMBER)
    d.text((x + aw, y), end, font=mf, fill=WHITE);           y += ah + 32
    d.text(((W - sw) // 2, y), sub, font=sf, fill=GRAY)
    return im

def s02():
    """HOOK 2"""
    im = add_glow(new_img())
    d = ImageDraw.Draw(im)
    mf, sf = f(80), f(40)
    l1 = "この数字の"; l2a = "正体"; l2b = "、知ってますか？"
    sub = "どこから来た数字なのか——少し立ち止まって考えてほしい。"
    l1w, l1h = sz(d, l1, mf)
    l2aw, l2ah = sz(d, l2a, mf)
    l2bw, _    = sz(d, l2b, mf)
    sw, sh     = sz(d, sub, sf)
    bh = l1h + 16 + l2ah + 30 + sh
    y  = (H - bh) // 2
    d.text(((W - l1w) // 2, y), l1, font=mf, fill=WHITE);    y += l1h + 16
    tw = l2aw + l2bw; x = (W - tw) // 2
    d.text((x, y), l2a, font=mf, fill=AMBER)
    d.text((x + l2aw, y), l2b, font=mf, fill=WHITE);         y += l2ah + 32
    d.text(((W - sw) // 2, y), sub, font=sf, fill=GRAY)
    return im

def s03():
    """DEFINITION + IQ bar"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, sf = f(26), f(80), f(34)
    lbt = "境界知能とは"
    l1_pre = "IQ "; l1_acc = "70〜85"; l1_end = " の"
    l2 = "グレーゾーン"
    sub = "知的障害（IQ 70未満）と平均（IQ 85以上）のあいだ"
    lbw, lbh = sz(d, lbt, lbf)
    pw, ph = sz(d, l1_pre, mf); aw, ah = sz(d, l1_acc, mf); ew, _ = sz(d, l1_end, mf)
    l2w, l2h = sz(d, l2, mf); sw, sh = sz(d, sub, sf)
    bar_area = 90
    bh = lbh + 28 + ph + 16 + l2h + 26 + sh + 50 + bar_area
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    tw = pw + aw + ew; x = (W - tw) // 2
    d.text((x, y), l1_pre, font=mf, fill=WHITE)
    d.text((x + pw, y), l1_acc, font=mf, fill=AMBER)
    d.text((x + pw + aw, y), l1_end, font=mf, fill=WHITE);  y += ph + 16
    d.text(((W - l2w) // 2, y), l2, font=mf, fill=WHITE);   y += l2h + 28
    d.text(((W - sw) // 2, y), sub, font=sf, fill=GRAY);    y += sh + 52
    # IQ bar
    bw = 780; bx = (W - bw) // 2; by = y; bh2 = 14
    d.rounded_rectangle([bx, by, bx + bw, by + bh2], radius=7, fill=DIM)
    def iqx(iq): return bx + int((iq - 40) / 120 * bw)
    x70, x85 = iqx(70), iqx(85)
    d.rounded_rectangle([x70, by, x85, by + bh2], radius=7, fill=AMBER)
    tf = f(22)
    for iq, label in [(55,"55"),(70,"70"),(85,"85"),(100,"100"),(115,"115"),(130,"130")]:
        tx = iqx(iq); col = AMBER if iq in (70,85) else DARK_G
        d.rectangle([tx-1, by+bh2+4, tx+1, by+bh2+14], fill=col)
        lw, lh = sz(d, label, tf)
        d.text((tx - lw//2, by + bh2 + 18), label, font=tf, fill=col)
    zf = f(22); zt = "境界知能"; zw, zh = sz(d, zt, zf)
    zcx = (x70 + x85) // 2
    d.text((zcx - zw//2, by - zh - 10), zt, font=zf, fill=AMBER)
    d.polygon([(zcx-7, by-4),(zcx+7, by-4),(zcx, by)], fill=AMBER)
    return im

def s04():
    """MATH 13.6%"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, sf = f(26), f(72), f(36)
    lbt = "正規分布の数学"
    l1 = "IQ 70〜85 の範囲には"
    l2_pre = "統計的に "; l2_acc = "約13.6%"; l2_end = " が収まる"
    sub = "標準偏差 ±1〜2 の範囲——設計の時点で決まっている"
    lbw, lbh = sz(d, lbt, lbf)
    l1w, l1h = sz(d, l1, mf)
    pw, ph = sz(d, l2_pre, mf); aw, ah = sz(d, l2_acc, mf); ew, _ = sz(d, l2_end, mf)
    sw, sh = sz(d, sub, sf)
    bh = lbh+28+l1h+16+ah+30+sh
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    d.text(((W - l1w) // 2, y), l1, font=mf, fill=WHITE);   y += l1h + 16
    tw = pw + aw + ew; x = (W - tw) // 2
    d.text((x, y), l2_pre, font=mf, fill=WHITE)
    d.text((x + pw, y), l2_acc, font=mf, fill=AMBER)
    d.text((x + pw + aw, y), l2_end, font=mf, fill=WHITE);  y += ah + 32
    d.text(((W - sw) // 2, y), sub, font=sf, fill=GRAY)
    return im

def s05():
    """7人に1人 BIG"""
    im = add_glow(new_img(), intensity=0.08)
    d = ImageDraw.Draw(im)
    bf, sf = f(200), f(40)
    t = "7人に1人"; tw, th = sz(d, t, bf)
    sub = "＝ 13.6% から来ている"; sw, sh = sz(d, sub, sf)
    bh = th + 36 + sh; y = (H - bh) // 2
    d.text(((W - tw) // 2, y), t, font=bf, fill=AMBER);     y += th + 36
    d.text(((W - sw) // 2, y), sub, font=sf, fill=GRAY)
    return im

def s06():
    """PIVOT"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf = f(26), f(80)
    lbt = "ここで問いたい"; lbw, lbh = sz(d, lbt, lbf)
    lines = ["この数字は", "どうやって生まれたのか"]
    sizes = [sz(d, l, mf) for l in lines]
    bh = lbh + 28 + sum(h for _, h in sizes) + 16
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    for i, (line, (lw, lh)) in enumerate(zip(lines, sizes)):
        col = AMBER if i == 1 else WHITE
        d.text(((W - lw) // 2, y), line, font=mf, fill=col)
        y += lh + 16
    return im

def s07():
    """VS boxes"""
    im = new_img()
    d = ImageDraw.Draw(im)
    hf, bf = f(50), f(34)
    ht = "「7人に1人」は——"; hw, hh = sz(d, ht, hf)
    bxw, bxh = 540, 180; gap = 80
    total = bxw * 2 + gap
    bx1 = (W - total) // 2; bx2 = bx1 + bxw + gap
    bby = (H - bxh) // 2 + 30
    d.text(((W - hw) // 2, bby - hh - 52), ht, font=hf, fill=WHITE)
    # box1 dim
    d.rounded_rectangle([bx1, bby, bx1+bxw, bby+bxh], radius=14, fill=PANEL, outline=BORDER, width=2)
    for li, (lt, ly_off) in enumerate([("現実から「発見」した", 0), ("数字か", 1)]):
        lw, lh = sz(d, lt, bf)
        d.text((bx1+(bxw-lw)//2, bby+(bxh-lh*2-16)//2 + li*(lh+12)), lt, font=bf, fill=GRAY)
    # VS sep
    vsf = f(40); vsw, vsh = sz(d, "?", vsf)
    d.text((bx1+bxw+(gap-vsw)//2, bby+(bxh-vsh)//2), "?", font=vsf, fill=DARK_G)
    # box2 amber
    d.rounded_rectangle([bx2, bby, bx2+bxw, bby+bxh], radius=14, fill=(20,16,3), outline=AMBER, width=2)
    for li, (lt, col) in enumerate([("定義の結果として", AMBER), ("「生まれた」数字か", AMBER)]):
        lw, lh = sz(d, lt, bf)
        d.text((bx2+(bxw-lw)//2, bby+(bxh-lh*2-16)//2 + li*(lh+12)), lt, font=bf, fill=col)
    return im

def s08():
    """ANSWER"""
    im = add_glow(new_img(), intensity=0.07)
    d = ImageDraw.Draw(im)
    lbf, bf, sf = f(26), f(140), f(40)
    lbt = "答え"; lbw, lbh = sz(d, lbt, lbf)
    bt = "後者だ"; bw, bh2 = sz(d, bt, bf)
    sub_lines = ["調べて出てきた数字ではなく", "定義によって導かれた数字だ"]
    ssz = [sz(d, l, sf) for l in sub_lines]
    sh = sum(h for _, h in ssz) + 12
    bh = lbh + 28 + bh2 + 32 + sh
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    d.text(((W - bw) // 2, y), bt, font=bf, fill=AMBER);    y += bh2 + 34
    for (line, (lw, lh)) in zip(sub_lines, ssz):
        d.text(((W - lw) // 2, y), line, font=sf, fill=GRAY); y += lh + 12
    return im

def s09():
    """MECHANISM + quote"""
    im = new_img()
    d = ImageDraw.Draw(im)
    bf, qf = f(44), f(38)
    body = [
        ("IQを正規分布で設計した時点で", WHITE),
        ("平均から1〜2標準偏差下の割合は", WHITE),
        ("数学的にもう決まっていた", AMBER),
    ]
    bsz = [sz(d, t, bf) for t, _ in body]
    body_h = sum(h for _, h in bsz) + 20 * (len(body) - 1)
    qt1 = "「境界知能」という名前をその範囲につけた瞬間——"
    qt2a = "7人に1人は"; qt2b = "自動的に確定した。"
    q1w, q1h = sz(d, qt1, qf)
    q2aw, q2ah = sz(d, qt2a, qf); q2bw, _ = sz(d, qt2b, qf)
    qpad = 36
    qbox_w = max(q1w, q2aw + q2bw) + qpad * 2
    qbox_h = q1h + q2ah + 24 + qpad * 2
    gap = 44
    bh = body_h + gap + qbox_h
    y  = (H - bh) // 2
    for (text, col), (lw, lh) in zip(body, bsz):
        d.text(((W - lw) // 2, y), text, font=bf, fill=col); y += lh + 20
    y += gap - 20
    qx = (W - qbox_w) // 2
    d.rounded_rectangle([qx, y, qx+qbox_w, y+qbox_h], radius=10, fill=(10,8,2))
    d.rectangle([qx, y+14, qx+4, y+qbox_h-14], fill=AMBER)
    ty = y + qpad
    d.text((qx + qpad, ty), qt1, font=qf, fill=(229, 231, 235)); ty += q1h + 18
    x2 = qx + qpad
    d.text((x2, ty), qt2a, font=qf, fill=GRAY)
    d.text((x2 + q2aw, ty), qt2b, font=qf, fill=AMBER)
    return im

def s10():
    """STRUCTURE: 定義→数値"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lf, df = f(80), f(40)
    lines = [
        ("「定義 → 数値」", AMBER, lf),
        ("であって", DARK_G, df),
        ("「発見 → 数値」", (100,110,120), lf),
        ("ではない", DARK_G, df),
    ]
    sizes = [sz(d, t, fo) for t, _, fo in lines]
    bh = sum(h for _, h in sizes) + 18 * (len(sizes) - 1)
    y  = (H - bh) // 2
    for (text, col, fo), (lw, lh) in zip(lines, sizes):
        d.text(((W - lw) // 2, y), text, font=fo, fill=col); y += lh + 18
    return im

def s11():
    """3 STEPS"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, nf, bf = f(26), f(52), f(48)
    lbt = "カテゴリーが作られる順番"; lbw, lbh = sz(d, lbt, lbf)
    steps = [("①","どこかに線を引く（定義する）"),
             ("②","線の内側に入る人を数える"),
             ("③","「○人に1人がXだ」と言う")]
    row_h = 92; list_w = 920
    bh = lbh + 38 + row_h * len(steps)
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 38
    lx = (W - list_w) // 2
    for i, (num, text) in enumerate(steps):
        ry = y + i * row_h
        if i > 0:
            d.rectangle([lx, ry-1, lx+list_w, ry], fill=DIM)
        nw, nh = sz(d, num, nf)
        d.text((lx, ry + (row_h - nh)//2 - 4), num, font=nf, fill=AMBER)
        tw, th = sz(d, text, bf)
        d.text((lx + 84, ry + (row_h - th)//2 - 4), text, font=bf, fill=WHITE)
    return im

def s12():
    """EXAMPLES chips"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, cf = f(26), f(72), f(34)
    lbt = "同じ構造の例"; lbw, lbh = sz(d, lbt, lbf)
    t1 = "線の位置が変われば"
    t2 = "有病率も変わる"
    t1w, t1h = sz(d, t1, mf); t2w, t2h = sz(d, t2, mf)
    chips = ["高血圧の基準値","貧困線","肥満（BMI）","境界知能"]
    csz = [sz(d, c, cf) for c in chips]
    cpx, cpy = 36, 18
    cws = [w + cpx*2 for w, _ in csz]; chs = [h + cpy*2 for _, h in csz]
    cgap = 24; row_h = max(chs)
    chips_w = sum(cws) + cgap*(len(chips)-1)
    bh = lbh + 28 + t1h + 16 + t2h + 48 + row_h
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    d.text(((W - t1w) // 2, y), t1, font=mf, fill=WHITE);   y += t1h + 16
    d.text(((W - t2w) // 2, y), t2, font=mf, fill=AMBER);   y += t2h + 48
    cx = (W - chips_w) // 2
    for (chip, (cw, ch)), bw in zip(zip(chips, csz), cws):
        bh2 = ch + cpy*2; cy = y + (row_h - bh2)//2
        d.rounded_rectangle([cx, cy, cx+bw, cy+bh2], radius=99, fill=PANEL, outline=BORDER, width=1)
        d.text((cx + cpx, cy + cpy), chip, font=cf, fill=(209,213,219))
        cx += bw + cgap
    return im

def s13():
    """TRAP"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, sf = f(26), f(74), f(38)
    lbt = "落とし穴"; lbw, lbh = sz(d, lbt, lbf)
    l1 = "数字が現実を映す"
    l2 = "鏡だと思い込む"
    l1w, l1h = sz(d, l1, mf); l2w, l2h = sz(d, l2, mf)
    sub_lines = ["数字の作られ方を知らないまま受け取ると", "議論の地に足がつかなくなる"]
    ssz = [sz(d, s, sf) for s in sub_lines]
    sh = sum(h for _, h in ssz) + 12
    bh = lbh + 28 + l1h + 16 + l2h + 32 + sh
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    d.text(((W - l1w) // 2, y), l1, font=mf, fill=WHITE);   y += l1h + 16
    d.text(((W - l2w) // 2, y), l2, font=mf, fill=AMBER);   y += l2h + 34
    for (line, (lw, lh)) in zip(sub_lines, ssz):
        d.text(((W - lw) // 2, y), line, font=sf, fill=GRAY); y += lh + 12
    return im

def s14():
    """WHY 85"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, sf = f(26), f(100), f(38)
    lbt = "問えるかどうか"; lbw, lbh = sz(d, lbt, lbf)
    pre = "なぜ "; acc = "85"; end = " なのか"
    pw, ph = sz(d, pre, mf); aw, ah = sz(d, acc, mf); ew, _ = sz(d, end, mf)
    sub_lines = ["なぜ 80 ではなく", "なぜ 90 でもなく——85 なのか",
                 "", "その根拠を問えることが", "統計リテラシーの核心にある"]
    ssz = [sz(d, s, sf) if s else (0, 22) for s in sub_lines]
    sh = sum(h for _, h in ssz) + 10*(len(sub_lines)-1)
    bh = lbh + 28 + ah + 40 + sh
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    tw = pw + aw + ew; x = (W - tw) // 2
    d.text((x, y), pre, font=mf, fill=WHITE)
    d.text((x + pw, y), acc, font=mf, fill=AMBER)
    d.text((x + pw + aw, y), end, font=mf, fill=WHITE);     y += ah + 44
    for (line, (lw, lh)) in zip(sub_lines, ssz):
        if line:
            d.text(((W - lw) // 2, y), line, font=sf, fill=GRAY)
        y += lh + 10
    return im

def s15():
    """THE QUESTION box"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, qf = f(26), f(56)
    lbt = "数字を見たときに持つべき問い"; lbw, lbh = sz(d, lbt, lbf)
    q_lines = ["この数字は", "何をどう定義した結果か？"]
    qsz = [sz(d, l, qf) for l in q_lines]
    qpad = 52
    box_w = max(w for w, _ in qsz) + qpad * 2
    box_h = sum(h for _, h in qsz) + 18 + qpad * 2
    bh = lbh + 36 + box_h
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 36
    bx = (W - box_w) // 2
    d.rounded_rectangle([bx, y, bx+box_w, y+box_h], radius=16, fill=(10,8,2), outline=AMBER, width=2)
    ty = y + qpad
    for line, (lw, lh) in zip(q_lines, qsz):
        if "定義" in line:
            pre2, _, rest = line.partition("定義")
            p2w, _ = sz(d, pre2, qf); dw, _ = sz(d, "定義", qf); rw, _ = sz(d, rest, qf)
            total = p2w + dw + rw; x0 = bx + (box_w - total) // 2
            d.text((x0, ty), pre2, font=qf, fill=WHITE)
            d.text((x0 + p2w, ty), "定義", font=qf, fill=AMBER)
            d.text((x0 + p2w + dw, ty), rest, font=qf, fill=WHITE)
        else:
            d.text((bx + (box_w - lw) // 2, ty), line, font=qf, fill=WHITE)
        ty += lh + 18
    return im

def s16():
    """CONCLUSION"""
    im = add_glow(new_img(), intensity=0.07)
    d = ImageDraw.Draw(im)
    mf = f(90)
    lines = [("数値は先に", "こない"), ("定義が先に", "ある")]
    sizes = [(sz(d, pre, mf), sz(d, acc, mf)) for pre, acc in lines]
    bh = sum(ph for (_, ph), _ in sizes) + 22
    y  = (H - bh) // 2
    for (pre, acc), ((pw, ph), (aw, _)) in zip(lines, sizes):
        tw = pw + aw; x = (W - tw) // 2
        d.text((x, y), pre, font=mf, fill=WHITE)
        d.text((x + pw, y), acc, font=mf, fill=AMBER)
        y += ph + 22
    return im

def s17():
    """OUTRO"""
    im = new_img()
    d = ImageDraw.Draw(im)
    lbf, mf, cf = f(26), f(62), f(36)
    lbt = "おわりに"; lbw, lbh = sz(d, lbt, lbf)
    mt_lines = ["統計の見方が変わると", "社会の議論の見え方も変わる"]
    mtsz = [sz(d, l, mf) for l in mt_lines]
    mt_h = sum(h for _, h in mtsz) + 16
    card_lines = [
        ("チャンネル登録・高評価", WHITE),
        ("よろしくお願いします", WHITE),
        ("", None),
        ("kiyo-field-notes.vercel.app", DARK_G),
    ]
    csz = [(sz(d, t, cf) if t else (0, 20)) for t, _ in card_lines]
    ci_h = sum(h for _, h in csz) + 10*(len(card_lines)-1)
    cpad = 38; cw = 700; card_h = ci_h + cpad*2
    gap = 44
    bh = lbh + 28 + mt_h + gap + card_h
    y  = (H - bh) // 2
    d.text(((W - lbw) // 2, y), lbt, font=lbf, fill=AMBER); y += lbh + 28
    for (text, (tw, th)) in zip(mt_lines, mtsz):
        col = AMBER if "見え方" in text else WHITE
        d.text(((W - tw) // 2, y), text, font=mf, fill=col); y += th + 16
    y += gap
    bx = (W - cw) // 2
    d.rounded_rectangle([bx, y, bx+cw, y+card_h], radius=14, fill=PANEL, outline=BORDER, width=1)
    ty = y + cpad
    for (text, col), (tw, th) in zip(card_lines, csz):
        if text and col:
            d.text((bx + (cw - tw) // 2, ty), text, font=cf, fill=col)
        ty += th + 10
    return im

# ── Sequence (slide_fn, hold_secs) ───────────────────────────
SLIDES = [
    (s01, 5), (s02, 6), (s03, 8), (s04, 7), (s05, 5),
    (s06, 5), (s07, 8), (s08, 6), (s09, 10), (s10, 7),
    (s11, 9), (s12, 8), (s13, 8), (s14, 9), (s15, 9),
    (s16, 8), (s17, 10),
]
FADE = 15  # frames (0.5 sec)

# ── Main ──────────────────────────────────────────────────────
def main():
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "pipe:0",
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", "-preset", "fast",
        str(OUT)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    print("Rendering slides...")
    images = []
    for i, (fn, _) in enumerate(SLIDES):
        sys.stdout.write(f"  [{i+1}/{len(SLIDES)}] {fn.__name__}\n")
        sys.stdout.flush()
        images.append(np.array(fn()))

    print("Writing video...")
    for i, (arr, (_, hold)) in enumerate(zip(images, SLIDES)):
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
    mb = OUT.stat().st_size / 1024 / 1024
    print(f"\nDone: {OUT}\nSize: {mb:.1f} MB")

if __name__ == "__main__":
    main()
