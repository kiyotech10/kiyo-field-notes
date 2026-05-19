# Kiyo's Field Notes — プロジェクト引き継ぎ資料

> 作成日: 2026-05-19  
> 引き継ぎ元: Claude Code (Anthropic)  
> 引き継ぎ先: Gemini

---

## 1. プロジェクト概要と技術スタック

### サイト概要

| 項目 | 内容 |
|------|------|
| サイト名 | Kiyo's Field Notes |
| キャッチコピー | 看護・学習・読書・日常のフィールドノート |
| URL | https://kiyo-field-notes.vercel.app |
| コンセプト | 看護師として働きながら、日々の思考を整理するフィールドノート型ブログ |
| 記事執筆 | ユーザーのアイデア・体験をもとにAIが文章を執筆（ホームページに注記あり） |

### 技術スタック

| 項目 | 技術 | バージョン |
|------|------|-----------|
| フレームワーク | **Astro** | ^6.3.1 |
| 言語 | TypeScript | Astro同梱 (strict モード) |
| Node.js | — | >=22.12.0 (必須) |
| コンテンツ管理 | Astro Content Collections (MDX) | — |
| スタイリング | **カスタム CSS変数** (フレームワークなし) | — |
| パッケージマネージャー | npm | — |

### 主要ライブラリ

| パッケージ | 用途 |
|-----------|------|
| `@astrojs/mdx` | MDX形式の記事サポート |
| `@astrojs/rss` | RSSフィード生成 (`/rss.xml`) |
| `@astrojs/sitemap` | サイトマップ生成（※後述の既知バグあり） |
| `sharp` | 画像最適化 |

### フォント

Google Fonts から読み込み（外部CDN）:

- **EB Garamond** (400/500/600/italic) — 見出し用 (`--font-heading`)
- **Noto Serif JP** (400/500/700) — 本文用 (`--font-body`)

`src/assets/fonts/` に Atkinson Hyperlegible の woff ファイルもあるが、現在は未使用（グローバルCSSで参照されていない）。

### デザイントークン (CSS変数)

`src/styles/global.css` で定義:

```css
--bg: #f9f7f3          /* 背景色（オフホワイト） */
--text: #1c1a16        /* 本文テキスト */
--text-muted: #7a7568  /* サブテキスト、日付など */
--accent: #1a3a52      /* アクセント色（ネイビー） */
--accent-light: #2a5578
--border: #ddd8cf      /* ボーダー色 */
--max-width: 640px     /* コンテンツ最大幅 */
```

**ダークモード機能は存在しない**（過去に実装→リバート済み）。

---

## 2. ディレクトリ構成

```
kiyo-field-notes/
├── public/                    # 静的ファイル（ビルド時にそのままコピー）
│   ├── favicon.svg            # ファビコン (SVG)
│   ├── favicon.ico            # ファビコン (ICO)
│   └── og-default.svg         # OGP画像（デフォルト）
│
├── src/
│   ├── assets/                # 画像等（Astroの画像最適化対象）
│   │   ├── blog-placeholder-*.jpg  # プレースホルダー画像（現在未使用）
│   │   └── fonts/             # ローカルフォント（現在未使用）
│   │
│   ├── components/            # 再利用可能なAstroコンポーネント
│   │   ├── BaseHead.astro     # <head>要素（meta, OGP, GA, フォント）
│   │   ├── Header.astro       # サイトヘッダー + グローバルナビ
│   │   ├── HeaderLink.astro   # ナビリンク（active状態の判定ロジック含む）
│   │   ├── Footer.astro       # フッター（著作権表示）
│   │   └── FormattedDate.astro # 日付フォーマット（ja-JP形式）
│   │
│   ├── content/               # ブログ記事（Markdownファイル群）
│   │   ├── diary/             # 日常の記録
│   │   ├── english/           # 英語学習メモ
│   │   ├── study/             # 試験勉強記録
│   │   ├── reading/           # 読書メモ
│   │   ├── nursing/           # 看護に関する考察
│   │   └── lifehack/          # 日常をラクにする知恵
│   │
│   ├── layouts/
│   │   └── BlogPost.astro     # 記事ページの共通レイアウト
│   │
│   ├── pages/                 # ルーティング（ファイル = URL）
│   │   ├── index.astro        # トップページ（カテゴリグリッド + Recent一覧）
│   │   ├── about.astro        # Aboutページ
│   │   ├── rss.xml.js         # RSSフィード
│   │   ├── diary/
│   │   │   ├── index.astro    # /diary/ — 記事一覧
│   │   │   └── [...slug].astro # /diary/[記事ID]/ — 記事詳細
│   │   ├── english/           # 同構造（index + [...slug]）
│   │   ├── study/             # 同構造
│   │   ├── reading/           # 同構造
│   │   ├── nursing/           # 同構造
│   │   └── lifehack/          # 同構造
│   │
│   ├── styles/
│   │   └── global.css         # グローバルスタイル（CSS変数定義含む）
│   │
│   ├── consts.ts              # サイト名・説明など定数
│   ├── content.config.ts      # Contentコレクション定義・スキーマ
│   └── env.d.ts               # Astro型定義
│
├── astro.config.mjs           # Astro設定
├── tsconfig.json              # TypeScript設定
├── package.json               # 依存関係・スクリプト
└── .gitignore
```

---

## 3. 記事（コンテンツ）の作成・運用フロー

### 3-1. 新規記事の追加手順

1. **ファイル作成場所**: `src/content/{カテゴリ}/` 配下に `.md` または `.mdx` ファイルを作成する。

   ```
   src/content/diary/my-new-article.mdx
   src/content/nursing/some-topic.md
   ```

2. **ファイル名がそのままURLになる**（拡張子除く）:
   - `src/content/diary/summer-sky.mdx` → `/diary/summer-sky/`

3. Frontmatter（後述）を記述し、本文を書く。

4. 記事に使用する画像（heroImage）が必要な場合は、**記事ファイルと同じディレクトリに配置**する（例: `src/content/diary/summer-sky.jpg`）。

### 3-2. Frontmatterの記述ルール

```yaml
---
title: "記事タイトル"          # 必須: 文字列
description: "記事の説明文"    # 必須: 文字列（一覧・OGP・RSSに使用）
pubDate: 2026-05-19           # 必須: YYYY-MM-DD 形式
updatedDate: 2026-05-20       # 任意: 更新日（記事上部に「更新:」として表示）
heroImage: ./image.jpg        # 任意: 記事と同ディレクトリの画像への相対パス
---
```

**注意事項**:
- `pubDate` は `YYYY-MM-DD` 形式で記述（`z.coerce.date()` で変換される）。
- `heroImage` は **相対パスで記事ファイルと同ディレクトリ**に置く必要がある（`src/assets/` への相対パスも可能だが、記事ローカルが推奨）。
- `title` と `description` はOGPメタタグ・RSS・一覧ページにも使われる重要フィールド。
- タグ・カテゴリ分類はFrontmatterではなく、**ファイルの配置ディレクトリで決まる**。

### 3-3. カテゴリ一覧

| ディレクトリ | ラベル | 説明 |
|-------------|--------|------|
| `diary/` | Diary | 日常の出来事や気づき |
| `english/` | English | 英語学習のメモ |
| `study/` | Study | 試験勉強の記録 |
| `reading/` | Reading | 読書メモ |
| `nursing/` | Nursing | 看護に関する考察 |
| `lifehack/` | Lifehack | 日常をラクにする知恵 |

### 3-4. 画像・静的アセット

| 用途 | 配置場所 | 参照方法 |
|------|---------|---------|
| 記事ヒーロー画像 | `src/content/{カテゴリ}/` (記事と同階層) | Frontmatterの `heroImage: ./filename.jpg` |
| プレースホルダー画像 | `src/assets/` | `import` でAstro最適化を経由 |
| OGPデフォルト画像 | `public/og-default.svg` | `/og-default.svg` (絶対パス) |
| ファビコン | `public/` | 自動参照 |

`src/` 配下の画像は Astro の `<Image>` コンポーネントで自動最適化される。`public/` 配下の画像は最適化なしでそのままコピーされる。

---

## 4. 開発・ビルド・デプロイコマンド

```bash
# 依存関係インストール
npm install

# ローカル開発サーバー起動（http://localhost:4321）
npm run dev

# 本番ビルド（./dist/ に出力）
npm run build

# ビルド済みサイトのプレビュー
npm run preview

# Astro CLIの直接実行
npm run astro -- --help
npm run astro check      # TypeScript/Astro型チェック
npm run astro add <integration>  # インテグレーション追加
```

カスタムスクリプトや Lint/Format 設定は **現時点では未設定**（ESLint/Prettierなし）。

---

## 5. インフラ・デプロイ環境

### ホスティング

**Vercel** でホスティング。`astro.config.mjs` に本番URLが設定済み:

```js
site: 'https://kiyo-field-notes.vercel.app'
```

### リポジトリ

GitHub: `kiyotech10/kiyo-field-notes`

### デプロイフロー

- `main` ブランチへのプッシュで **Vercel が自動ビルド・デプロイ**（Vercel の Git Integration による）。
- CI/CD設定ファイル（GitHub Actions等）は**存在しない**。Vercelダッシュボードで直接管理。

### アナリティクス

**Google Analytics 4** が導入済み。`src/components/BaseHead.astro` に計測タグをハードコード:

```
Measurement ID: G-MQBHP6Z0PL
```

---

## 6. 環境変数と重要な設定ファイル

### 環境変数

**現在 `.env` は不要**（外部APIキー等は使用していない）。

Google Analytics のID（`G-MQBHP6Z0PL`）は `src/components/BaseHead.astro` にハードコードされている。将来的に環境変数化する場合のキー名:

| キー名 | 用途 |
|--------|------|
| `PUBLIC_GA_ID` | Google Analytics 測定ID（ハードコードから移行する場合） |

### astro.config.mjs

```js
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://kiyo-field-notes.vercel.app',
  integrations: [mdx()],  // ⚠️ sitemap() が未登録（後述の既知バグ参照）
});
```

`@astrojs/sitemap` はインポートされているが `integrations` 配列に追加されていない（**既知バグ**）。

### content.config.ts

6つのコレクション（diary, english, study, reading, nursing, lifehack）が定義されている。すべて同一の `postSchema` を共有:

```ts
z.object({
  title: z.string(),           // 必須
  description: z.string(),     // 必須
  pubDate: z.coerce.date(),    // 必須
  updatedDate: z.coerce.date().optional(),
  heroImage: z.optional(image()),
})
```

### tsconfig.json

Astro公式の `strict` 設定を継承し `strictNullChecks: true` を追加。

---

## 7. 現状の課題と未実装の機能（特記事項）

### 既知のバグ・不整合

#### 🔴 Bug 1: サイトマップが生成されていない

**場所**: `astro.config.mjs`

`@astrojs/sitemap` がインポートされているが `integrations` 配列に追加されていないため、`/sitemap-index.xml` が生成されない。`BaseHead.astro` では `<link rel="sitemap" href="/sitemap-index.xml" />` が出力されているため、リンク切れになっている。

**修正方法**:
```js
// astro.config.mjs
integrations: [mdx(), sitemap()],  // sitemap() を追加
```

---

#### 🟡 Bug 2: `Lifehack` カテゴリがヘッダーナビに存在しない

**場所**: `src/components/Header.astro`

ナビゲーションに `Lifehack` へのリンクがない（`/lifehack/` ページ自体は存在する）。

**修正方法**:
```astro
<!-- Header.astro の <nav> 内に追加 -->
<HeaderLink href="/lifehack">Lifehack</HeaderLink>
```

---

#### 🟡 Bug 3: `Lifehack` カテゴリが RSSフィードに含まれていない

**場所**: `src/pages/rss.xml.js`

`lifehack` コレクションが `getCollection` で取得されておらず、RSS配信対象外になっている。

**修正方法**:
```js
// rss.xml.js
const [diary, english, study, reading, nursing, lifehack] = await Promise.all([
  getCollection('diary'),
  getCollection('english'),
  getCollection('study'),
  getCollection('reading'),
  getCollection('nursing'),
  getCollection('lifehack'),  // 追加
]);
// allPosts の展開にも lifehack を追加する
```

---

#### 🟡 Bug 4: `BlogPost` レイアウトの `categoryLabels` に `lifehack` が未登録

**場所**: `src/layouts/BlogPost.astro` (21〜27行目)

`lifehack` カテゴリの記事ページで「← Back」リンクのラベルが `lifehack`（生の値）のまま表示される。

**修正方法**:
```ts
const categoryLabels: Record<string, string> = {
  diary: 'Diary',
  english: 'English',
  study: 'Study',
  reading: 'Reading',
  nursing: 'Nursing',
  lifehack: 'Lifehack',  // 追加
};
```

---

### 今後実装したい機能（アイデア）

- **検索機能** — カテゴリをまたいだキーワード検索（Fuse.js等のクライアントサイド検索）
- **タグ機能** — Frontmatterにタグを追加し、タグ別一覧ページを作る
- **OGP画像の自動生成** — 記事タイトルからSatori等で動的OGP画像を生成
- **ページネーション** — 各カテゴリ一覧が記事増加で長くなった場合に対応
- **関連記事表示** — 記事末尾に同カテゴリの他記事を表示
- **Lint/Formatter設定** — ESLint + Prettier の導入（現在未設定）

---

### 実装上の注意点・クセ

1. **URLは `post.id` をそのままスラグとして使用**。`id` はコレクションの `glob` ローダーがファイル名から自動生成する（拡張子なし）。URLは `/diary/summer-sky/` の形式（末尾スラッシュあり）。

2. **記事の読了時間は本文文字数から概算**。`[...slug].astro` 内で `Math.max(1, Math.ceil(body.length / 400))` で計算している（日本語前提の係数ではないため精度は低い）。

3. **コレクションのスキーマは全カテゴリ共通**（`postSchema` 関数を共有）。将来カテゴリ固有のフィールドが必要になったら `content.config.ts` で別スキーマを定義する必要がある。

4. **`study` カテゴリには現在記事が0件**。コレクション定義・ページルーティングは完備しているが `src/content/study/` ディレクトリが空。

5. **`reading` カテゴリも現在記事が0件**（`lifehack` へ移動された経緯あり）。

6. **Claude Code固有ファイル**: `.gitignore` に `.claude/` が記載されているが、現リポジトリには該当ディレクトリなし。引き継ぎ先AIが Claude Code を使う場合は自動生成される。

7. **Astro v6 の Content Collections は Loader API を使用**（v5以前の `src/content/config.ts` ではなく `src/content.config.ts` がルートに置かれている点に注意）。
