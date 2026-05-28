// @ts-check
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// 記事内のテーブルを横スクロール可能なラッパーで囲む（モバイルで本文ごと
// 横スクロールせず、テーブル単体だけをスライドできるようにするため）
function rehypeTableWrap() {
	return (tree) => {
		const walk = (node) => {
			if (!Array.isArray(node.children)) return;
			// 先に子を再帰処理してから包む（包んだラッパーを再走査して
			// 無限にネストするのを防ぐ）
			for (const child of node.children) walk(child);
			node.children = node.children.map((child) =>
				child.type === 'element' && child.tagName === 'table'
					? {
							type: 'element',
							tagName: 'div',
							properties: { className: ['table-scroll'] },
							children: [child],
						}
					: child,
			);
		};
		walk(tree);
	};
}

export default defineConfig({
	site: 'https://kiyo-field-notes.vercel.app',
	integrations: [mdx(), sitemap()],
	markdown: {
		rehypePlugins: [rehypeTableWrap],
	},
});
