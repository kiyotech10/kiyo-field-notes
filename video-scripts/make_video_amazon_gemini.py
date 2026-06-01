#!/usr/bin/env python3
"""
MP4生成: AmazonとGeminiで、気になる本の中身を無料でのぞく方法
Usage: python3 make_video_amazon_gemini.py
Output: amazon-gemini-book-preview.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "amazon-gemini-book-preview.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "本の選び方",
        "line1": "気になる本の中身を",
        "accent": "無料でのぞく",
        "sub": "Amazon ＋ Chrome Gemini を使った実践テクニック",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "こんな経験ない？",
        "lines": [
            "目次だけでは判断がつかない……",
            {"pre": "「第3章が気になるけど、", "accent": "自分に合う内容？", "post": "」"},
        ],
        "sub": "買ってから「思ってたのと違った」——これを防ぐ方法がある",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "方法",
        "title": "たった3ステップ",
        "sub": "追加コスト一切なし",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "やり方",
        "items": [
            {"num": "①", "text": "Amazonで本の商品ページを開く", "sub": "レビュー・目次が充実しているページほどよい"},
            {"num": "②", "text": "ChromeのGemini機能を起動", "sub": "サイドパネルから——ページの内容をAIが読み込む"},
            {"num": "③", "text": "「ネタバレ」と入力して送信", "sub": "各章のポイントをまとめて教えてくれる"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "実例",
        "title": "実際に試してみた",
        "sub": "「2034 未来予測——AIのいる明日」",
        "hold": 5,
    },
    {
        "type": "QUOTE",
        "label": "Geminiが返した内容（例）",
        "quote_lines": [
            "Chapter1：AIによる死生観のリセット",
            "——故人AIの日常化、亡くなった家族をAIとして",
            "再現し対話を続けることが当たり前になる世界",
        ],
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "わかること",
        "lines": [
            {"pre": "本の", "accent": "全体像", "post": "がつかめる"},
            {"pre": "「気になる部分が", "accent": "本当に書いてある？", "post": "」がわかる"},
        ],
        "sub": "購入前に内容を確認できる——買い失敗を大幅に減らせる",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "応用",
        "title": "「ネタバレ」以外の使い方",
        "sub": "質問を工夫するとさらに精度が上がる",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "使える質問例",
        "items": [
            "「この本の第3章の要点は？」",
            "「著者が最も言いたいことは何？」",
            "「この本は初心者に向いている？」",
            "「似た本と比べて何が違う？」",
        ],
        "sub": "具体的に聞くほど、精度が上がる",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "ポイント",
        "title": "精度を上げるコツ",
        "sub": "Amazonページの充実度が鍵",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "精度が上がる条件",
        "items": [
            "目次が詳しく掲載されているページ",
            "「商品説明」が充実している本",
            "著者情報・推薦文が多いページ",
            "レビューが豊富（内容紹介を含む）",
        ],
        "sub": "GeminiはAmazonページ上の情報を使う——ページが充実していれば回答も詳しくなる",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "注意点",
        "lines": [
            {"pre": "「買わない」道具ではなく", "accent": "", "post": ""},
            {"pre": "「買うべき本を", "accent": "見極める", "post": "」道具"},
        ],
        "sub": "興味が持てたら——ぜひ本を手にとってほしい",
        "hold": 8,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "Amazon ＋ Chrome Gemini ＋ 「", "accent": "ネタバレ", "post": "」"},
            {"pre": "これだけで", "accent": "買う前に中身を確認", "post": "できる"},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "積読を増やす前に",
            "一度試してみてほしい",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
