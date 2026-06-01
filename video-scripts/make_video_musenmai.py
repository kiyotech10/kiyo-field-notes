#!/usr/bin/env python3
"""
MP4生成: 無洗米と普通のお米、コスパは実は同じ？
Usage: python3 make_video_musenmai.py
Output: musenmai-cospa.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "musenmai-cospa.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "お米の話",
        "line1": "「無洗米は",
        "accent": "割高だ」",
        "line2": "は思い込みだった",
        "sub": "コスパを正しく計算すると——答えが変わる",
        "hold": 6,
    },
    {
        "type": "BIG_TEXT",
        "pre": "実は",
        "accent": "コスパほぼ同じ",
        "sub": "計算方法を知れば、「無洗米は高い」という思い込みが消える",
        "font_size": 100,
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "なぜ？",
        "title": "研ぐと量が減る",
        "sub": "この事実を知っている人は意外と少ない",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "普通のお米の真実",
        "lines": [
            "研ぐと——ぬか・表面の米粒が",
            {"pre": "", "accent": "水と一緒に流れていく", "post": ""},
        ],
        "sub": "研いだあとの量は、研ぐ前より少なくなる",
        "hold": 8,
    },
    {
        "type": "BIG_TEXT",
        "pre": "重量が",
        "accent": "5〜10%",
        "post": "減る",
        "sub": "5kgのお米を研ぐと、4.5〜4.75kgになっている",
        "font_size": 130,
        "hold": 8,
    },
    {
        "type": "TABLE",
        "label": "コスパ比較",
        "headers": ["", "普通のお米", "無洗米"],
        "rows": [
            ["研ぎの手間", "あり", "なし"],
            ["研いだ後の量", "5〜10%減る", "そのまま"],
            ["水の使用量", "多い（数回分）", "少ない"],
            ["実質コスパ", "表示より割高", "表示通り"],
        ],
        "accent_col": 2,
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "4つの理由",
        "title": "コメマイスターが推す根拠",
        "sub": "お米のプロが無洗米を選ぶ理由",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "コメマイスターが無洗米を推す理由",
        "items": [
            {"num": "①", "text": "栄養価が保たれる", "sub": "専用処理でぬかを除去——必要な栄養はしっかり残る"},
            {"num": "②", "text": "味が安定する", "sub": "研ぎムラなし——誰が炊いても均一な仕上がり"},
            {"num": "③", "text": "節水・時短になる", "sub": "研ぎ水不要——忙しい朝にも嬉しい"},
            {"num": "④", "text": "環境にやさしい", "sub": "とぎ汁を排水に流さない——河川への負荷が減る"},
        ],
        "hold": 11,
    },
    {
        "type": "SECTION",
        "number": "追加情報",
        "title": "もっとおいしく炊くコツ",
        "sub": "無洗米ならではのポイント",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "無洗米をさらにおいしく炊く",
        "items": [
            "水の量を通常より5%ほど多めに",
            "炊く前に30分〜1時間浸水させる",
            "炊き上がり後15分はふたを開けない",
            "余裕があればミネラルウォーターで炊く",
        ],
        "sub": "少しの工夫でクオリティが大きく上がる",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "「においが気になる」への回答",
        "lines": [
            {"pre": "製法による特性——", "accent": "炊き方で改善できる", "post": ""},
            "多くの場合、慣れると気にならなくなる",
        ],
        "sub": "最初は違和感があっても、米の種類を変えると解消することが多い",
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "label": "節水効果（参考）",
        "quote_lines": ["普通のお米（4合分）の研ぎ水は", "平均で約1〜1.5リットル", "無洗米なら——ゼロ"],
        "accent_word": "ゼロ",
        "hold": 8,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "無洗米 ＝ ", "accent": "コスパ同じ", "post": ""},
            {"pre": "＋ ", "accent": "手間なし", "post": " ＋ 味安定 ＋ 環境"},
        ],
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "lines": [
            "「無洗米は高い」は",
            {"pre": "", "accent": "計算の落とし穴", "post": "だった"},
        ],
        "sub": "次のお米を選ぶとき——無洗米を試してみてはどうだろう",
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "小さな見直しが",
            "家計と環境を変える",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
