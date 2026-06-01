#!/usr/bin/env python3
"""
MP4生成: 看護師こそ、「越境学習」が武器になる
Usage: python3 make_video_cross_boundary.py
Output: cross-boundary-learning.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "cross-boundary-learning.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "学び方の革命",
        "line1": "看護師こそ",
        "accent": "越境学習が武器",
        "sub": "異分野から学ぶことが、キャリアを最短で深く広くする",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "越境学習とは",
        "lines": [
            "自分の専門分野の外に出て",
            {"pre": "", "accent": "異なる分野から学ぶ", "post": "こと"},
        ],
        "sub": "ビジネス界で注目——看護においては「それ以上に」有効",
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "問題",
        "title": "「看護のための○○」だけで学ぶ落とし穴",
        "sub": "専門に絞ると「本質」を見逃す",
        "hold": 5,
    },
    {
        "type": "COMPARE",
        "label": "学び方の比較",
        "left_label": "看護専門の本",
        "left_items": ["わかりやすく編集済み", "すぐ使える", "でも——本質が削ぎ落とされている", "応用が効きにくい"],
        "right_label": "本家本元の分野の本",
        "right_items": ["深い理論・根拠がある", "遠回りに見える", "でも——応用が効く", "どこでも使えるフレームになる"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "例① キャリア",
        "title": "キャリア論の本家へ",
        "sub": "看護専用の本よりも、深い理解が得られる",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "読むべき「本家」キャリア論",
        "items": [
            "エドガー・シャイン「キャリアの錨」",
            "ハーズバーグの動機づけ理論",
            "マズローの欲求5段階説",
            "ドラッカー「プロフェッショナルの条件」",
        ],
        "sub": "「なぜ人は仕事に意味を見出すのか」「どんなときに燃え尽きるのか」が根本からわかる",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "フレームを持つと",
        "lines": [
            {"pre": "自分や同僚のキャリアが", "accent": "違う解像度", "post": "で見える"},
        ],
        "sub": "看護専用の視点より、普遍的な理論のほうが「現場を読む力」を与えてくれる",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "例② 統計",
        "title": "数学から学びなおす",
        "sub": "「p値がわからない」を根本から解決する",
        "hold": 5,
    },
    {
        "type": "COMPARE",
        "label": "統計の学び方",
        "left_label": "医療統計から入る",
        "left_items": ["公式を覚える", "「p<0.05が有意」だけわかる", "直感的な理解がない", "もやもやが残る"],
        "right_label": "数学・統計から入る",
        "right_items": ["確率・分布の直感がつく", "公式の意味が体感できる", "「なぜ」がわかる", "論文が深く読める"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "越境学習の他の例",
        "items": [
            "英語——看護英語より「英語そのもの」の勉強法",
            "マネジメント——看護管理より経営学・組織論の入門",
            "コミュニケーション——心理学・認知科学から学ぶ",
            "データ——統計学・データ分析の基礎から",
        ],
        "sub": "「看護専用」より「本家本元」に当たるほうが、深く広く活用できる",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "越境学習のパラドックス",
        "lines": [
            {"pre": "一見", "accent": "遠回り", "post": "に見えて"},
            {"pre": "最終的に", "accent": "最短コース", "post": "になる"},
        ],
        "sub": "本質から理解した知識は——状況が変わっても応用が効く",
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "越境学習の本質",
        "quote_lines": [
            "看護の教科書だけで看護を学ぶより",
            "違う分野の本棚を覗いたほうが",
            "看護がよく見える",
        ],
        "accent_word": "看護がよく見える",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "今日からできること",
        "items": [
            "興味のある「非医療系」の本を1冊選ぶ",
            "他学部・他業界の人と話す機会を作る",
            "看護以外の講義・動画を週1本見る",
            "「なぜ」を問いながら読む習慣を持つ",
        ],
        "sub": "「わくわくする」を基準に——義務感では続かない",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "専門特化の知識は", "accent": "すぐ使える", "post": ""},
            {"pre": "本家本元の知識は", "accent": "どこでも使える", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "違う分野の本棚を覗こう",
            "看護が、もっとよく見えるようになる",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
