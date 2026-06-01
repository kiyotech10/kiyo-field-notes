#!/usr/bin/env python3
"""
MP4生成: 看護師の将来性と入学者数の推移【2025年版】
Usage: python3 make_video_nursing_future.py
Output: nursing-future-outlook.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "nursing-future-outlook.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "データで見る",
        "line1": "看護師の",
        "accent": "将来性",
        "sub": "感覚ではなく政府統計から読む【2025年版】",
        "hold": 6,
    },
    {
        "type": "SECTION",
        "number": "DATA 1",
        "title": "就業者数の推移",
        "sub": "厚労省「衛生行政報告例」より",
        "hold": 5,
    },
    {
        "type": "TABLE",
        "label": "看護師 就業者数推移（准看護師除く）",
        "headers": ["年", "就業者数"],
        "rows": [
            ["2010年", "約95万人"],
            ["2016年", "約116万人"],
            ["2020年", "約128万人"],
            ["2022年", "約133万人"],
            ["2024年（推計）", "約138万人"],
        ],
        "accent_col": 1,
        "hold": 9,
    },
    {
        "type": "BIG_TEXT",
        "pre": "10年で",
        "accent": "+43万人",
        "sub": "一貫して増加——現在は約135〜140万人規模",
        "font_size": 130,
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "DATA 2",
        "title": "入学者数の推移",
        "sub": "就業者数とは逆の傾向が……",
        "hold": 5,
    },
    {
        "type": "TABLE",
        "label": "看護師等養成所 入学者数",
        "headers": ["年度", "入学者数"],
        "rows": [
            ["2010年度", "約55,000人"],
            ["2015年度", "約59,000人（ピーク）"],
            ["2020年度", "約57,000人"],
            ["2024年度（推計）", "約53,000人"],
        ],
        "accent_col": 1,
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "逆の構造",
        "lines": [
            {"pre": "就業者数：", "accent": "増加中", "post": ""},
            {"pre": "入学者数：", "accent": "減少中", "post": ""},
        ],
        "sub": "少子化による18歳人口の減少——この「ズレ」が供給不足を生み出す",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "DATA 3",
        "title": "2040年までの需給見通し",
        "sub": "厚労省・看護職員需給分科会（2040年まで推計）",
        "hold": 5,
    },
    {
        "type": "TABLE",
        "label": "需給ギャップ予測（看護職員全体）",
        "headers": ["時期", "需要", "供給", "不足数"],
        "rows": [
            ["2025年", "約188万人", "175〜182万人", "最大13万人"],
            ["2030年", "約196万人", "178〜185万人", "最大18万人"],
            ["2040年", "約202万人", "175〜183万人", "最大27万人"],
        ],
        "accent_col": 3,
        "hold": 10,
    },
    {
        "type": "QUOTE",
        "label": "厚労省の公式見解",
        "quote_lines": [
            "看護師は",
            "「絶対的に不足する職種」",
        ],
        "accent_word": "絶対的に不足する",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "評価",
        "title": "将来性の4つの観点",
        "sub": "需要・供給・待遇・AIの影響",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "総合評価",
        "items": [
            {"num": "①", "text": "需要面：非常に強い", "sub": "後期高齢者2200万人時代——病院・在宅・介護全方位で需要増"},
            {"num": "②", "text": "供給面：懸念あり", "sub": "入学者減少→2030年代に養成所の定員割れが深刻化か"},
            {"num": "③", "text": "待遇：改善中", "sub": "処遇改善補助金が継続——まだ道半ばだが方向は正しい"},
            {"num": "④", "text": "AIの影響：小さい", "sub": "身体的ケア・関係構築はAI代替が困難——安定した雇用が続く"},
        ],
        "hold": 11,
    },
    {
        "type": "STATEMENT",
        "label": "視点の転換",
        "lines": [
            {"pre": "「安定してるから」", "accent": "ではなく", "post": ""},
            {"pre": "「構造的に必要とされる——", "accent": "だから力を磨く", "post": "」"},
        ],
        "sub": "需要があるということは、質への期待も高まるということ",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "日本で", "accent": "最も将来性が高い", "post": "職種のひとつ"},
            {"pre": "不足が拡大する中で", "accent": "専門性が価値になる", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "数字で見れば明らか——",
            "看護師のキャリアを磨く意味がある",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
