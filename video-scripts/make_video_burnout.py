#!/usr/bin/env python3
"""
MP4生成: 頑張りすぎると病気になる——Utsuさんの活動休止と、自然に沿った生き方
Usage: python3 make_video_burnout.py
Output: burnout-natural-living.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "burnout-natural-living.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "BURNOUT",
        "line1": "頑張りすぎると",
        "accent": "病気になる",
        "sub": "Utsuさんの活動休止が教えてくれたこと",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "就活インフルエンサー",
        "lines": [
            {"pre": "Utsuさんが", "accent": "活動休止", "post": "した"},
        ],
        "sub": "自律神経不調——多くの若者に影響を与えてきた人物が倒れた",
        "hold": 7,
    },
    {
        "type": "QUOTE",
        "label": "一つの象徴",
        "quote_lines": ["「ああ、そうか」と思った", "頑張り続けることには、上限がある"],
        "accent_word": "上限がある",
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "PART 1",
        "title": "人生のネタバラシ文化",
        "sub": "情報が行動を加速させ、消耗を早める",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "SNSが公開する「攻略情報」",
        "items": [
            "就活・転職の攻略法",
            "給料の上げ方・交渉術",
            "FIRE達成の手順",
            "副業で稼ぐ方法",
        ],
        "sub": "本来なら自分で時間をかけて学ぶことが、次々と公開される",
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "lines": [
            "ネタバラシは行動を加速させる",
            {"pre": "加速した行動は", "accent": "消耗を早める", "post": ""},
        ],
        "sub": "情報を受け取った人は「わかった、じゃあやらなきゃ」と焦る",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "PART 2",
        "title": "体が先にアラームを出す",
        "sub": "メンタルより先に、体が悲鳴を上げる",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "体が出す赤信号",
        "items": [
            "なんか最近、眠れない",
            "胃が重い・食欲がない",
            "頭が働かない、集中できない",
            "休日でも疲れが取れない",
        ],
        "sub": "これらはすべて、自律神経が限界に近づいているサインだ",
        "hold": 9,
    },
    {
        "type": "BIG_TEXT",
        "accent": "頑張りすぎ",
        "post": "ることと",
        "sub": "体を壊すことは——思っていたより近い場所にある",
        "font_size": 110,
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "PART 3",
        "title": "自然に沿った生き方",
        "sub": "田舎暮らしの話ではない",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "人間の体の設計",
        "items": [
            {"num": "①", "text": "睡眠を削らない", "sub": "修復・記憶整理・免疫強化はすべて睡眠中に起こる"},
            {"num": "②", "text": "太陽のリズムに合わせる", "sub": "サーカディアンリズム——体内時計を整える"},
            {"num": "③", "text": "疲れたら休む", "sub": "「もう少し」が積み重なって限界を超える"},
            {"num": "④", "text": "お腹が空いたら食べる", "sub": "制限より「適切なタイミング」が大切"},
        ],
        "hold": 10,
    },
    {
        "type": "COMPARE",
        "label": "交感神経 vs 副交感神経",
        "left_label": "交感神経（アクセル）",
        "left_items": ["仕事・集中・緊張", "SNSチェック", "スマホを手放せない", "常に「何かしなきゃ」"],
        "right_label": "副交感神経（ブレーキ）",
        "right_items": ["休息・睡眠・回復", "散歩・入浴", "意識的なオフ時間", "「何もしない」時間"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "情報との付き合い方",
        "lines": [
            "受け取ったすべてを",
            {"pre": "", "accent": "すぐに実行しなくていい", "post": ""},
        ],
        "sub": "人生に「正解ルート」があるように見えても、それはあくまで誰かの地図だ",
        "hold": 8,
    },
    {
        "type": "BULLET",
        "label": "自分のペースを取り戻す",
        "items": [
            "毎朝すべての通知を確認しなくていい",
            "週に一度、SNSから離れる日を作る",
            "「今すぐやらなきゃ」という焦りに名前をつける",
            "自分の体力・ペース・季節を知る",
        ],
        "sub": "これは逃げではなく、長く走り続けるための戦略だ",
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "強さの定義",
        "quote_lines": ["強さとは、走り続けることではない", "立ち止まるべきときに", "立ち止まれること"],
        "accent_word": "立ち止まれること",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "頑張りすぎることは", "accent": "美徳ではない", "post": ""},
            {"pre": "人間は", "accent": "自然の一部", "post": "だ"},
        ],
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "lines": [
            "焦らず、でも止まらず。",
            {"pre": "そのくらいのテンポが", "accent": "長く走り続ける", "post": "コツ"},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "体の声を聞くことが",
            "長期的な強さにつながる",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
