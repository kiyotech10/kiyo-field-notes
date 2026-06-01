#!/usr/bin/env python3
"""
MP4生成: TOEIC 905点。でも「英語ができる」は目的じゃない
Usage: python3 make_video_toeic.py
Output: toeic-905.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "toeic-905.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "TOEIC スコア",
        "accent": "905点",
        "line2": "でも目的じゃない",
        "sub": "スコアの先にあるものを問う",
        "hold": 6,
    },
    {
        "type": "TABLE",
        "label": "結果",
        "headers": ["パート", "スコア"],
        "rows": [
            ["Listening", "480"],
            ["Reading", "425"],
            ["合計", "905点"],
        ],
        "accent_col": 1,
        "hold": 7,
    },
    {
        "type": "STATEMENT",
        "label": "一晩経って気づいた",
        "lines": [
            "スコアが上がっても",
            {"pre": "英語で", "accent": "何かができるようになった", "post": ""},
            "わけじゃない",
        ],
        "hold": 8,
    },
    {
        "type": "BIG_TEXT",
        "accent": "英語は道具だ",
        "sub": "ハンマーを持っていること自体に価値はない——何を打つかだけが問題",
        "font_size": 100,
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "問い",
        "title": "看護師として英語で何ができるか",
        "sub": "道具の使い道を明確にする",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "英語が使えると広がる世界",
        "items": [
            {"num": "①", "text": "英語の医療論文を読む", "sub": "最新エビデンスに直接アクセスできる"},
            {"num": "②", "text": "外国人患者と話す", "sub": "多様な患者背景に対応できる"},
            {"num": "③", "text": "海外学会・研修に参加", "sub": "グローバルな医療知識をアップデート"},
            {"num": "④", "text": "英語圏でのキャリア", "sub": "選択肢そのものが広がる"},
        ],
        "hold": 10,
    },
    {
        "type": "COMPARE",
        "label": "よくある落とし穴",
        "left_label": "NG：順番が逆",
        "left_items": ["まず英語を仕上げる", "完璧になったら使う", "いつまでも「準備中」", "スコアが目的になる"],
        "right_label": "OK：目的が先",
        "right_items": ["やりたいことを決める", "必要な英語を学ぶ", "使いながら伸ばす", "スコアは通過点"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "問いを逆にする",
        "quote_lines": [
            "「英語で何をしたいか」を先に決め",
            "そのために必要な英語を学ぶ",
        ],
        "accent_word": "先に決め",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "実践",
        "title": "論文を読む習慣の作り方",
        "sub": "ハードルを下げれば続けられる",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "今日からできること",
        "items": [
            "PubMedでキーワード検索——アブストラクトだけ読む",
            "週1回、英語の投稿をSNSにする",
            "オンライン英会話で月4回話す",
            "英語日記を3行から始める",
        ],
        "sub": "「完璧な英語」でなくていい。使い続けることが力になる",
        "hold": 9,
    },
    {
        "type": "TABLE",
        "label": "目的別 × 伸ばすべき英語",
        "headers": ["目的", "優先すべきスキル"],
        "rows": [
            ["論文を読む", "読解力（Academic Reading）"],
            ["外国人患者と話す", "聴解・会話（Medical English）"],
            ["学会発表", "発表英語・Q&A対応"],
            ["海外就職", "IELTS / OET 取得"],
        ],
        "accent_col": 1,
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "905点の先へ",
        "lines": [
            {"pre": "「英語が", "accent": "できる人", "post": "」より"},
            {"pre": "「英語を使って", "accent": "何かをしている人", "post": "」へ"},
        ],
        "sub": "スコアは、そのための資格確認でしかない",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "スコアは", "accent": "手段", "post": ""},
            {"pre": "目的は", "accent": "英語で何をするか", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "問いを持って学ぶとき",
            "英語は力になる",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
