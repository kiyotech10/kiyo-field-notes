#!/usr/bin/env python3
"""
MP4生成: 「行動最適化」が奪うもの——医療の余白は、無駄ではない
Usage: python3 make_video_ehr.py
Output: ehr-optimization.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "ehr-optimization.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "医療DXへの問い",
        "line1": "「行動最適化」が",
        "accent": "奪うもの",
        "sub": "医療の余白は、無駄ではない",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "ニュース",
        "lines": [
            "都立墨東病院が",
            {"pre": "電子カルテ", "accent": "「行動最適化支援」", "post": "を"},
            "億単位の予算で導入",
        ],
        "sub": "どの操作が非効率か分析し、医療者の動きを最適化する——悪くない試みだ",
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "label": "でも、問いたい",
        "quote_lines": [
            "それは",
            "何を生み出すのか",
        ],
        "accent_word": "何を生み出すのか",
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "構造の問題",
        "title": "効率化の恩恵が見えにくい",
        "sub": "医療は民間企業とは違う",
        "hold": 5,
    },
    {
        "type": "COMPARE",
        "label": "民間企業 vs 医療",
        "left_label": "民間企業の効率化",
        "left_items": ["コストが下がる", "利益が増える", "価格競争力がつく", "効果が数字で返る"],
        "right_label": "医療の効率化",
        "right_items": ["診療報酬は変わらない", "患者の負担額も変わらない", "恩恵の行き先が不明確", "何のための効率化？"],
        "highlight": "left",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "「空いた時間」の使い道——誰も答えていない",
        "items": [
            "患者数を増やすのか？",
            "スタッフを削減するのか？",
            "その時間で「別の何か」をするのか？",
        ],
        "sub": "億単位の投資に対して、「何を変えるか」が明確に定義されているか疑問だ",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "本質的な問題",
        "title": "削られる「余白」",
        "sub": "効率化が進んだとき、何が消えるか",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "現場の実感",
        "lines": [
            "生まれた時間は——",
            {"pre": "次のタスクで", "accent": "埋められる", "post": ""},
        ],
        "sub": "ベッドサイドに立てる時間が増えるのではなく——こなせる業務量の基準が上がる",
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "label": "静かに削られていくもの",
        "lines": [
            {"pre": "それが——", "accent": "「余白」", "post": ""},
        ],
        "sub": "処置と処置のあいだの、わずかな時間",
        "hold": 7,
    },
    {
        "type": "SECTION",
        "number": "余白の価値",
        "title": "記録に残らないケア",
        "sub": "数字には現れないが、機能している",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "「余白」の中で起きること",
        "items": [
            "「なんか今日は顔色が違う」という気づき",
            "廊下での会話——「昨日から食べていない」という情報",
            "ちょっとした患者の変化に気づける観察",
            "家族からの些細な言葉の中にある重要情報",
        ],
        "sub": "記録には残らない——でも急変を防いだり、退院後の生活を変えたりすることがある",
        "hold": 10,
    },
    {
        "type": "QUOTE",
        "label": "看護の本質",
        "quote_lines": [
            "タスクの隙間にある観察と対話が",
            "ケアの本質に近い場所に",
            "あることがある",
        ],
        "accent_word": "ケアの本質",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "問われていないこと",
        "lines": [
            "「何を最適化するか」が",
            {"pre": "", "accent": "問われていない", "post": "まま進んでいる"},
        ],
        "sub": "患者のアウトカム？ 医療者の疲弊？ それとも数字上のスループット？",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "改善すべき本物の非効率（改善してよい）",
        "items": [
            "重複入力・転記作業",
            "同じ情報を何度も探す非効率",
            "紙とデジタルの混在",
            "ナースコールへの移動の重複",
        ],
        "sub": "これらは本当に改善すべき——目的を明確にしたDXは意味がある",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "余白は", "accent": "削っていい無駄ではない", "post": ""},
            {"pre": "そこに", "accent": "数字で測れないケア", "post": "が宿る"},
        ],
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "quote_lines": [
            "「速くなった」ではなく",
            "「患者に何が返ったか」で評価できるか",
        ],
        "accent_word": "患者に何が返ったか",
        "hold": 9,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "効率化の目的を問い続ける",
            "ケアの本質を守り抜く",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
