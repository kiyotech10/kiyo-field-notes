import { getCollection } from 'astro:content';

export async function GET() {
	const categories = ['diary', 'english', 'study', 'reading', 'nursing', 'lifehack'] as const;
	const posts = (
		await Promise.all(
			categories.map(async (cat) => {
				const items = await getCollection(cat);
				return items.map((p) => ({
					title: p.data.title,
					description: p.data.description,
					category: cat,
					tags: p.data.tags ?? [],
					pubDate: p.data.pubDate.toISOString(),
					slug: p.id,
					url: `/${cat}/${p.id}/`,
				}));
			})
		)
	)
		.flat()
		.sort((a, b) => b.pubDate.localeCompare(a.pubDate));

	return new Response(JSON.stringify(posts), {
		headers: { 'Content-Type': 'application/json' },
	});
}
