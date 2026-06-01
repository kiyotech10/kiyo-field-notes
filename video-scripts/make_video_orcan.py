#!/usr/bin/env python3
"""
MP4生成: オルカンで投資をはじめた。月10万円、夫婦で積み立てるだけ
Usage: python3 make_video_orcan.py
Output: orcan-invest.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "orcan-invest.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "投資の話",
        "line1": "オルカンで",
        "accent": "投資をはじめた",
        "sub": "月10万円、夫婦で積み立てるだけ",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "選んだもの",
        "lines": [
            "eMAXIS Slim 全世界株式",
            {"pre": "通称 ", "accent": "「オルカン」", "post": ""},
        ],
        "sub": "毎月10万円を自動積立。それだけ",
        "hold": 7,
    },
    {
        "type": "BULLET",
        "label": "やったこと——それだけ",
        "items": [
            "自動積立の設定をした",
            "リバランスはしない",
            "銘柄を調べない",
            "ニュースを見て売買しない",
        ],
        "sub": "「全世界の経済成長に乗っかる」——あとは時間に任せる",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "なぜ？",
        "title": "アクティブより インデックス",
        "sub": "データが示す結論",
        "hold": 5,
    },
    {
        "type": "COMPARE",
        "label": "アクティブ vs インデックス",
        "left_label": "アクティブファンド",
        "left_items": ["運用コストが高い", "長期でインデックスに勝てない", "銘柄選定が必要", "時間とエネルギーを消費"],
        "right_label": "インデックス（オルカン）",
        "right_items": ["業界最低水準のコスト", "長期で安定したリターン", "全世界に自動分散", "何もしなくていい"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "個別株について",
        "lines": [
            "企業分析・決算読み・タイミング——",
            {"pre": "その時間を", "accent": "仕事・副業に使う", "post": "ほうが"},
            "確実にリターンが出る",
        ],
        "sub": "市場を出し抜こうとするより、市場全体に乗るほうが再現性が高い",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "大切なこと",
        "title": "夫婦で認識を合わせる",
        "sub": "一人で決めると、下落時に崩れやすい",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "夫婦で決めたこと",
        "items": [
            {"num": "①", "text": "毎月いくら積み立てるか", "sub": "月10万円——生活費・貯金との割り振りを明確に"},
            {"num": "②", "text": "生活費との割り振り", "sub": "積立10万円 ＋ 貯金7万円でバランスを設定"},
            {"num": "③", "text": "「下がっても売らない」", "sub": "下落時に動じない——共通認識が精神的安定になる"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "複利",
        "title": "時間を味方につける力",
        "sub": "早く始めることが唯一の正解",
        "hold": 5,
    },
    {
        "type": "TABLE",
        "label": "複利シミュレーション（月10万円・年利5%）",
        "headers": ["期間", "元本", "運用後の資産"],
        "rows": [
            ["10年", "1,200万円", "約1,550万円"],
            ["20年", "2,400万円", "約4,100万円"],
            ["30年", "3,600万円", "約8,300万円"],
        ],
        "accent_col": 2,
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "複利の本質",
        "quote_lines": [
            "増えた分が次の元本になって",
            "さらに増える",
            "時間が長いほど、差が大きくなる",
        ],
        "accent_word": "時間が長いほど",
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "label": "オルカンを選んだ3つの理由",
        "lines": [
            {"pre": "① これ一本で", "accent": "世界中に分散", "post": ""},
            {"pre": "② 信託報酬が", "accent": "業界最低水準", "post": ""},
            {"pre": "③ ", "accent": "新NISA", "post": "の対象"},
        ],
        "hold": 8,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "オルカン毎月10万 ＋ 貯金7万", "accent": "", "post": ""},
            {"pre": "リバランスなし、", "accent": "余計なことをしない", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "quote_lines": [
            "シンプルにやることを絞るのが",
            "長続きのコツ",
        ],
        "accent_word": "長続きのコツ",
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "迷ったらシンプルに——",
            "オルカン一本で始めてみる",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
