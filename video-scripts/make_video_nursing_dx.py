#!/usr/bin/env python3
"""
MP4生成: 令和8年度改定 医療DXによる急性期看護配置基準の柔軟化
Usage: python3 make_video_nursing_dx.py
Output: nursing-dx-medical-fee.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "nursing-dx-medical-fee.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "令和8年度 診療報酬改定",
        "line1": "医療DXで",
        "accent": "看護配置が変わる",
        "sub": "急性期7対1基準の柔軟化——現場への影響を解説",
        "hold": 6,
    },
    {
        "type": "SECTION",
        "number": "基礎知識",
        "title": "7対1看護とは",
        "sub": "急性期一般入院料1の基本要件",
        "hold": 5,
    },
    {
        "type": "STATEMENT",
        "label": "従来の基準",
        "lines": [
            {"pre": "患者", "accent": "7人", "post": "に対して"},
            {"pre": "看護師", "accent": "1人以上", "post": "の配置"},
        ],
        "sub": "これが「7対1看護」——高い看護配置が必要な急性期病棟の基準",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "今回の変更",
        "title": "ICT導入で9割配置が認められる",
        "sub": "2026年度改定の新しい特例",
        "hold": 5,
    },
    {
        "type": "TABLE",
        "label": "配置基準の変化",
        "headers": ["項目", "従来の基準", "医療DX特例"],
        "rows": [
            ["看護配置人数", "7対1相当", "通常の9割（約7.7対1）"],
            ["入院基本料", "基準未満で減算", "減算なし（7対1を維持）"],
            ["ICT要件", "なし", "指定3分野のツール運用"],
            ["残業時間要件", "なし", "常勤看護師 月平均10時間以下"],
        ],
        "accent_col": 2,
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "ICT要件",
        "title": "3つの必須ツール",
        "sub": "すべて導入・活用していることが条件",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "算定要件となる3分野のICT機器",
        "items": [
            {"num": "①", "text": "見守り機器", "sub": "転倒転落センサー——不要な訪室を減らし安全を確保"},
            {"num": "②", "text": "看護記録の効率化ツール", "sub": "音声入力・バイタル自動転送——転記・手入力を削減"},
            {"num": "③", "text": "情報共有の迅速化ツール", "sub": "インカム・スマホ連絡——緊急時の応援要請を即座に"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "現場への影響",
        "title": "課題と展望",
        "sub": "看護師から見た率直な評価",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "現場の課題",
        "items": [
            {"num": "①", "text": "直接ケアのマンパワー", "sub": "食事・排泄介助は減らせない——9割体制での質の維持が課題"},
            {"num": "②", "text": "導入初期の学習コスト", "sub": "新機器への習熟期間——一時的に業務負荷が増える"},
            {"num": "③", "text": "夜勤帯の安全確保", "sub": "少人数でどこまで安全に運用できるか"},
        ],
        "hold": 10,
    },
    {
        "type": "COMPARE",
        "label": "効率化の成果——どう使うか",
        "left_label": "懸念されるパターン",
        "left_items": ["空いた時間で業務量増加", "スタッフ削減の口実に", "「余白」が消える", "疲弊が悪化"],
        "right_label": "本来の目的",
        "right_items": ["直接ケアに集中できる", "残業・疲弊が減る", "患者観察の時間が増える", "ケアの質が上がる"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "この改定が意味すること",
        "lines": [
            "テクノロジーで間接業務を減らし",
            {"pre": "看護師が本来すべき", "accent": "直接ケアに集中", "post": "できる環境へ"},
        ],
        "sub": "人手不足の穴埋めではなく——DXで看護の価値を高める",
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "本質的なメッセージ",
        "quote_lines": [
            "医療DXは看護の仕事を奪わない",
            "看護師が「看護らしいこと」に",
            "集中できるための手段だ",
        ],
        "accent_word": "看護らしいこと",
        "hold": 9,
    },
    {
        "type": "BULLET",
        "label": "看護師に求められるスキル変化",
        "items": [
            "ICT機器を使いこなすデジタルリテラシー",
            "データから患者状態を読む判断力",
            "効率化した時間の使い方を設計する力",
            "変化する環境への適応力",
        ],
        "sub": "「道具」として使いこなす——難しくない",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "DXは", "accent": "看護の質を高める手段", "post": ""},
            {"pre": "問うべきは", "accent": "患者に何が返ったか", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "テクノロジーを味方に——",
            "看護の本質を守り抜く",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
