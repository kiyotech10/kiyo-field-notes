#!/usr/bin/env python3
"""
MP4生成: PayPayクレジットは、事前にPayPayマネーで支払いができる
Usage: python3 make_video_paypay.py
Output: paypay-credit-prepay.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "paypay-credit-prepay.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "PayPay 活用術",
        "line1": "クレジットなのに",
        "accent": "今すぐ支払える",
        "sub": "PayPayクレジット「事前支払い」機能の全解説",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "こんな不安ない？",
        "lines": [
            "「今月いくら使ったっけ……」",
            {"pre": "「口座残高が", "accent": "足りるか不安", "post": "……」"},
        ],
        "sub": "クレジット払いの「宙に浮いている感覚」——解消できる機能がある",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "機能紹介",
        "title": "PayPayクレジット「事前支払い」",
        "sub": "引き落とし日を待たずに払える",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "事前支払いとは",
        "lines": [
            "PayPayマネーで",
            {"pre": "好きなタイミングに", "accent": "支払いを済ませる", "post": ""},
        ],
        "sub": "引き落とし日を待たなくていい——その場でクレジット残高が減る",
        "hold": 8,
    },
    {
        "type": "LIST",
        "label": "手順（3ステップ）",
        "items": [
            {"num": "①", "text": "PayPayアプリを開く", "sub": "クレジット管理画面に移動"},
            {"num": "②", "text": "「支払い金額調整」をタップ", "sub": "支払いたい金額を入力"},
            {"num": "③", "text": "PayPayマネーで支払う", "sub": "即時にクレジット残高が減る"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "活用シーン",
        "title": "こんなときに使うと便利",
        "sub": "3つのタイミング",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "活用シーン",
        "items": [
            {"num": "①", "text": "大きな買い物をした直後", "sub": "家電・旅行——翌月の引き落とし額を気にしなくて済む"},
            {"num": "②", "text": "月末に残高が不安なとき", "sub": "PayPayマネーで先に充当——引き落とし失敗を防げる"},
            {"num": "③", "text": "使いすぎを防ぎたいとき", "sub": "事前払いで「使った実感」が生まれる——支出管理が楽になる"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "重要",
        "title": "ポイントはちゃんとつく",
        "sub": "事前払いしても損しない",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "安心ポイント",
        "lines": [
            {"pre": "事前払いをしても", "accent": "PayPayポイントは付与", "post": "される"},
        ],
        "sub": "ポイントを稼ぎながら、支払いは自分のペースで——これがPayPayクレジットの便利さ",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "なぜ知られていない？",
        "title": "「後払い」の思い込み",
        "sub": "発想の転換が必要",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "気づきにくい理由",
        "lines": [
            "「クレジット ＝ 後で払う」という固定観念",
            {"pre": "「", "accent": "前払いできる", "post": "」という発想が浮かびにくい"},
        ],
        "sub": "でも実際には——この機能があることで心理的ストレスが大きく減る",
        "hold": 8,
    },
    {
        "type": "BULLET",
        "label": "家計管理が楽になる理由",
        "items": [
            "「今いくら使ったか」が常にわかる",
            "引き落とし日のドキドキがなくなる",
            "口座残高との突合が不要",
            "使い過ぎを「その場で」止められる",
        ],
        "sub": "キャッシュレス生活を送るなら——支払いコントロール機能を活用しよう",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "PayPayクレジット ＋", "accent": "事前支払い", "post": ""},
            {"pre": "引き落とし日を待たず、好きなタイミングで", "accent": "払えて", "post": ""},
            {"pre": "", "accent": "ポイントもちゃんとつく", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "クレジット払いの不安を",
            "事前払いで解消しよう",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
