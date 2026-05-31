#!/usr/bin/env node
// note.com貼り付け用 記事エクスポートスクリプト
// 使い方: node export-for-note.mjs

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CONTENT_DIRS = [
  { dir: 'diary',    label: 'Diary' },
  { dir: 'nursing',  label: 'Nursing' },
  { dir: 'lifehack', label: 'Lifehack' },
  { dir: 'english',  label: 'English' },
  { dir: 'study',    label: 'Study' },
  { dir: 'reading',  label: 'Reading' },
];

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { meta: {}, body: content };

  const meta = {};
  for (const line of match[1].split('\n')) {
    const [key, ...rest] = line.split(':');
    if (key && rest.length) {
      let val = rest.join(':').trim().replace(/^["']|["']$/g, '');
      if (key.trim() === 'tags') {
        val = val.replace(/[\[\]]/g, '').split(',').map(t => t.trim().replace(/^["']|["']$/g, '')).join(' ');
      }
      meta[key.trim()] = val;
    }
  }
  return { meta, body: match[2].trim() };
}

function convertToNote(body) {
  return body
    .replace(/^#{1}\s+/gm, '')        // h1 → 見出しなし（noteのタイトルに使う）
    .replace(/^#{2}\s+/gm, '■ ')      // h2 → ■
    .replace(/^#{3}\s+/gm, '▶ ')      // h3 → ▶
    .replace(/\*\*(.*?)\*\*/g, '《$1》') // bold → 《》
    .replace(/`([^`]+)`/g, '$1')       // インラインコード → プレーンテキスト
    .replace(/^---$/gm, '\n──────────\n') // hr → 区切り線
    .trim();
}

const OUTPUT_DIR = path.join(__dirname, 'note-export');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

let summary = [];

for (const { dir, label } of CONTENT_DIRS) {
  const dirPath = path.join(__dirname, 'src', 'content', dir);
  if (!fs.existsSync(dirPath)) continue;

  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.mdx') || f.endsWith('.md'));

  for (const file of files) {
    const raw = fs.readFileSync(path.join(dirPath, file), 'utf-8');
    const { meta, body } = parseFrontmatter(raw);
    const noteBody = convertToNote(body);

    const title = meta.title || file.replace(/\.mdx?$/, '');
    const date = meta.pubDate || '';
    const tags = meta.tags ? meta.tags.split(' ').map(t => `#${t}`).join(' ') : '';
    const blogUrl = `https://kiyo-field-notes.vercel.app/${dir}/${file.replace(/\.mdx?$/, '')}/`;

    const noteText = [
      title,
      '',
      noteBody,
      '',
      '──────────',
      `カテゴリ: ${label}`,
      date ? `投稿日: ${date}` : '',
      tags ? `タグ: ${tags}` : '',
      `元記事: ${blogUrl}`,
    ].filter(l => l !== undefined).join('\n');

    const outFile = path.join(OUTPUT_DIR, `${label}_${file.replace(/\.mdx?$/, '')}.txt`);
    fs.writeFileSync(outFile, noteText, 'utf-8');

    summary.push({ label, title, file: outFile });
    console.log(`✓ ${label}: ${title}`);
  }
}

console.log(`\n${summary.length}件 → note-export/ フォルダに出力しました`);
