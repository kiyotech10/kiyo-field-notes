#!/usr/bin/env python3
"""
MP4生成: 「適応」とは、逃げる力も含む——Xと検閲と、ダーウィンの誤解
Usage: python3 make_video_platform.py
Output: platform-adaptability.mp4
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from video_engine import render_video

OUT = Path(__file__).parent / "platform-adaptability.mp4"

SLIDES = [
    {
        "type": "HOOK",
        "label": "SNS時代の適応論",
        "line1": "「適応」とは",
        "accent": "逃げる力も含む",
        "sub": "Xと検閲と、ダーウィンの誤解",
        "hold": 6,
    },
    {
        "type": "STATEMENT",
        "label": "懐かしいTwitter",
        "lines": [
            "言論の自由と検閲のあいだで揺れながらも",
            {"pre": "「", "accent": "場の空気", "post": "」があったころ"},
        ],
        "sub": "完璧ではなかったが、荒らしやヘイトを抑える仕組みが機能していた",
        "hold": 8,
    },
    {
        "type": "QUOTE",
        "label": "有名な言葉——実は誤解がある",
        "quote_lines": [
            "「最も強い者が生き残るのではなく",
            "変化に適応できた者が生き残る」",
            "——ダーウィンの言葉として知られているが",
        ],
        "hold": 8,
    },
    {
        "type": "STATEMENT",
        "label": "実は……",
        "lines": [
            {"pre": "ダーウィン本人が", "accent": "書いていない", "post": ""},
            "19世紀の社会学者メギンソンの解釈が",
            "いつのまにかダーウィンの言葉に",
        ],
        "sub": "でも、内容自体は的を射ている——強さではなく、適応できるかどうか",
        "hold": 9,
    },
    {
        "type": "SECTION",
        "number": "現状",
        "title": "今のXで起きていること",
        "sub": "プラットフォームの設計が情報の質を決める",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "Xで起きているサイクル",
        "items": [
            "モデレーション緩和→荒らし・ヘイトが増える",
            "アルゴリズムが怒りを増幅する",
            "広告主が離れる",
            "ユーザーが疲弊する",
        ],
        "sub": "これは一時的な混乱ではなく、設計の問題だ",
        "hold": 9,
    },
    {
        "type": "STATEMENT",
        "label": "本当に懐かしいのは",
        "lines": [
            {"pre": "「管理されていたころ」ではなく", "accent": "", "post": ""},
            {"pre": "「", "accent": "場として機能していたころ", "post": "」"},
        ],
        "sub": "プラットフォームの品質は、ルールとアルゴリズムの設計で決まる",
        "hold": 8,
    },
    {
        "type": "SECTION",
        "number": "リスク",
        "title": "プラットフォーム依存の危うさ",
        "sub": "フォロワーはあなたの資産ではない",
        "hold": 5,
    },
    {
        "type": "LIST",
        "label": "特定プラットフォームに依存するリスク",
        "items": [
            {"num": "①", "text": "フォロワーはPFの資産", "sub": "サービス終了・凍結で一瞬にして失う"},
            {"num": "②", "text": "投稿は消える可能性", "sub": "サービス終了・ポリシー違反で削除される"},
            {"num": "③", "text": "ルールは一方的に変わる", "sub": "アルゴリズム変更でリーチが突然落ちる"},
        ],
        "hold": 10,
    },
    {
        "type": "SECTION",
        "number": "適応",
        "title": "「出ていく力」が適応力",
        "sub": "ダーウィン的な意味での適応",
        "hold": 5,
    },
    {
        "type": "BULLET",
        "label": "プラットフォーム時代の戦略",
        "items": [
            "自分のドメインでブログ・サイトを持つ",
            "メールリストを作る（誰にも奪われない資産）",
            "複数のSNSに分散させる",
            "「いつでも離れられる」状態を保つ",
        ],
        "sub": "これが長期的な強さになる",
        "hold": 9,
    },
    {
        "type": "COMPARE",
        "label": "依存 vs 自立",
        "left_label": "プラットフォーム依存",
        "left_items": ["1つのSNSに全集中", "アルゴリズムに振り回される", "ルール変更で動揺する", "「逃げられない」状態"],
        "right_label": "プラットフォーム自立",
        "right_items": ["複数チャネルを持つ", "自分のドメインが軸", "いつでも移動できる", "「出ていく力」がある"],
        "highlight": "right",
        "hold": 9,
    },
    {
        "type": "QUOTE",
        "label": "静かな適応力",
        "quote_lines": [
            "強さは、しがみつくことではなく",
            "次に行けることの中にある",
        ],
        "accent_word": "次に行けること",
        "hold": 9,
    },
    {
        "type": "CONCLUSION",
        "label": "まとめ",
        "lines": [
            {"pre": "適応とは", "accent": "移動できること", "post": ""},
            {"pre": "「出ていく力」が", "accent": "静かな強さ", "post": ""},
        ],
        "hold": 8,
    },
    {
        "type": "OUTRO",
        "message_lines": [
            "プラットフォームに依存しない",
            "発信の拠点を持とう",
        ],
        "hold": 10,
    },
]

if __name__ == "__main__":
    render_video(SLIDES, OUT)
