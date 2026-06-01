#!/usr/bin/env python3
"""
MP4生成: 「看護師になること」を目標にしてはいけない
Usage: python3 make_video_nursing_career.py
Output: nursing-career-beyond.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "nursing-career-beyond.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "看護キャリア論",
        "line1": "「看護師になること」を",
        "accent": "目標にするな",
        "sub": "免許取得はゴールではなく、スタートラインだ",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "よくある学生のゴール設定",
        "lines": [
            "入学 → 実習 → 国試 → 就職",
            {"pre": "それを", "accent": "「ゴール」", "post": "として走り切る"},
        ],
        "sub": "4年間全力で頑張った——でも、その先が真っ白になる",
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "label": "燃え尽き症候群の皮肉",
        "quote_lines": [
            "燃え尽き症候群は",
            "夢を叶えた人間にこそ",
            "起こる",
        ],
        "accent_word": "夢を叶えた",
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "label": "1年目のリアル",
        "lines": [
            {"pre": "「", "accent": "なんか思ってたのと違う", "post": "」"},
            {"pre": "「", "accent": "次に何を目指せばいいか", "post": "わからない」"},
        ],
        "sub": "これは偶然ではない——ゴール設定の問題だ",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "転換",
        "title": "問い方を変える",
        "sub": "「なりたい」→「何をしたいか」",
        "hold": 5,
    },
    {
        "type": "COMPARE",
        "label": "問いの違い",
        "left_label": "NG：なりたい",
        "left_items": ["看護師になりたい", "就職がゴール", "達成したら終わり", "40年が空白になる"],
        "right_label": "OK：何をしたいか",
        "right_items": ["看護師として何をしたいか", "就職はスタートライン", "問いが続く", "40年間を設計できる"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "看護師として何をしたいか——選択肢",
        "items": [
            "急性期で救命に携わる",
            "地域・在宅で暮らしを支える",
            "専門看護師・認定看護師を取って極める",
            "海外で働く・英語圏のキャリアを目指す",
            "管理職・教育者として後進を育てる",
        ],
        "sub": "「なってから考えればいい」ではなく——在学中に問い続けることで解像度が上がる",
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "大学4年間",
        "title": "訓練所ではなく、探索期間",
        "sub": "「看護師になる」ための4年間ではなく",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "実習で拾える情報",
        "lines": [
            {"pre": "「この領域が", "accent": "好き", "post": "」"},
            {"pre": "「この患者層が", "accent": "苦じゃない", "post": "」"},
            {"pre": "「この業務が", "accent": "向いてる気がする", "post": "」"},
        ],
        "sub": "感覚の断片が、卒業後のキャリアの核になる",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "「外へ出る」越境体験も有効",
        "items": [
            "病院ボランティア・見学実習",
            "他学部の講義を聴講する",
            "医療以外の業界でアルバイト",
            "社会人との交流・メンター探し",
        ],
        "sub": "異なる文脈に触れることで——「自分はどこに立ちたいか」が輪郭を持ち始める",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "免許について",
        "lines": [
            {"pre": "免許は強力な", "accent": "パスポート", "post": "だ"},
            "でも——どこへ行くかを決めるのは自分",
        ],
        "sub": "免許取得はゴールではなく、スタートラインに立てたということ",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "ロールモデル",
        "title": "40代でもキャリアを更新し続ける看護師",
        "sub": "共通点——免許を「手段」として見ていた",
        "hold": 5,
    },
    {
        "type": "QUOTE",
        "label": "キャリアの本質",
        "quote_lines": [
            "看護師になることを「手段」として",
            "もっと先にある何かを見ていた",
            "——それが、長く走り続ける人の共通点",
        ],
        "accent_word": "手段",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "看護師になることは", "accent": "出発点", "post": "だ"},
            {"pre": "問いを持ち続けることが", "accent": "エンジンになる", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "lines": [
            "看護師になること——出発点",
            {"pre": "そこからどこへ向かうかが", "accent": "本当の問い", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "免許の先に何があるか",
            "問い続けることがキャリアを作る",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
