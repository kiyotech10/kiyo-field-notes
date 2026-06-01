# 記事説明動画 インデックス

各記事に対応した動画制作スクリプト一覧です。目安尺は **5〜6分**（音声付き）。

---

## ファイル構成

```
video-scripts/
  video_engine.py              # 汎用スライド描画エンジン（全記事共通）
  add_voice_generic.py         # 汎用 TTS音声合成・動画合成スクリプト
  
  # 記事ごとのスライドスクリプト（python3 make_video_*.py で実行）
  make_video_burnout.py        # 頑張りすぎると病気になる
  make_video_musenmai.py       # 無洗米コスパ
  make_video_toeic.py          # TOEIC 905点
  make_video_platform.py       # 適応とは逃げる力も含む
  make_video_nursing_future.py # 看護師の将来性【2025版】
  make_video_nursing_dx.py     # 医療DX看護配置基準柔軟化
  make_video_orcan.py          # オルカン投資はじめた
  make_video_nursing_career.py # 看護師になることを目標にするな
  make_video_cross_boundary.py # 越境学習が武器になる
  make_video_ehr.py            # 行動最適化が奪うもの
  make_video_amazon_gemini.py  # Amazon+Geminiで本をのぞく
  make_video_paypay.py         # PayPayクレジット事前払い
  
  # 音声ナレーションスクリプト（録音時の読み上げ原稿）
  burnout-natural-living-voice.md
  musenmai-cospa-voice.md
  toeic-905-voice.md
  platform-adaptability-voice.md
  nursing-future-outlook-voice.md
  nursing-dx-medical-fee-voice.md
  orcan-invest-voice.md
  nursing-career-beyond-voice.md
  cross-boundary-learning-voice.md
  ehr-optimization-voice.md
  amazon-gemini-voice.md
  paypay-credit-voice.md
  
  # TTS用ナレーションテキスト（add_voice_generic.py と組み合わせて使う）
  burnout_texts.py
  toeic_texts.py
  
  # 既存（境界知能統計）
  borderline-intelligence-statistics.md
  borderline-intelligence-voice.md
  make_video.py
  add_voice.py
```

---

## 動画一覧

| # | ファイル名 | 記事タイトル | カテゴリ | スライド数 | 目安尺 |
|---|-----------|-------------|---------|----------|-------|
| 1 | make_video_burnout.py | 頑張りすぎると病気になる | ライフハック | 18 | ~6分 |
| 2 | make_video_musenmai.py | 無洗米コスパは実は同じ | ライフハック | 15 | ~5分 |
| 3 | make_video_toeic.py | TOEIC 905点。でも目的じゃない | 英語 | 14 | ~5分 |
| 4 | make_video_platform.py | 「適応」とは逃げる力も含む | ライフハック | 15 | ~6分 |
| 5 | make_video_nursing_future.py | 看護師の将来性【2025版】 | 看護 | 15 | ~6分 |
| 6 | make_video_nursing_dx.py | 医療DX看護配置基準の柔軟化 | 看護 | 15 | ~6分 |
| 7 | make_video_orcan.py | オルカンで投資をはじめた | ライフハック | 15 | ~6分 |
| 8 | make_video_nursing_career.py | 「看護師になること」を目標にするな | 看護 | 16 | ~6分 |
| 9 | make_video_cross_boundary.py | 越境学習が武器になる | 看護 | 15 | ~5分 |
| 10 | make_video_ehr.py | 「行動最適化」が奪うもの | 看護 | 17 | ~6分 |
| 11 | make_video_amazon_gemini.py | Amazon+Geminiで本をのぞく | ライフハック | 14 | ~5分 |
| 12 | make_video_paypay.py | PayPayクレジット事前払い | ライフハック | 14 | ~5分 |

---

## 使い方

### 1. スライド動画（音声なし）を生成する

```bash
cd video-scripts
python3 make_video_burnout.py        # → burnout-natural-living.mp4
python3 make_video_musenmai.py       # → musenmai-cospa.mp4
python3 make_video_toeic.py          # → toeic-905.mp4
# ... 他の記事も同様
```

### 2. 音声付き動画を生成する（TTS版）

```bash
# burnout記事の場合（burnout_texts.py が必要）
python3 add_voice_generic.py burnout  # → burnout-natural-living-with-voice.mp4

# toeic記事の場合
python3 add_voice_generic.py toeic    # → toeic-905-with-voice.mp4
```

### 3. 自分の声で録音する場合

各記事の `*-voice.md` を参照して読み上げ原稿を確認。スライド動画を画面録画しながら読み上げる。

---

## 動画エンジンのスライドタイプ

| タイプ | 説明 |
|-------|------|
| HOOK | 冒頭フック（大きいタイトル＋サブ） |
| SECTION | セクション区切り（左アクセントライン） |
| STATEMENT | 主張スライド（強調テキスト） |
| LIST | 番号付きリスト |
| TABLE | テーブル |
| QUOTE | 引用ボックス |
| COMPARE | 2列比較 |
| BIG_TEXT | 大きいテキスト強調 |
| BULLET | 箇条書き |
| CONCLUSION | 結論スライド |
| OUTRO | エンディング（CTA付き） |

---

## 共通設定

- **解像度**: 1920×1080 (Full HD)
- **フレームレート**: 30fps
- **カラーテーマ**: ダーク背景（#090909）+ アンバーアクセント
- **フォント**: IPAゴシック (ipag.ttf)
- **フェード**: スライド間 0.5秒
